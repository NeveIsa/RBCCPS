### Python Library for accessing SmartCity middleware

#### Some basics

- A *device* can be broadly classified into 3 types: sensors,actuators,applications.
- *Sensors* publish data to the middleware, *actuators* subscribe to data from middleware and *applications* can both publish and subscribe.
- A device is recognised by a *resource_id*, eg: iiot_light_sensor_101.


#### Examples
##### 1. Creating a new Device

```python

import smartcity as scity

# pass a resource_id(must be string) and a device_type(sensor,actuator,application[default])
mydevice=scity.Device("spider_sense","sensor")

# Prompts for confirmation, etc.

```

##### 2. Publishing from a device

```python

import smartcity as scity

#pass the resource_id
mydevice=scity.Device("spidey_sense")

#pass the data to publish(must be string)
mydevice.pub("I sense danger, spider senses activated")

```
 
