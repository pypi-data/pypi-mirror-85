# WikiReader
**WikiReader** is a simple wikipedia browser tool writen in Python for reading Wikipedia
articles without distraction. It uses Suckless' dmenu for finding articles.


*It is written for my own purposes and is deliberately kept simple.*


## Installation
To install WikiReader, simply run:
``` bash
pip install wikireader
```
WikiReader was written in Python 3.8.5 and had dmenu as an external dependency.
To install dmenu:

On Debian/Ubuntu
``` bash
sudo apt install dmenu
```
On Arch Linux:
``` bash
pacman -S dmenu
```
WikiReader also relies on PyQt5, so it needs the dependencies of that package as well.

## Usage
Run the command `wikireader`. A dmenu instance will popup on your screen. Here you can write a 
keyword or query. The dmenu will disappear and reappear with suggestions to articles. After
chosing one, the article will be loaded and shown in a simplified html form.

## Config
Configuration is not implemented yet. However the appearance of the text can be modified by
css. This file is created after the first run of the program at `~/.config/wikireader/layout.css`.
If you mess it up, you can just delete the file and it will be recreated after rerunning WikiReader.

## Licence
The package is released under MIT license.

