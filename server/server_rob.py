import socket
import json
import ssl
import scapy

# create a socket object
s = socket.socket()

    # get local machine name
host = socket.gethostname()

#TOS Stuff
DSCP=0x88
s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)

# define the port on which you want to bind
port = 12345

# bind the socket to a public host and port
s.bind((host, port))

# listen for incoming connections
s.listen(1)

# define the registered sensor IDs
registered_sensors = ["abc123", "def456", "ghi789"] # new: add registered sensor IDs

while True:
    # accept the incoming connection
    client_socket, addr = s.accept()
    print("Got a connection from ", addr)

    # wrap the socket in SSL/TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    client_socket = context.wrap_socket(client_socket, server_side=True)

    # receive the sensor data from the client
    sensor_data = client_socket.recv(1024).decode()
    print("Received sensor data: ", sensor_data)

    # parse the sensor data from JSON format
    sensor_json = json.loads(sensor_data)

    # check if the sensor is registered
    if sensor_json["sensor_id"] not in registered_sensors:
        response = "Sensor not registered"
    else:
        # check the sensor data and send the appropriate response
        if sensor_json["sensor_name"] == "temperature_sensor":
            if sensor_json["sensor_value"] > 30.0:
                response = "Turn on the AC"
            elif sensor_json["sensor_value"] < 10.0:
                response = "Turn on the heater"
            else:
                response = "Temperature is normal"
        else:
            response = "Unknown sensor"

    # send the response to the client
    client_socket.send(response.encode())

    # close the connection
    client_socket.close()

