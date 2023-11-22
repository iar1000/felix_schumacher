# felix schumacher - the official game
## installation
### mac
create a virtual environment in the top level folder and install all the necessary dependencies into it to run the game. 
the dependencies are listed in `requirements.txt` and can installed with pip. the rest of the game assets are found in `src/`.
````bash
python -m venv venv # create a virtual environment
``````
the directory structure should look like this now:
```bash
felix_schumacher
|-- src/
|-- venv/
|-- requirements.txt
|-- .gitignore
|-- README.md
```
after creating the virtual environment, activate it and install the dependencies:
````bash
source venv/bin/activate # activate the environment
pip install -r requirements.txt # install all dependencies
``````
### windows
for the setup of the virtual environment use the internet, for example [the following tutorial on how to setup a venv on linux and windows](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/).
the installation of the requirements is the same.
a common issue on windows is [the virtualenv not activating](https://stackoverflow.com/questions/18713086/virtualenv-wont-activate-on-windows).

## running the game
the main game can be started in the terminal by running following from the top-level directory:
````
python src/main.py

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    change width of window (in pixels)
  --height HEIGHT  change height of window (in pixels)
  --small          play on small map (reduced loading time)
  --funny          play in funny mode (very hard)
````
you can change some game variables via command line. for example, if you want to have a different screen size, let's say 900x600, you can do this by running:
````
python src/main.py --width 900 --height 600
````
note that `--small` and `--funny` don't need an additional arguments, the can be set as flags (true if set, false if not set).

### how to play
use the keys on your keyboard to move and have fun! but be careful, too much alcohol changes your cognitive capabilities...

### troubleshooting
make sure you went through the installation guide first and everything is setup properly. if you did and it still doesn't work, ask ChatGPT. last resort is to message me.

## further development
feel free to use, change and enhace!
you will notice that the game engine is pretty straightforward. everything you need to know is in `felix.py`.  
if you want to change the looks of the game, play around with the sprites and the sprite sizes.
the map is created by a simple pixel color to tile/sprite mapping, defined in `map.py`. you can find two sample maps in `src/sprites/maps/`, the `.pixil` files can be uploaded and edited on [pixilart.com](pixilart.com). make sure to use the correct colors or change the color mapping before you start to get creative!  
the game state is mainly handled from `alcoholism.py`, includes the counter and music.
