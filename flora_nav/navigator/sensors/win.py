import csv
import navigator.conf.config as cfg

class WindSensor:
    def __init__(self) -> None:
        self._data = self._load_csv_data(cfg.WIN_DATA_FILE)

        self._speed = 0.0
        self._direction = 0.0
        
        self._marker = 4970
        
        self.update()
    
    # *** Getters ***
    # Returns wind speed in knots
    def get_wind_speed(self) -> float:
        return self._speed
    
    # Returns wind direction in degrees
    def get_wind_direction(self) -> float:
        return self._direction
    
    # *** Measurements update ***
    def update(self):
        self._direction = float(self._data[self._marker][1])
        self._speed = float(self._data[self._marker][2])
        self._marker = self._marker + 1

        
    def _load_csv_data(self, filepath : str):
        rows = [] 
        with open(filepath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(list(row.values()))
        return rows