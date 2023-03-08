import gmplot
from selenium import webdriver
from time import sleep
import pathlib
from datetime import datetime
from PIL import Image
import os

gmap = gmplot.GoogleMapPlotter


def show_satelitar_map(lat: float, lng: float, zoom: int, map_type: int, apikey: str, file_name: str) -> None:

    latitude_list = [lat]

    longitude_list = [lng]

    if apikey == '':
        try:
            with open('apikey.txt', 'r') as apifile:
                apikey = apifile.readline()
        except FileExistsError:
            pass

    gmap = gmplot.GoogleMapPlotter(latitude_list[0],
                                   longitude_list[0], 20, map_type=map_type, apikey=apikey)

    gmap.draw(f"{str(file_name)}")


def screenshoot(file_name: str) -> None:
    sonar_path = pathlib.Path.absolute(
        pathlib.Path(f'.//{file_name}'))

    if os.path.exists(sonar_path) == True:
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.get(str(sonar_path))
        print(sonar_path)
        sleep(1.5)

        ATM = datetime.now().strftime("%H-%M-%S")
        # print(ATM)
        driver.save_screenshot(f"{ATM}_photo.png")
        driver.quit()
        Image.open(f"{ATM}_photo.png")
    else:
        print("check path of .html file")


if __name__ == "__main__":
    show_satelitar_map(lat=52.230951, lng=21.004316, zoom=20,
                       map_type="satellite", apikey='', file_name="mapy.html")

    screenshoot(file_name="mapy.html")
