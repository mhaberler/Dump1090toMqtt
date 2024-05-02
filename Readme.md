# Dump1090toMQTT


![Logo](logo.jpg)
    
## Overview

Dump1090toMQTT is a Python script that monitors data from a dump1090 server, which provides information about airplanes, and publishes this data to an MQTT broker for further processing. The script can be run as a service, continuously collecting data and publishing it to the MQTT broker.

## Features

- Monitors data from a dump1090 server.
- Publishes airplane data to an MQTT broker.
- Can be run as a service for continuous monitoring.

## Requirements

- Python 3.x
- paho-mqtt library (`pip install paho-mqtt`)

## Configuration

The configuration for the script is stored in a `config.ini` file. This file contains the following sections:

### [dump1090]

- `host`: The IP address of the dump1090 server.
- `port`: The port number of the dump1090 server.

### [mqtt]

- `host`: The IP address of the MQTT broker.
- `port`: The port number of the MQTT broker.

Example `config.ini`:

```ini
[dump1090]
host = 172.25.164.232
port = 30003

[mqtt]
host = 172.25.96.250
port = 1883
```

## Usage

1. Install the required dependencies:

   ```bash
   pip install paho-mqtt
   ```

2. Configure the `config.ini` file with the appropriate IP addresses and port numbers.

3. Run the script:

   ```bash
   python Dump1090toMQTT.py
   ```

   The script will connect to the dump1090 server, collect airplane data, and publish it to the MQTT broker.

## Running as a Service

To run the script as a service, follow these steps:

1. Create a systemd service unit file named `dump1090tomqtt.service`:

   ```ini
   [Unit]
   Description=Dump1090toMQTT Service
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/your/script/directory
   ExecStart=/usr/bin/python3 /path/to/your/Dump1090toMQTT.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Replace `your_username` with your username and `/path/to/your/script` with the actual path where your Python script is located.

2. Save the file and reload the systemd manager configuration:

   ```bash
   sudo systemctl daemon-reload
   ```

3. Start and enable the service:

   ```bash
   sudo systemctl start dump1090tomqtt
   sudo systemctl enable dump1090tomqtt
   ```

   Now your script will run as a service and automatically start whenever your system boots up.


