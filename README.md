# *team-the-flowers*

## **The Flowers**

### - Filip Szpręgiel

### - Bartłomiej Szykuła

### - Piotr Targowski

### - Jakub Walczak

---

## **Challenge**

### Small UAV Navigation Concept

---

## **Solution**

### **FLORA Navigation System**

Our solution is based on inertial sensors data like from gyroscope, accelerometer, barometer or wind sensor. We have developed the complete **Compute Module** with *C++ low-code* implementation of software.

We also developed 3 concepts of using the module and designed simulation scenarios in order to visualize the expected results of operation - the effectiveness of navigation.

---

### **Compute Module**

The whole source code is stored in `./flora_nav/lib` directory.

The module consists of 2 submoduls:

- velocity estimator    `./flora_nav/lib/vel`
- position calculator   `./flora_nav/lib/pos`

Executable files of the both of modules in `./flora_nav/bin`.

#### **Velocity Estimator**

First of all, we have to estimate UAV's integrated linear velocity.
For this operation, inertial data from sensors are used:

- gyroscope
- accelerometer
- barometer
- compass
- wind sensor

Firstly we reduce sensors' signals noises with *Madgwick Filter* and calculate *pitch* and *roll* angles. This operation could be more precise if there was the magnetometer sensor.

Next, we *compensate the gravity acceleration influence* on accelerometer data and then we can estimate velocity value. There are calculation of component velocities by axies X, Y, Z and integration into *linear velocity* of UAV.

In the end we *reduce the wind influence* on previously estimated linear velocity with vector operations based on UAV velocity, wind speed and angle between these vectors.

After all, calculated velocity can be provided to next submodule in order to calculate actual UAV position.

---

#### **Position Calculator**

Initial GPS position of drone can be collected from GPS or inserted to a memory of on-board computer manually.
As well as it’s altitude. These data constitutes the initial coordinate system which is mathematicall interpretation
for the moving small UAV.

Translation matrix:

    T = | 1 | 0 | 0 | xt |
        | 0 | 1 | 0 | yt |
        | 0 | 0 | 1 | 0  |
        | 0 | 0 | 0 | 1  |

x<sub>t</sub> - value of latitude which you have to move the position of UAV on map after traveling for one second with given velocity.

y<sub>t</sub> - value of longtitude which you have to move the position of UAV on map after traveling for one second with given velocity.

Given the previous data the starting position of UAV will look like this:

    P = | xp |
        | yp |
        | 0  |
        | 1  |

Position of UAV after time interval will be calculated this way:

P<sub>current</sub> = P<sub>UAV</sub> x T

---

## **Scenarios**

We have prepared a simulation and visualization environment in order to simulate several scenarios of potential use of the module.

Simulator source code is store in `./flora_nav/navigator` directory.
Main file : `./flora_nav/flora_nav.py`

---

### **Offline Navigation**

UAV navigates with only inertial data from on-board sensors:

- Gyroscope
- Accelerometer
- Barometer
- Compass
- Wind Sensor

In this scenario there is no GPS signal during the mission. Operator has to insert initial GPS position data. The machine then relies entirely on module calculations.

---

### **Hybrid Navigation**

UAV tries to get actual position with GPS module at certain intervals and with a certain probability of obtaining a GPS signal at these times.

After very defined time interval the machine (if there is a GPS signal) can verify its position and make corrections for the next calculations.

---

---

### **\[ Friendly | Hostile ] Zone**

This scenario assumes that there is valid GPS signal at the begining of mission and can rely on its data. Nextly the signal could be lost | `Hostile Zone` | and UAV turns into **offline navigation** mode.

In the end of mission on the way back, when the UAV enter the | `Friendly Zone` | the GPS signal could be regained and it will be very helpfull during the landing operation.
