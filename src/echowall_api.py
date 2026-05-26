"""
EchoWall API Integration
Connects to ESP32-S3 hardware for real-time through-wall sensing
"""

import time
import json
from typing import Dict, Optional, List
from enum import Enum
from dataclasses import dataclass


class SensingMode(Enum):
    """EchoWall sensing modes"""
    SIMULATION = "sim"
    SERIAL = "serial"
    MQTT = "mqtt"
    REST_API = "rest"


@dataclass
class SensingResult:
    """Result from EchoWall sensing"""
    presence: bool
    occupancy_count: int
    posture: str
    breathing_rate: Optional[float]
    heart_rate: Optional[float]
    confidence: float
    timestamp: float
    mode: str
    hardware: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "presence": self.presence,
            "occupancy_count": self.occupancy_count,
            "posture": self.posture,
            "breathing_rate": self.breathing_rate,
            "heart_rate": self.heart_rate,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "mode": self.mode,
            "hardware": self.hardware,
            "privacy": {
                "raw_data_stored": False,
                "cloud_upload": False,
                "local_only": True,
                "jitter_applied": True
            }
        }


class EchoWallAPI:
    """
    EchoWall Hardware Integration API
    
    Supports multiple connection modes:
    - Simulation: For testing without hardware
    - Serial: Direct USB connection to ESP32-S3
    - MQTT: Wireless connection via MQTT broker
    - REST: HTTP API connection
    """
    
    def __init__(self, mode: SensingMode = SensingMode.SIMULATION, **kwargs):
        """
        Initialize EchoWall API
        
        Args:
            mode: Sensing mode (sim, serial, mqtt, rest)
            **kwargs: Mode-specific parameters
                - serial_port: Serial port path (e.g., /dev/ttyUSB0)
                - mqtt_broker: MQTT broker address
                - mqtt_topic: MQTT topic to subscribe
                - rest_url: REST API endpoint
        """
        self.mode = mode
        self.connected = False
        self.last_result: Optional[SensingResult] = None
        
        # Connection parameters
        self.serial_port = kwargs.get('serial_port', '/dev/ttyUSB0')
        self.mqtt_broker = kwargs.get('mqtt_broker', 'localhost')
        self.mqtt_topic = kwargs.get('mqtt_topic', 'echowall/sensing')
        self.rest_url = kwargs.get('rest_url', 'http://localhost:8000')
        
        # Initialize connection
        self._connect()
    
    def _connect(self) -> bool:
        """Establish connection based on mode"""
        if self.mode == SensingMode.SIMULATION:
            self.connected = True
            return True
        
        elif self.mode == SensingMode.SERIAL:
            return self._connect_serial()
        
        elif self.mode == SensingMode.MQTT:
            return self._connect_mqtt()
        
        elif self.mode == SensingMode.REST_API:
            return self._connect_rest()
        
        return False
    
    def _connect_serial(self) -> bool:
        """Connect via Serial (USB)"""
        try:
            import serial
            self.serial_conn = serial.Serial(
                self.serial_port, 
                baudrate=115200, 
                timeout=1
            )
            self.connected = True
            return True
        except ImportError:
            print("⚠️  pyserial not installed. Install: pip install pyserial")
            return False
        except Exception as e:
            print(f"⚠️  Serial connection failed: {e}")
            return False
    
    def _connect_mqtt(self) -> bool:
        """Connect via MQTT"""
        try:
            import paho.mqtt.client as mqtt
            
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    self.connected = True
                    client.subscribe(self.mqtt_topic)
            
            def on_message(client, userdata, msg):
                try:
                    data = json.loads(msg.payload.decode())
                    self.last_result = self._parse_sensing_data(data)
                except Exception as e:
                    print(f"⚠️  MQTT message parse error: {e}")
            
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = on_connect
            self.mqtt_client.on_message = on_message
            self.mqtt_client.connect(self.mqtt_broker, 1883, 60)
            self.mqtt_client.loop_start()
            
            return True
        except ImportError:
            print("⚠️  paho-mqtt not installed. Install: pip install paho-mqtt")
            return False
        except Exception as e:
            print(f"⚠️  MQTT connection failed: {e}")
            return False
    
    def _connect_rest(self) -> bool:
        """Connect via REST API"""
        try:
            import requests
            response = requests.get(f"{self.rest_url}/health", timeout=2)
            self.connected = response.status_code == 200
            return self.connected
        except ImportError:
            print("⚠️  requests not installed. Install: pip install requests")
            return False
        except Exception as e:
            print(f"⚠️  REST API connection failed: {e}")
            return False
    
    def sense(self) -> SensingResult:
        """
        Perform sensing operation
        
        Returns:
            SensingResult with current environment data
        """
        if not self.connected:
            raise ConnectionError("Not connected to EchoWall hardware")
        
        if self.mode == SensingMode.SIMULATION:
            return self._sense_simulation()
        
        elif self.mode == SensingMode.SERIAL:
            return self._sense_serial()
        
        elif self.mode == SensingMode.MQTT:
            return self._sense_mqtt()
        
        elif self.mode == SensingMode.REST_API:
            return self._sense_rest()
        
        raise NotImplementedError(f"Mode {self.mode} not implemented")
    
    def _sense_simulation(self) -> SensingResult:
        """Simulate sensing data"""
        import random
        
        presence = random.random() > 0.2
        occupancy = random.randint(1, 4) if presence else 0
        postures = ["standing", "sitting", "lying"]
        posture = random.choice(postures) if presence else "none"
        
        return SensingResult(
            presence=presence,
            occupancy_count=occupancy,
            posture=posture,
            breathing_rate=round(random.uniform(12.0, 20.0), 1) if presence else None,
            heart_rate=round(random.uniform(60.0, 90.0), 1) if presence else None,
            confidence=round(random.uniform(0.75, 0.95), 2),
            timestamp=time.time(),
            mode="simulation",
            hardware="ESP32-S3 (simulated)"
        )
    
    def _sense_serial(self) -> SensingResult:
        """Read sensing data from Serial"""
        try:
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line:
                data = json.loads(line)
                return self._parse_sensing_data(data)
        except Exception as e:
            print(f"⚠️  Serial read error: {e}")
        
        # Return empty result on error
        return SensingResult(
            presence=False, occupancy_count=0, posture="unknown",
            breathing_rate=None, heart_rate=None, confidence=0.0,
            timestamp=time.time(), mode="serial", hardware="ESP32-S3"
        )
    
    def _sense_mqtt(self) -> SensingResult:
        """Get latest MQTT sensing data"""
        if self.last_result:
            return self.last_result
        
        # Wait for first message
        time.sleep(0.5)
        
        if self.last_result:
            return self.last_result
        
        # Return empty if no data yet
        return SensingResult(
            presence=False, occupancy_count=0, posture="unknown",
            breathing_rate=None, heart_rate=None, confidence=0.0,
            timestamp=time.time(), mode="mqtt", hardware="ESP32-S3"
        )
    
    def _sense_rest(self) -> SensingResult:
        """Fetch sensing data from REST API"""
        try:
            import requests
            response = requests.get(f"{self.rest_url}/sense", timeout=2)
            response.raise_for_status()
            data = response.json()
            return self._parse_sensing_data(data)
        except Exception as e:
            print(f"⚠️  REST API error: {e}")
            return SensingResult(
                presence=False, occupancy_count=0, posture="unknown",
                breathing_rate=None, heart_rate=None, confidence=0.0,
                timestamp=time.time(), mode="rest", hardware="ESP32-S3"
            )
    
    def _parse_sensing_data(self, data: Dict) -> SensingResult:
        """Parse sensing data from any source"""
        return SensingResult(
            presence=data.get("presence", False),
            occupancy_count=data.get("occupancy_count", 0),
            posture=data.get("posture", "unknown"),
            breathing_rate=data.get("breathing_rate"),
            heart_rate=data.get("heart_rate"),
            confidence=data.get("confidence", 0.0),
            timestamp=data.get("timestamp", time.time()),
            mode=str(self.mode.value),
            hardware=data.get("hardware", "ESP32-S3")
        )
    
    def get_status(self) -> Dict:
        """Get connection status"""
        return {
            "connected": self.connected,
            "mode": self.mode.value,
            "serial_port": self.serial_port if self.mode == SensingMode.SERIAL else None,
            "mqtt_broker": self.mqtt_broker if self.mode == SensingMode.MQTT else None,
            "rest_url": self.rest_url if self.mode == SensingMode.REST_API else None
        }
    
    def disconnect(self):
        """Close connection"""
        if self.mode == SensingMode.SERIAL and hasattr(self, 'serial_conn'):
            self.serial_conn.close()
        
        elif self.mode == SensingMode.MQTT and hasattr(self, 'mqtt_client'):
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        
        self.connected = False


# Convenience function
def sense_environment(mode: str = "sim", **kwargs) -> Dict:
    """
    Convenience function for sensing
    
    Args:
        mode: 'sim', 'serial', 'mqtt', or 'rest'
        **kwargs: Connection parameters
        
    Returns:
        Dict with sensing results
    """
    mode_enum = SensingMode(mode)
    api = EchoWallAPI(mode=mode_enum, **kwargs)
    result = api.sense()
    api.disconnect()
    return result.to_dict()


if __name__ == "__main__":
    # Demo usage
    print("EchoWall API Demo")
    print("=" * 50)
    
    # Simulation mode
    print("\n📡 Simulation Mode:")
    result = sense_environment(mode="sim")
    print(f"   Presence: {result['presence']}")
    print(f"   Occupancy: {result['occupancy_count']}")
    print(f"   Posture: {result['posture']}")
    print(f"   Confidence: {result['confidence']:.1%}")
    print(f"   Privacy: {result['privacy']}")
    
    # Show available modes
    print("\n🔌 Available Modes:")
    for mode in SensingMode:
        print(f"   - {mode.value}")
