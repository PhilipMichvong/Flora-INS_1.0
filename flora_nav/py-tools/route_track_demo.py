import sys
import tkinter as tk
import tkintermapview as tkmap

ORG_COLOR = "red"
ORG_WIDTH = "3"

CAL_COLOR_GPS_STATUS = {
    0 : "blue",
    1 : "green"
}
CAL_WIDTH_GPS_STATUS = {
    0 : "4",
    1 : "6"
}

SATELITE_MAP_VISUALIZER = False
ANIM_DELAY = 100  # [ms]

def desktop_init() -> None:
    global root_tk, map_widget
    
    root_tk = tk.Tk()
    root_tk.geometry(f"500x500")
    root_tk.title("UAV Flight Track Visualizer")

    map_widget = tkmap.TkinterMapView(
        root_tk, width=600, height=400, corner_radius=0)

    map_widget.pack(fill="both", expand="true")
    
    if SATELITE_MAP_VISUALIZER:
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=13)

def load_gps_data(data_file_name: str) -> list:
    my_file = open(data_file_name, 'r')
    data = my_file.readlines()
    return data[::10]


def animation_org_data_step():
    global oind, oindflag
    try:
        if not oindflag:
            try:
                start_coords = org_data_list[oind]
                end_coords = org_data_list[oind + 1]
                
                print(f'ORG: {end_coords}')
                map_widget.set_path([start_coords, end_coords], color=ORG_COLOR, width=ORG_WIDTH)
                oind = oind + 1
                root_tk.update()
                
            except NameError:
                oind = 0
                oindflag = False
                
                start_coords = org_data_list[oind]
                end_coords = org_data_list[oind + 1]
                
                print(f'ORG: {end_coords}')
                map_widget.set_path([start_coords, end_coords], color=ORG_COLOR, width=ORG_WIDTH)
                oind = oind + 1
                root_tk.update()
                
            except IndexError:
                print("ORG: End of Data")
                oindflag = True
                
    except NameError:
        oindflag = False
    
def animation_cal_data_step():
    global cind, cindflag
    try:
        if not cindflag:
            try:
                start_coords = (cal_data_list[cind][0], cal_data_list[cind][1])
                end_coords = (cal_data_list[cind + 1][0], cal_data_list[cind + 1][1])
                gps_status = cal_data_list[cind + 1][2]
                color = CAL_COLOR_GPS_STATUS[cal_data_list[cind + 1][2]]
                width = CAL_WIDTH_GPS_STATUS[gps_status]
                
                print(f'CAL: {end_coords} : {gps_status}')
                map_widget.set_path([start_coords, end_coords], color=color, width=width)
                cind = cind + 1
                root_tk.update()
                
            except NameError as e:
                cind = 0
                cindflag = False
                
                start_coords = (cal_data_list[cind][0], cal_data_list[cind][1])
                end_coords = (cal_data_list[cind + 1][0], cal_data_list[cind + 1][1])
                gps_status = cal_data_list[cind + 1][2]
                color = CAL_COLOR_GPS_STATUS[gps_status]
                width = CAL_WIDTH_GPS_STATUS[gps_status]
                
                print(f'CAL: {end_coords} : {gps_status}')
                map_widget.set_path([start_coords, end_coords], color=color, width=width)
                cind = cind + 1
                root_tk.update()
                
            except IndexError:
                print("CAL: End of Data")
                cindflag = True
                
    except NameError:
        cindflag = False


def main() -> None:
    # ===== Pos args parse =====
    if len(sys.argv) != 3:
        print('Bad usage!')
        print(f'python3 {sys.argv[0]} <<path/to/calc_pos.txt>> <<path/to/org_pos.txt>>')
        sys.exit(1)
        
    cal_datafile = sys.argv[1]
    org_datafile = sys.argv[2]
    
    # ===== Desktop App Init =====
    print('App init... ', end='\t\t')
    desktop_init()
    print('Done.')

    # ===== GPS points data load =====
    print('Data loading... ', end='\t')
    cal_data = load_gps_data(cal_datafile)
    org_data = load_gps_data(org_datafile)
    print('Done.')
    
    # ===== Routes animation preparation =====

    global org_data_list, cal_data_list
    org_data_list = []
    cal_data_list = []
    
    # *** Real GPS Data ***
    for i, row in enumerate(org_data):
        row = row.split(", ")
        x, y = float(row[0]), float(row[1])
        org_data_list.append((x, y))
        root_tk.createtimerhandler((i + 1) * ANIM_DELAY + 10000, animation_org_data_step)
        
    # *** Calculated GPS Data ***
    for i, row in enumerate(cal_data):
        row = row.split(", ")
        x, y, gps_status = float(row[0]), float(row[1]), int(row[2])
        cal_data_list.append((x, y, gps_status))
        root_tk.createtimerhandler(((i + 1) * ANIM_DELAY) + 10005, animation_cal_data_step)
    
    map_widget.set_position(48.558600, 35.119128)
    
    # ===== App Run =====
    print('\nApp is started.')
    root_tk.mainloop()


if __name__ == "__main__":
    main()