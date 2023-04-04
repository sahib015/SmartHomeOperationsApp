import socket
import json
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import time

#Method to return the temperature value from the sensor to the server
#The value is generated randomly using the random library
def get_temperature():
    while True:
        try:
            # Get Temperature
            temp = random.randint(1,40) #random temperature values between 1 and 40
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

#Method to return the humidity value from the sensor to the server
#The value is generated randomly using the random library

def getHumidity():
    while True:
        try:
            #Get Humidity
            humidity = random.randint(1,100)#random humidity % values between 1 and 100
            return humidity
        except ValueError:
            print("Invalid Humidity value. Please try again.")

#Method defining the client ie temperature and humidity sensor that is unregistered in the server
def run_client():
    while True:
        try:
            # Set DSCP Value = AF41
            DSCP = 0x90
            
            # Sensor Type
            sensor_type = "known_sensor" 

            # create a socket object
            s = socket.socket()

            # set the TOS marking for the socket
            s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)

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
            humidity = getHumidity()
            tempHumidSensor_data = {
                "sensor_type": sensor_type,
                "sensor_name": "temperatureHumidity_sensor",
                "sensor_tempValue": temperature,
                "sensor_humidityValue": humidity,
                "sensor_unit": "Celsius and %",
                "sensor_id": "321cba" # new: add sensor id
            }

            # convert the sensor data to JSON format
            sensor_json = json.dumps(tempHumidSensor_data)

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
       
            #Time nterval for the update. For demonstration purposes it is set to 5 seconds
            time.sleep(5)

        except socket.error as e:
            print(f"Socket error occurred: {e}")

#run the client method 
run_client()

