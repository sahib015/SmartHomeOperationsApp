import socket
import json
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from termcolor import colored
import threading

#Method to handle the incoming connections between the sensors
def handle_connection(client_socket, addr):
    while True:
        try:
            registered_sensors = ["abc123", "def456", "ghi789"]

            # define the shared secret key for message encryption
            key = b'mysecretpassword'
            iv = key

            # receive the encrypted sensor data
            encrypted_sensor_data = client_socket.recv(1024)
            print(colored("Received encrypted sensor data: ", "blue"), "Session:", addr, "Data:", encrypted_sensor_data)
            
            # close connection when ACK is empty
            if encrypted_sensor_data == b'':
                client_socket.close()
                print(f"Connection with {addr} closed")
                break
            # decrypt the sensor data
            decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
            sensor_data = unpad(decrypt_cipher.decrypt(encrypted_sensor_data), AES.block_size).decode()
            print(colored("Decrypted sensor data: ", "blue"), "Session:", addr, "Data:", sensor_data)

            # store data in JSON
            sensor_json = json.loads(sensor_data)

            
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
            print(colored("Response to sensor:", "blue"), "Session:", addr, "SensorID:", sensor_json["sensor_id"], "Response:", response)

            # encrypt the server response
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_response = pad(response.encode(), AES.block_size)
            encrypted_response = cipher.encrypt(padded_response)
        
            # send the encrypted response to the client
            client_socket.send(encrypted_response)
            print(colored("Encrypted server response sent: ", "blue"), "Session:", addr, "SensorID:", sensor_json["sensor_id"], "Response:", encrypted_response)
        
        except Exception as e:
            print(f"Exception occurred: {e}")

def run_server():
    try:
        # Set DSCP Value = EF
        DSCP = 0xB8

        # create a socket object and set TOS field in the IP header of the network packet
        s = socket.socket()
        s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)
      
        host = socket.gethostname()
        port = 12345

        # bind the socket to a public host and port
        s.bind((host, port))
        
        # listen for any incoming connections
        s.listen(5)
        print("Server is running on:", socket.gethostbyname(host), "port", port)

        #Run the server. To note the server requires to be running before recieving any connections from the sensors
        while True:
            # accept the incoming connection
            client_socket, addr = s.accept()
            print("Got a connection from ", addr)

            # wrap the socket in SSL/TLS
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile="server.crt", keyfile="server.key")
            client_socket = context.wrap_socket(client_socket, server_side=True)

            # Client connection
            threading.Thread(target=handle_connection,args=(client_socket, addr), daemon=True).start()
        
        # close the connection
        client_socket.close()
        print(f"Connection with {addr} closed")
        
    except socket.error as e:
        print(f"Socket error occurred: {addr} {e}")
        
run_server()
