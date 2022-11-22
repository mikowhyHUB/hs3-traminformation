# Tram Information for Hackespace Trójmiasto
Real-time tracking of nearest trams next to headquarters of [Hackerspace Trójmiasto](https://github.com/hs3city) located in Gdańsk, Poland. 
The project was written to be finally displayed on matrix monitors. The script takes data from the two closest stops going in two different directions of the city.

The data is pulled from the official Open Data API located here:
https://ckan.multimediagdansk.pl/dataset/tristar/resource/00fbcffa-5188-45be-b300-b4da9a91c24f

## Features
- Gets live data from ckan.multimediagdansk.pl
- Shows live data 
- Shows train emoji when the time is under 1 minute
- Refreshes every n seconds for its owns 
- Shows n lines of coming trams
- Configurable station

## Instructions
1. Open this project in PlatformIO
2. Run "pip3 install requirements.txt" command
3. You can set other stops in Tricity with(Default stops are: Zajezdnia 01 and Zajezdnia 02):
- Choose the stop you want to be displayed('stopId') in [List of stops](https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json)
- Replace stopId with the one you choose in def main() -> url1 or 2 -> 'https://ckan2...stopId=XXXX'
4. Start the "main.py" file. (Works on Python 3.10.7)
5. You will see an output while it works. The output refreshes on its own every 20sec(You can change it in the code execution)
6. To stop script, just press control + z 


## Todo
- Add colors to the tram numbers
- Add the option to show scheduled data if live data is not available
- Add an apostrophe next to the minute

## Contribution

Big thanks to [DoomHammer](https://github.com/DoomHammer) for the chance to do this project.




### If you have any questions, feel free to contact me :)
