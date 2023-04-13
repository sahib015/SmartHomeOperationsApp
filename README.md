# SmartHomeOperationsApp
## Readme- Secure Software Development Assessment- Code 

## Introduction
The main threat in IoT smart homes, is due to the distributed nature of the system, and the connectivity between processes and devices. The connectivity can be unreliable and open to attack (Taivalsaari et al, 2018).
    
**Hypothesis: How to secure the connectivity between processes in a distributed IoT smart home to prevent attacks such as injection attacks, message modification, man-in-the-middle attacks and DoS attacks.**
    
## Usage Instructions 
### **How to run the system**
### **Run the Server**
Using a terminal, navigate to the server folder, and start the virtual environment on your preferred computer.
* “SmartHomeOperationsApp-Windows/server” 
* “SmartHomeOperationsApp-Mac/server” 
 
The virtual environments are created and can be activated using the commands.
* Type “Scripts\activate” – Windows 
* Type “source bin/activate” – Mac 

Once the virtual environment is activated install the following libraries (note this needs to be installed on both virtual environments (server and sensor)
* Pycryptodome – pip install pycryptodome
* Termcolor – pip install termcolor

After the libraries have been installed, run the server application using the following commands. The server should start running before running the different sensors.
* Type “python server.py”
* Type “python3 server.py” if having multiple versions of python. 

### Run the Different Sensors
 Using a new terminal, navigate to the sensor folder, and start the virtual environment on the same computer running server.py. 
 * “SmartHomeOperationsApp-Windows/sensor” 
 * “SmartHomeOperationsApp-Mac/sensor” 
 
Ensure the libraries have been installed- refer to the libraries above to install on the sensor virtual environment. 

After the libraries have been installed run the sensor application using the following commands.
* Type “python reg_sensor.py”, python unknown_sensor.py” and python unknown_sensor.py”
* Type “python3 reg_sensor.py”, python3 ureg_sensor.py” and python3 unknown_sensor.py” if having multiple versions of python
## Identified Vulnerabilities with Mitigations
IoT devices are vulnerable to a cyber-attack, and an attacker may fabricate, intercept, manipulate or interrupt transmitted data (Addullah et al, 2019).
The main security risks can be mitigated by encryption, and should be at the core of IoT (Abdullah et al, 2019). 
Addressing vulnerabilities of identity theft, man-in-the-middle attacks and distributed denial of service attacks, the application has implemented the following mitigations - 
* Message Encryption - Data being transmitted is secure.
* SSL/TLS Communication – Using Certificates, secures the connection between the client and the server to avoid data tampering. 
* The server authenticates by sensor type and sensor ID - This ensures registered sensors get a valid response from the server and that the data remains secure
* The server verifies the size of the packet payload and checks whether it is valid or empty. 
* The implementation of multithreading helps prevent session jamming attacks and allows multiple valid simultaneous connections. This improves the application's performance, reliability, and resilience to denial-of-service attacks.

**By implementing these mitigations, we were able to address the vulnerabilities that were posed in our hypothesis.**

## Programming Principles
* Object-Oriented Programming - Local variables within functions support information hiding and encapsulation.  Python modules and functions have also been leveraged, to promote re-use of code. 
* Software Version Control has been implemented.
* Code includes comments.

## Proposed scope for next SPRINT
The following mitigations should be considered for inclusion in the next SPRINT.
* Additional authentication including certificates and passwords between the IoT devices and Server
* Use of random ports for communication
* A regular process which checks for firmware updates ensuring the latest security patches are deployed. 

## Design Considerations
We should remain mindful, that this system is more likely to be implemented in people’s homes, rather than an Enterprise with dedicated IT Staff and corresponding skillset. The complexity of any design must take this into consideration as demonstrated by Figure 1.

![Security_Triangle](/Security_Triangle.png "Figure 1.Security, Functionality and Useability Triangle")
**Figure 1-** Security, Functionality and Useability Triangle
## References
