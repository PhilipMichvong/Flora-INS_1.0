import random

import navigator.conf.config as cfg
import navigator.sensors as sensors
import navigator.modules as modules

def randomize_gps_module_link_status(gps_off : bool) -> bool:
    if gps_off:
        return False
    
    if random.randint(0, 100) >= cfg.GPS_LINK_STATUS_POSSIBILITY_RATE:
        return False
    
    return True


class Navigator:
    def __init__(self, gps_off : bool = False, gps_check_interval : int = 1) -> None:
        # on-Board Sensors
        self._imu = sensors.imu.IMUSensor()
        self._nav = sensors.nav.NavSensor()
        self._win = sensors.win.WindSensor()
        
        # on-Board Modules
        self._gps = modules.gps.GPSModule()
        self._compute_module = modules.compute.ComputeModule()
    
        self._gps_off = gps_off
        self._gps_check_interval = gps_check_interval
    
        # Start Actual GPS position (latitude, longitude)
        self._act_pos = self._get_initial_gps_pos()
        
        self._imu.update()
        self._nav.update()
        self._win.update()
        self._gps.update()

        self._prev_alt = self._imu.get_altitude()
        self._vel = 0.0
        self._i = 0
        self._gps_shot = False
        self._tmp_gps_hold = 12
    
    def __del__(self) -> None:
        del self._compute_module
        

    def update(self, zone = False) -> None:
        # Sensors real time work simulation
        self._imu.update()
        self._nav.update()
        self._gps.update()
        self._win.update()
        
        # === GPS SCENARIOS HANDLE ===
        if zone:
            # UAV is in friendly zone [GPS : ONLINE]
            self._gps.link_status = True
            self._act_pos = self._gps.get_position()
            return
        else:
            # UAV is in hostile zone [GPS : OFFLINE]
            self._gps.link_status = False
            
        if self._i % (self._gps_check_interval * 100) == 0:
            self._gps_shot = True
        
        # Maintain gps signal to apropriate scenario's visualization
        if self._tmp_gps_hold < 12:
            self._gps.link_status = True
            self._tmp_gps_hold = self._tmp_gps_hold + 1
        else:
            # Try to establish GPS connection
            if self._gps_shot:
                self._gps.link_status = randomize_gps_module_link_status(self._gps_off)
                if self._gps.is_online():
                    self._act_pos = self._gps.get_position()
                    self._gps_shot = False
                    self._tmp_gps_hold = 0
                    self._i = self._i + 1
                    return
            else:
                self._gps.link_status = False

        # Get sensor data
        gyro_data = self._imu.get_gyro_data()
        acc_data = self._imu.get_acc_data()
        alt = self._imu.get_altitude()
        bearing = self._nav.get_bearing()
        wind_data = (self._win.get_wind_speed(), self._win.get_wind_direction())
        
        # Calculations
        #   * velocity
        calc_vel = self._compute_module.estimate_velocity(gyro_data=gyro_data, acc_data=acc_data, wind_data=wind_data, bearing=bearing, index=self._i)
        
        if calc_vel is not None:
            self._vel = calc_vel
            
        #   * GPS position
        pos = self._compute_module.calculate_position(prev_pos=self._act_pos, 
                                                      prev_alt=self._prev_alt, 
                                                      act_alt=alt, 
                                                      act_vel=self._vel, 
                                                      bearing=bearing, 
                                                      t=100)
        
        if pos is not None:
            self._act_pos = pos
            
        self._prev_alt = alt
        self._i = self._i + 1
    
    def get_actual_gps_position(self) -> (tuple[float]):
        return self._act_pos
    
    def get_gps_status(self) -> bool:
        return self._gps.is_online()

    def _get_initial_gps_pos(self) -> tuple[float]:
        while True:
            self._gps.link_status = randomize_gps_module_link_status(False)
            if self._gps.is_online():
                return self._gps.get_position()
