# felix schumacher - the official game
## installation
create a virtual environment and install all the necessary dependencies to run the game. 
the dependencies are listed in `requirements.txt` and can installed with pip. the rest of the game assets are found in `src/`.
````bash
python -m venv venv # create a virtual environment
source venv/bin/activate # activate the environment
pip install -r requirements.txt # install all dependencies
``````

## running the game
the main game can be started from the terminal by running:
````
python src/main.py

optional arguments:
  -h, --help       show this help message and exit
  --width WIDTH    change width of window (in pixels)
  --height HEIGHT  change height of window (in pixels)
  --small          play on small map (reduced loading time)
  --funny          play in funny mode (very hard)
````
make sure you went through the installation guide first and that the virtual environment you created is activated.

### how to play
use the keys on your keyboard to move and have fun! but be careful, too much alcohol changes your cognitive capabilities...

## further development
feel free to use, change and enhace!
you will notice that the game engine is pretty straightforward. everything you need to know is in `felix.py`.  
if you want to change the looks of the game, play around with the sprites and the sprite sizes.
the map is created by a simple pixel color to tile/sprite mapping, defined in `map.py`. you can find two sample maps in `src/sprites/maps/`, the `.pixil` files can be uploaded and edited on [pixilart.com](pixilart.com). make sure to use the correct colors or change the color mapping before you start to get creative!  
the game state is mainly handled from `alcoholism.py`, includes the counter and music.