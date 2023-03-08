import subprocess
import navigator.conf.config as cfg

class ComputeModule:
    def __init__(self) -> None:
        self.vel_prg = cfg.CALC_VEL_PRG # Velocity calculation program path
        self.pos_prg = cfg.CALC_POS_PRG # Position calculation program path
        
        # Logfiles (for STDERR from cpp programs)
        self.vel_log = open(cfg.CALC_VEL_LOG, 'w') # Velocity calc program logfile
        self.pos_log = open(cfg.CALC_POS_LOG, 'w') # Position calc program logfile

        # CSV logfiles
        self.vel_csv_log = open(cfg.CALC_VEL_CSV_LOG, 'w')          # calculated velocity (step, velX, velY, velZ, vel)
        self.acc_csv_log = open(cfg.CALC_ACC_CSV_LOG, 'w')          # raw accelerometer data (accX, accY, accZ)
        self.acc_cmp_csv_log = open(cfg.CALC_ACC_CMP_CSV_LOG, 'w')  # compensated accelerometer data (accCmpX, accCmpY, accCmpZ)
        
        # CSV logfiles headers init
        self.vel_csv_log.write('t,velX,velY,velZ,velAir,vel\n')
        self.acc_csv_log.write('t,accX,accY,accZ\n')
        self.acc_cmp_csv_log.write('t,accCmpX,accCmpY,accCmpZ\n')
        
        # cpp programs args to being maintained and updated
        self.q = [1.0, 0.0, 0.0, 0.0]   # velocity calculate: Madgwick filter quaterions
        self.vel = 0                    # velocity calculate: previous integrated velocity
    
    def __del__(self) -> None:
        # Logfiles close
        self.vel_log.close()
        self.pos_log.close()
        self.vel_csv_log.close()
        self.acc_csv_log.close()
        self.acc_cmp_csv_log.close()
    
    
    '''
     Estimate UAV velocity with IMU data
        Returns estimated actual velocity value as a float value on success or None on errors
    '''
    def estimate_velocity(self, gyro_data : dict, acc_data : dict, wind_data : tuple, bearing : float, index : int) -> float | None:
        # Build program arguments
        args =  [   str(gyro_data["x"]),
                    str(gyro_data["y"]),
                    str(gyro_data["z"]),
                    str(acc_data["x"]),
                    str(acc_data["y"]),
                    str(acc_data["z"]),
                    str(self.q[0]),
                    str(self.q[1]),
                    str(self.q[2]),
                    str(self.q[3]),
                    str(wind_data[0]),
                    str(wind_data[1]),
                    str(bearing)
                ]
        # Build command
        cmd = [self.vel_prg] + args
        
        # Execute calculation program 
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Save stderr stream to logfile
        self.vel_log.write(f'{result.stderr.decode("utf-8")}')
        
        # Save raw acceleration to csv logfile
        self.acc_csv_log.write(f'{index},{acc_data["x"]},{acc_data["y"]},{acc_data["z"]}\n')
        
        if result.returncode == 0:
            res = result.stdout.decode('utf-8').split(',')
            
            accCmpX, accCmpY, accCmpZ = float(res[0]), float(res[1]), float(res[2])
            self.q[0] = float(res[3])
            self.q[1] = float(res[4])
            self.q[2] = float(res[5])
            self.q[3] = float(res[6])
            
            velx, vely, velz = float(res[7]), float(res[8]), float(res[9])
            airvel = float(res[10])
            self.vel = float(res[11])
            
            self.acc_cmp_csv_log.write(f'{index},{accCmpX},{accCmpY},{accCmpZ}\n')
            self.vel_csv_log.write(f'{index},{velx},{vely},{velz},{airvel},{self.vel}\n')
            
            # print(f'{result.returncode} : {res}')
            
            return self.vel
        
        # print(f'{result.returncode} : FAILURE!')
        
        return None
    
    '''
     Calculate UAV GPS position with input data
     params:
      - previous GPS position (lattitude, longitude)
      - previous altitude [m]
      - actual altitude [m]
      - actual velocity [m/s]
      - UAV bearing [degrees]
      - time [ms]
     Returns calculated UAV GPS position as tuple : (lattitude, longitude) on success or None on errors
    '''
    def calculate_position(self, prev_pos : tuple, prev_alt : float, act_alt : float, act_vel : float, bearing : float, t : float) -> tuple[float] | None:
        # Build program arguments
        args =  [   str(prev_pos[0]),
                    str(prev_pos[1]), 
                    str(prev_alt), 
                    str(act_alt), 
                    str(act_vel), 
                    str(bearing), 
                    str(t)
                ]
        # Build command
        cmd = [self.pos_prg] + args
        
        # Execute calculation program 
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Save stderr stream to log file
        self.pos_log.write(f'{result.stderr.decode("utf-8")}')
        
        # If Success
        if result.returncode == 0:
            # Collect calculated result
            res = result.stdout.decode('utf-8').split(',')
            lat, lon = float(res[0]), float(res[1])
            return (lat, lon)
        
        return None
