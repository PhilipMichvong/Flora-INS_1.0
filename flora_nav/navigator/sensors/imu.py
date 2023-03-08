import csv
import navigator.conf.config as cfg

class IMUSensor:
    def __init__(self) -> None:
        self._gyro_data = self._load_csv_data(cfg.IMU_GYRO_FILE)
        self._acc_data  = self._load_csv_data(cfg.IMU_ACC_FILE)
        self._alt_data  = self._load_csv_data(cfg.IMU_ALT_FILE)
        self._marker = 5000
        
        self._gyro = {'x' : 0.0, 'y' : 0.0, 'z' : 0.0}
        self._acc = {'x' : 0.0, 'y' : 0.0, 'z' : 0.0}
        self._alt = 0.0
        
        self.update()
        
    # *** Getters ***
    # Returns IMU gyroscope data as dictionary with keys ['x', 'y', 'z']
    def get_gyro_data(self) -> dict:
        return self._gyro
    
    # Returns IMU accelerometer data as dictionary with keys ['x', 'y', 'z']
    def get_acc_data(self) -> dict:
        return self._acc
    
    # Returns IMU calculated altitude as float value
    def get_altitude(self) -> float:
        return self._alt
    
    # *** Measurements update ***
    def update(self):
        self._gyro['x'] = float(self._gyro_data[self._marker][1])
        self._gyro['y'] = float(self._gyro_data[self._marker][2])
        self._gyro['z'] = float(self._gyro_data[self._marker][3])
        
        self._acc['x'] = float(self._acc_data[self._marker][1])
        self._acc['y'] = float(self._acc_data[self._marker][2])
        self._acc['z'] = float(self._acc_data[self._marker][3])
        
        alt = float(self._alt_data[self._marker][1])
        if alt < 0:
            self._alt = 0
        else:
            self._alt = alt 
        
        self._marker = self._marker + 1

    def _load_csv_data(self, filepath : str):
        rows = [] 
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(list(row.values()))
        return rows