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
#@return- temp
def get_temperature():
    while True:
        try:
            temp = random.randint(1,40) #random temperature values between 1 and 40
            return temp
        except ValueError:
            print("Invalid temperature value. Please try again.")

#
# Method to return the humidity value from the sensor to the server
#The value is generated randomly using the random library
# @return- humidity    
       
def getHumidity():
    while True:
        try:
            humidity = random.randint(1,100) #random humidity % values between 1 and 100
            return humidity
        except ValueError:
            print("Invalid humidity value. Please try again.")


#Method defining the client ie temperature and humidity sensor that is registered to the server
def run_client():
    while True:
        try:
            # sensor information

            sensor_type = "known_sensor"
        
            temperature = get_temperature()
            humidity = getHumidity()
        
            tempHumidSensor_data = {
                "sensor_type": sensor_type,
                "sensor_name": "temperatureHumidity_sensor",
                "sensor_tempValue": temperature,
                "sensor_humidityValue": humidity,
                "sensor_unit": "Celsius and %",
                "sensor_id": "abc123" 
            }
    
            # store the sensor data to JSON format
            sensor_json = json.dumps(tempHumidSensor_data)
        
            print(colored("Sensor data to server: ","blue"), "Data:", sensor_json)
    
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
            print(colored("Encrypted sensor data sent: ", "blue"), "Data:", encrypted_data)

            # receive the response from the server
            encrypted_response = s.recv(1024)
            print(colored("Received encrypted server response: ", "blue"), "Response:", encrypted_response)
    
            # create a new AES cipher object for decrypting the response data and recode the encrypted data recieved from the server
            decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
            decrypted_response = decrypt_cipher.decrypt(encrypted_response)
            unpadded_response = unpad(decrypted_response, AES.block_size)
            response = unpadded_response.decode()
    
            print(colored("Decrypted Response from server: ", "blue"), "Response:", response)
            
            # Time nterval for the update. For demonstration purposes it is set to 5 seconds
            time.sleep(5)

        
        except socket.error as e:
            print(f"Socket error occurred: {e}")

# Run the client sensor       
if __name__ == '__main__':
   
        
    # Set DSCP Value = AF41
    DSCP = 0x90

    # create a socket object and set the TOS marking for the socket
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
    #Open connection
    s.connect((host, port))
    print(colored("Connected to server", "blue"), host, "port",port,".")
        
    run_client()
        
    # close the connection
    s.close()
    print(colored("Disconnected from server", "blue"), host, "port", port, ".")
    


