import sys

import navigator.conf.config as cfg
from navigator.navigator import Navigator

def init(gps_off : bool) -> None:
    global navigator, zone
    
    if cfg.GPS_SCENARIO_ZONE:
        zone = True
    else:
        zone = False
    
    print('Navigator module : \t\tInit...')
    navigator = Navigator(gps_off, cfg.GPS_CHECK_INTERVAL)
    print('  * Navigator module : \t\tOK')

def main() -> None:
    # GPS position logfile to future track visualization
    print('GPS position logfile : \t\tInit...')
    pos_logfile = open(cfg.CALC_POS_CSV, 'w')
    
    # GPS position (latitude, longitude)
    position = navigator.get_actual_gps_position()
    pos_logfile.write(f'{position[0]}, {position[1]}, {1}\n')
    print('  * GPS position logfile : \tOK\n')
    
    str_ind = 4999      # start log sample index [!CONST!]
    stp_ind = 13500     # stop  log sample index [MAX: about 14000]
    i = str_ind
    percent = round((((i - str_ind) / (stp_ind - str_ind)) * 100), 2)
    
    print('UAV log data is being processed:')
    while True:
        if cfg.GPS_SCENARIO_ZONE:
            if percent < 20 or percent > 80:
                zone = True
            else:
                zone = False
            navigator.update(zone=zone)
        else:
            navigator.update()
        
        position = navigator.get_actual_gps_position()
        gps_status = navigator.get_gps_status()
        
        pos_logfile.write(f'{position[0]}, {position[1]}, {int(gps_status)}\n')
        
        i = i + 1
        if i >= stp_ind:
            break
        
        percent = round((((i - str_ind) / (stp_ind - str_ind)) * 100), 2)
        print(f'  * Processing:  100 / {percent} %  ', end='\r')
        
    print('  * Processing:  100 / 100 %   ')

def clean() -> None:
    print('\nCleaning...')
    try:
        del navigator
    except KeyboardInterrupt:
        pass
    print('  * Cleaned.\n')

if __name__ == '__main__':
    print('*** FLORA NAVIGATION SYSTEM ***'.center(50))
    print('** SIMULATION **'.center(50))
    print('\n  SCENARIO: ', end='')
    
    if cfg.GPS_SCENARIO_OFFLINE:
        print('Offline Navigation\n')
        print('               Description:')
        print('                 UAV navigates with only inertial data')
        print('                  from on-board sensors:')
        print('                     * Gyroscope')
        print('                     * Accelerometer')
        print('                     * Barometer')
        print('                     * Compass')
        print('                     * Wind Sensor')
        print('\n' + 54 * '=' + '\n')
        init(gps_off=True)
        
    elif cfg.GPS_SCENARIO_ZONE:
        print('[ Friendly | Hostile ] Zones\n')
        print('               Description:')
        print('                 * Friendly Zone : GPS signal is being obtained ')
        print('                                    at the beginning of flight')
        print('                                    and at the end.')
        print('                 * Hostile  Zone : Meanwhile there is no GPS connection.')
        print('\n' + 54 * '=' + '\n')
        init(gps_off=True)
    
    elif  cfg.GPS_SCENARIO_HYBRID:
        print('Hybrid Navigation\n')
        print('               Description:')
        print('                 UAV tries to get actual position with GPS module')
        print('                  at certain intervals and with a certain probability')
        print('                  of obtaining a GPS signal at these times.')
        print('               Conditions:')
        print(f'                * time interval:   {cfg.GPS_CHECK_INTERVAL} s')
        print(f'                * probability:     {cfg.GPS_LINK_STATUS_POSSIBILITY_RATE * 100}%')
        print('\n' + 54 * '=' + '\n')
        init(gps_off=False)
        
    else:
        print('No scenario was chosen. Check the config file.')
        sys.exit(1)
    
    try:
        main()
        
    except KeyboardInterrupt:
        clean()
        print('-- Manually Interrupted --\n')
        print('Simulation program ended up with Success.\n')
        sys.exit(0)
        
    except Exception as e:
        clean()
        print('-- Unexpected Exception --')
        print(type(e).__name__)
        print(e, end='\n\n')
        print('Simulation program ended up with Failure!\n')
        sys.exit(1)
        
    clean()
    print('Simulation program ended up with Success.\n')
    sys.exit(0)
