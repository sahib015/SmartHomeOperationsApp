import socket
import json
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def get_temperature():
    while True:
        try:
            temp = float(input("Enter temperature value: "))
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

def run_client():

    # Sensor Type
    sensor_type = "known_sensor" 

    # create a socket object
    s = socket.socket()

    # get local machine name
    host = socket.gethostname()

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
        "sensor_type": sensor_type,
        "sensor_name": "temperature_sensor",
        "sensor_value": temperature,
        "sensor_unit": "Celsius",
        "sensor_id": "abc123" # new: add sensor id
    }

    # convert the sensor data to JSON format
    sensor_json = json.dumps(sensor_data)

    # set up the encryption key and IV
    key = b'mysecretpassword'
    iv = key

    # ensure the IV is 16 bytes long
    if len(iv) != 16:
        raise ValueError("IV must be 16 bytes long")

    # create the AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # pad the sensor data to a multiple of 16 bytes
    padded_data = pad(sensor_json.encode(), AES.block_size)

    # encrypt the padded sensor data using AES-CBC
    encrypted_data = cipher.encrypt(padded_data)

    # send the encrypted sensor data to the server
    s.sendall(encrypted_data)

    # receive the response from the server
    encrypted_response = s.recv(1024)
    print("Received encrypted server response: ", encrypted_response)
    
    # create a new AES cipher object for decrypting the response data
    decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)

    # decrypt the response using AES-CBC
    decrypted_response = decrypt_cipher.decrypt(encrypted_response)

    # unpad the decrypted response
    unpadded_response = unpad(decrypted_response, AES.block_size)
    
    # convert the response from bytes to string format
    response = unpadded_response.decode()

    print("Decrypted Response from server: ", response)

    # close the connection
    s.close()

run_client()

