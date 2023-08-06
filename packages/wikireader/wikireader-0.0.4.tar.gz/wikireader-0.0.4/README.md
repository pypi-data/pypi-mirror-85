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
Configuration is still in it's early stages. The first implementation is in
version 0.0.4. At the moment you can only set the theme.
The config folder is in `~/.config/wikireader/`. There will be a `config.json`.
If it is not there, run the wikireader command once. The program will create
the folder and the default config files. There will be a css folder as well
with availabel themes, at the moment only a dark- and a light theme. Be free to
create your own theme, but beware that you give it a different name.
In the config.json you can set the theme, by setting the css filename without
the `.css` extentsion:
``` json
{
    "theme": "light"
}
```
The default is dark as I prefer that.

## Licence
The package is released under MIT license.

