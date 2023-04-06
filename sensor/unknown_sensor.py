#import libraries to be used
import socket
import json
import ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from termcolor import colored
import random
import time

#Method to return the temperature value from the sensor to the server
#The value is generated randomly using the random library
#@return- return temp value generated

def get_temperature():
    while True:
        try:
            temp = random.randint(1,40) #random temperature values between 1 and 40
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

#Method to return the humidity value from the sensor to the server
#The value is generated randomly using the random library
#@return- return humidity value generated

def getHumidity():
    while True:
        try:
            humidity = random.randint(1,100)#random humidity % values between 1 and 100
            return humidity
        except ValueError:
            print("Invalid Humidity value. Please try again.")

#Method defining the client ie temperature and humidity sensor that is unknown to the server
def run_client():

    while True:
        try:
            # Set DSCP Value = AF32
            DSCP = 0x70

            sensor_type = "unknown_sensor" 

           #create a socket object and set the TOS marking for the socket
            s = socket.socket()
            s.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, DSCP)

            host = socket.gethostname()
           
            port = 12345

            # connect to the server on local computer
            context = ssl.create_default_context()
            # Bypass SSL certificate verification
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            s = context.wrap_socket(s, server_hostname=host)
            s.connect((host, port))#Open connection

             # add sensor data
            temperature = get_temperature()
            humidity = getHumidity()
            sensor_data = {
                "sensor_type": sensor_type,
                "sensor_name": "temperatureHumidity_sensor",
                "sensor_tempValue": temperature,
                "sensor_humidityValue": humidity,
                "sensor_unit": "Celsius and %",
                "sensor_id": "xyz987" 
            }

            # convert the sensor data to JSON format
            sensor_json = json.dumps(sensor_data)

            # set up the encryption key and IV
            key = b'mysecretpassword'
            iv = key

            # ensure the IV is 16 bytes long
            if len(iv) != 16:
                raise ValueError("IV must be 16 bytes long")

            # create the AES cipher object ensuring its 16 bytes long and encrypt the data before sending the data to the server
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(sensor_json.encode(), AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            s.sendall(encrypted_data)

            # receive the response from the server
            encrypted_response = s.recv(1024)
            print(colored("Received encrypted server response: ", "blue"), encrypted_response)
    
           
            # create a new AES cipher object for decrypting the response data and recode the encrypted data recieved from the server
            decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_response = decrypt_cipher.decrypt(encrypted_response)
            unpadded_response = unpad(decrypted_response, AES.block_size)
            response = unpadded_response.decode()

            print(colored("Decrypted Response from server: ", "blue"), response)

            # close the connection
            s.close()
               
            # Time nterval for the update. For demonstration purposes it is set to 5 seconds
            time.sleep(5)

        except socket.error as e:
            print(f"Socket error occurred: {e}")

#Run the client           
run_client()

