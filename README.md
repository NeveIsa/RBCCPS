### Python Library for accessing SmartCity middleware

#### Some basics

- A device can be broadly classified into 3 types: sensors,actuators,applications.
- 'Sensors' publish data to the middleware, 'actuators' subscribes to data from middleware and 'applications' can both publish and subscribe.
- A device is recognised by a 'resource_id', eg: iiot_light_sensor_101.


#### EXAMPLES

##### Create a new Device

```python

import smartcity as scity

# pass a resource_id
mydevice=scity.Device("my_resource_id")

# Prompts for confirmation, etc.

```

 
