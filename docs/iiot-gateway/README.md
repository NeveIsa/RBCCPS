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
1. The IIOT gateway needs to have the following features -
  - A lightweight interface for IIOT end devices to publish and subscribe messages.
  - A persistent message queue to retain messages from end devices when connection to Smartcity middleware is lost. 


#### B.2 Details
![Details](details.jpg)

#### C. Libraries/Tools
- [Mosquitto MQTT Broker](https://mosquitto.org/)
- [paho-mqtt python MQTT Client](https://pypi.python.org/pypi/paho-mqtt/1.1)
- [Smartcity Middleware Python Client](https://github.com/NeveIsa/RBCCPS/tree/master/docs/middleware-client)
