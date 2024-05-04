import socket
import json
import time
import paho.mqtt.client as mqtt
import configparser

class PlaneData:
    def __init__(self):
        self.mode_s = None
        self.callsign = None
        self.lat = None
        self.lon = None
        self.alt = None
        self.sqw = None

def process_data(data, planes, mqtt_client):
    # Split data by lines
    lines = data.split('\n')

    # Iterate over each line
    for line in lines:
        # Split each line by comma
        parts = line.split(',')

        # Check if parts list has enough elements
        if len(parts) >= 17:
            # Extract ModeS, Callsign, Lat, Long, Alt, and SQW
            mode_s = parts[4]
            callsign = parts[10]
            lat = parts[14]
            lon = parts[15]
            alt = parts[11]
            sqw = parts[16]

            # If ModeS not in planes, create a new PlaneData object
            if mode_s not in planes:
                planes[mode_s] = PlaneData()

            # Update PlaneData object with the received data
            plane = planes[mode_s]
            plane.mode_s = mode_s
            if callsign and plane.callsign is None:
                plane.callsign = callsign
            if lat and plane.lat is None:
                plane.lat = lat
            if lon and plane.lon is None:
                plane.lon = lon
            if alt and plane.alt is None:
                plane.alt = alt
            if sqw and plane.sqw is None:
                plane.sqw = sqw

            # Check if all fields are populated
            if all(vars(plane).values()):
                # Publish data to MQTT broker
                topic = f"Planes/{plane.callsign}"
                payload = json.dumps(vars(plane))
                mqtt_client.publish(topic, payload)

                # Remove the plane data from the dictionary once published
                del planes[mode_s]
        else:
            # If data format is not as expected, skip processing this line
            continue

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection to MQTT broker failed")

def main():
    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get dump1090 configuration
    dump1090_host = config.get('dump1090', 'host')
    dump1090_port = config.getint('dump1090', 'port')

    # Get MQTT configuration
    mqtt_host = config.get('mqtt', 'host')
    mqtt_port = config.getint('mqtt', 'port')
    #get username and password if they exist
    mqtt_username = config.get('mqtt', 'username', fallback=None)
    mqtt_password = config.get('mqtt', 'password', fallback=None)

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Dictionary to store plane data until all fields are populated
    planes = {}

    # Connect to MQTT broker
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(mqtt_host, mqtt_port, 60)

    try:
        # Connect to dump1090
        s.connect((dump1090_host, dump1090_port))
        print("Connected to dump1090")

        # Receive data continuously
        while True:
            # Receive data from dump1090
            data = s.recv(1024).decode('utf-8')

            # Process the received data
            if data:
                process_data(data, planes, mqtt_client)
                time.sleep(0.1)  # Delay to avoid flooding MQTT broker

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Closing connection.")
    finally:
        # Close the connection when done
        s.close()

if __name__ == "__main__":
    main()
