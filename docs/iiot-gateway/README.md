## <p style="color:gray"> IIOT GATEWAY </p>


 
### Contents
**A. Terminology Reference**
**B. Architecture**
**C. Libraries/Tools**
**D. Examples**

#### A. Terminology Reference

#### A.1 Key entities
- Analytics Application 
- Middleware 
- Devices {IIOT gateway devices, IIOT end devices}

#### A.2 Overview
![Overview](overview.jpg)

---

#### B. Architecture
#### B.1 Layout
** The IIOT gateway needs to have the following features**
  - A lightweight interface for IIOT end devices to publish and subscribe messages
  - A persistent message queue to retain messages from end devices when connection to Smartcity middleware is lost. 
 
** Selection of an interface between gateway and the end devices**
  - Considering the above two, MQTT is a very strong candidate which provides a PUB-SUB architecture and  a message queue out of the box.
  - Mosquitto is an open source MQTT Broker that is supported by Raspberry Pi.
  - paho-mqtt is an open source MQTT Client python library.
  
  ** Important MQTT related details **
   - MQTT stands for Message Queue Telemetry Transport
   - Uses TCP as the transport layer with a lightweight application level binary protocol (Headers are binary instead of ascii text - unlike HTTP) 
   - Provides sessions and message queues using ClientID parameter for messages with QoS > 0.
#### B.2 Details
![Details](details.jpg)

#### C. Libraries/Tools
- [Mosquitto MQTT Broker](https://mosquitto.org/)
- [paho-mqtt python MQTT Client](https://pypi.python.org/pypi/paho-mqtt/1.1)
- [Smartcity Middleware Python Client](https://github.com/NeveIsa/RBCCPS/tree/master/docs/middleware-client)
