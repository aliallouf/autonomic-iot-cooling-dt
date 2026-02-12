import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
import rtamt

# --- 1. STL SPECIFICATION ---
spec = rtamt.StlDiscreteTimeSpecification()
spec.declare_var('temp', 'float')
spec.declare_var('fan_status', 'float')

# FORMAL RULE: (Hot -> Fan ON) AND (Cool -> Fan OFF)
# This model defines the "Safety Envelope" for our Autonomic Twin
spec.spec = '((temp > 30) implies (fan_status >= 1)) and ((temp <= 30) implies (fan_status <= 0))'

try:
    spec.parse()
except rtamt.RTAMTException as e:
    print(f'STL Parse Error: {e}')
    exit(1)

timestamp = 0
current_fan_state = 0.0

# --- 2. MQTT CALLBACKS ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Autonomic DT Online. Synchronizing with Physical Object...")
        # Subscribing to all relevant telemetry for unit 001
        client.subscribe("telemetry/+/001")
    else:
        print(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    global timestamp, current_fan_state
    payload = msg.payload.decode()

    # Reflection: Update local understanding of Physical Fan State
    if "fan_status" in msg.topic:
        current_fan_state = 1.0 if payload == "ON" else 0.0

    # Reflection: Process Temp and Evaluate Model
    if "temp" in msg.topic:
        try:
            current_temp = float(payload)
            
            # THE COGNITIVE STEP: Evaluate the formal model
            rob = spec.update(timestamp, [('temp', current_temp), ('fan_status', current_fan_state)])
            
            # --- SEND ROBUSTNESS TO NODE-RED ORCHESTRATOR ---
            # This enables the 'Master Replica' to log and visualize the DT health
            client.publish("dt/monitor/robustness", str(rob))
            
            print(f"[TS:{timestamp}] Temp:{current_temp}°C | Fan:{'ON' if current_fan_state==1 else 'OFF'} | Rob:{rob}")
            
            # --- THE AUTONOMIC DECISION ENGINE (Integrated Execution) ---
            if rob < 0:
                if current_temp > 30 and current_fan_state == 0.0:
                    print("🚨 VIOLATION: Too Hot! Overriding -> ON")
                    client.publish("commands/fan/001", "ON")
                
                elif current_temp <= 30 and current_fan_state == 1.0:
                    print("🚨 VIOLATION: Wasting Energy! Overriding -> OFF")
                    client.publish("commands/fan/001", "OFF")
            
            timestamp += 1
        except Exception as e:
            print(f"Logic Error: {e}")

# --- 3. INITIALIZE ---
client = mqtt.Client(CallbackAPIVersion.VERSION1, "DT_Cognitive_Engine_001")
client.on_connect = on_connect
client.on_message = on_message

print("🔗 Connecting to HiveMQ...")
client.connect("broker.hivemq.com", 1883)
client.loop_forever()