import tkinter
from tkintermapview import TkinterMapView

ORG_DATAFILE = './data/test_set/out/data_org.txt'
CAL_DATAFILE = './data/calc/pos.txt'
SATELITE_MAP_VISUALIZER = False


def desktop_init() -> None:
    global root_tk, map_widget
    
    root_tk = tkinter.Tk()
    root_tk.geometry(f"500x500")
    root_tk.title("UAV Flight Track Visualizer")

    map_widget = TkinterMapView(
        root_tk, width=600, height=400, corner_radius=0)

    map_widget.pack(fill="both", expand="true")
    
    if SATELITE_MAP_VISUALIZER:
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=18)

def load_gps_data(data_file_name: str) -> list:
    my_file = open(data_file_name, 'r')
    data = my_file.readlines()
    return data[::10]

def draw_track(data : list[str], line_color : str, line_width : str) -> None:
    map_widget.set_address(f"{data[0]}", marker=False)
    cal_start_point_x, cal_start_point_y = float(data[0].split(
        ', ')[0]), float(data[0].split(', ')[1])

    for i, row in enumerate(data):
        try:
            cal_x, cal_y = float(row.split(', ')[0]), float(row.split(', ')[1])

            uv_path = map_widget.set_path([(cal_start_point_x, cal_start_point_y), (cal_x, cal_y)
                                           ], color=line_color, width=line_width)
            uv_path.add_position(cal_x, cal_y)
            cal_start_point_x = cal_x
            cal_start_point_y = cal_y
            
        except ValueError:
            pass


def main() -> None:
    # ===== Desktop App Init =====
    print('App init... ', end='\t\t')
    desktop_init()
    print('Done.')

    # ===== GPS points data load =====
    print('Data loading... ', end='\t')
    cal_data = load_gps_data(CAL_DATAFILE)
    org_data = load_gps_data(ORG_DATAFILE)
    print('Done.')
    
    # ===== Tracks drawing =====
    print('Tracks drawing... ', end='\t')
    draw_track(cal_data, "blue", "8")
    draw_track(org_data, "red", "4")
    print('Done.')

    # ===== App Run =====
    print('\nApp is started.')
    root_tk.mainloop()


if __name__ == "__main__":
    main()

