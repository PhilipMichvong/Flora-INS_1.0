# Instalation

pip upgrade

    python -m pip install --upgrade pip

download github repo

    git clone https://github.com/tidehackathon/team-the-flowers

Change dir to api workdir

    cd ./team-the-flowers

install virtual enviroment python module

    python -m pip install virtualenv

create virtual enviroment for API

    python -m venv ./.venv

activate venv

    ./.venv/Scripts/activate

install required modules

    python -m pip install -r ./requirements

Run scripts

    python {script_name}.py

## **Documentation**

## satellite_photos.py

Arguments:

- Lattitude
- Longtitude
- Map type
- Zoom of map
- API key to Google maps(free 200$ every month)
- Name of output map file

Using Google maps API program saves map of given coordinates to HTML file. Which is opened by selenium library tools to make screenshot.

## similarity_tests.py

Script makes two test of similarity between the real life drone photo with satelitar view of the same coordinates. It uses flann base method which compares these two photos in terms of size channels and identical pixels. The disadvantage of this test is the angle of photos. Test number two is the solution. By designating differences between grayed images it presents percentage of error between the two photos and the errors are shown in separate window. Both test use machine learning and AI.

## google_map_display.py

It collects data sent by .cpp script and interprets position of drone by GPS data and the data calculated by the .cpp script. Presentation is on selected by user type of map. It gives user whole control over the map(zooming moving in all axes). Map doesn’t require API key to work.
