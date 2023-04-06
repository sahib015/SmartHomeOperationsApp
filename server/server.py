#import libraries to be used 

import socket
import json
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from termcolor import colored

#Method defining the server configurations to listen to incomming connections 
# and send packets of information back to the sensor recieving data from. 

def run_server():
    try:
        # Set DSCP Value = AF41
        DSCP = 0xB8
        # create a socket object and set Type of Service (TOS) field in the IP header of the network packet
        s = socket.socket()
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))
    
        # listen for incoming connections
        s.listen(1)
        print("Server is running on:", socket.gethostbyname(host), "port", port)# confirm incomming connection printed on terminal
        # define the registered sensor IDs
        registered_sensors = ["abc123", "def456", "ghi789"] 
    
        # define the shared secret key for message encryption
        key = b'mysecretpassword'
        iv = key
    
        while True:
            # accept the incoming connection
            client_socket, addr = s.accept()
            print("Got a connection from ", addr)
   
            #  wrap the socket in SSL/TLS and  receive the encrypted data from the client
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            client_socket = context.wrap_socket(client_socket, server_side=True)
    
           
            encrypted_sensor_data = client_socket.recv(1024)
            print(colored("Received encrypted sensor data: ", "blue"), encrypted_sensor_data)
    
            # decrypt the sensor data using AES-CBC encryption
            decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
            sensor_data = unpad(decrypt_cipher.decrypt(encrypted_sensor_data), AES.block_size).decode()
            print(colored("Decrypted sensor data: ", "blue"), sensor_data)
    
            sensor_json = json.loads(sensor_data)
        
            # perform checks on the sensor

            if sensor_json["sensor_type"] != "known_sensor":
                response = colored("Unknown sensor", "yellow", "on_red", ["bold", "underline"])
            else:
                
                if sensor_json["sensor_id"] not in registered_sensors:
                    response = colored("Sensor not registered", "yellow")
                else:
                    
                    if sensor_json["sensor_tempValue"] > 30.0 or sensor_json["sensor_humidityValue"] > 60.0:
                        response = colored("Turn on the AC", "yellow")
                    elif sensor_json["sensor_tempValue"] < 10. or sensor_json["sensor_humidityValue"] < 30.0:
                        response = colored("Turn on the heater", "yellow")
                    else:
                        response = colored("Temperature and humidity of the room is normal", "green")
            print(colored("Response to sensor:", "blue"), response)

            # encrypt the server response using AES-CBC encryption and send the response to the client
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_response = pad(response.encode(), AES.block_size)
            encrypted_response = cipher.encrypt(padded_response)
            client_socket.send(encrypted_response)
        
            # close the connection
            client_socket.close()
            print(f"Connection with {addr} closed")


    except socket.error as e:
        print(f"Socket error occurred: {e}")

#Run the server. To note the server requires to be running before recieving any connections from the sensors
run_server()
