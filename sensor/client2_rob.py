import socket
import json
import ssl

import socket
import json
import ssl


def get_temperature():
    while True:
        try:
            temp = float(input("Enter temperature value: "))
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

def run_client():
    # create a socket object
    s = socket.socket()

    # get local machine name
    host = socket.gethostname()

#TOS Stuff
    DSCP=0x90
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)
   
    # define the port on which you want to connect
    port = 12345

    # connect to the server on local computer
    context = ssl.create_default_context()
    # Bypass SSL certificate verification
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    s = context.wrap_socket(s, server_hostname=host)
    s.connect((host, port))

    # define the sensor data
    temperature = get_temperature()
    sensor_data = {
        "sensor_name": "temperature_sensor",
        "sensor_value": temperature,
        "sensor_unit": "Celsius",
        "sensor_id": "abc123" # new: add sensor id
    }

    # convert the sensor data to JSON format
    sensor_json = json.dumps(sensor_data)

    # send the sensor data to the server
    s.sendall(sensor_json.encode())

    # receive the response from the server
    response = s.recv(1024).decode()
    print("Response from server: ", response)

    # close the connection
    s.close()

run_client()


def get_temperature():
    while True:
        try:
            temp = float(input("Enter temperature value: "))
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

def run_client():
    # create a socket object
    s = socket.socket()

    # get local machine name
    host = socket.gethostname()

#TOS Stuff
    DSCP=0x90
    s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)
   
    # define the port on which you want to connect
    port = 12345

    # connect to the server on local computer
    context = ssl.create_default_context()
    # Bypass SSL certificate verification
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    s = context.wrap_socket(s, server_hostname=host)
    s.connect((host, port))

    # define the sensor data
    temperature = get_temperature()
    sensor_data = {
        "sensor_name": "temperature_sensor",
        "sensor_value": temperature,
        "sensor_unit": "Celsius",
        "sensor_id": "abc123" # new: add sensor id
    }

    # convert the sensor data to JSON format
    sensor_json = json.dumps(sensor_data)

    # send the sensor data to the server
    s.sendall(sensor_json.encode())

    # receive the response from the server
    response = s.recv(1024).decode()
    print("Response from server: ", response)

    # close the connection
    s.close()

run_client()

