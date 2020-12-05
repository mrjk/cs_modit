# Cities Skylines: Mod It!

This is a standalone web app to manage your Cities Skylines mods. It relies on a nifty web interface with powerful tagging facility. It maily relies on the ModList mod, that provides an easy way to load list of mods. 

So far, there is no good solutions to manage mods with Cities Skylines, either you use the impracticale game interface, either you use the even worst interface of the Steam Workshop. This tools is an attempt to 

## Project status

The project is under heavy development, use at your own risks.


## Usage

### Features

* Mirror Steam Workshop
* Allow to tag mods and organise them in playlists
* Allow to import and export modlists

## Internal Design

### Pony DB

https://editor.ponyorm.com/user/mrjk78/CsModIt/designer


### Other resources

https://github.com/Astavinu/WorkshopManager => OK ?
https://github.com/b1naryth1ef/steamy


### Interesting paths (Linux)

Autorepair management: ~/.local/share/Steam/steamapps/common/Cities_Skylines/Cities_Data/AutoRepair.log
ScreenLoader management: ~/.local/share/Colossal\ Order/Cities_Skylines/Report/LoadingScreenMod/*.htm
Savegames management: ~/.local/share/Colossal Order/Cities_Skylines/Saves/*.crp
CS runtime files: ~/.local/share/Steam/steamapps/common/Cities_Skylines/
System Workshop items: ~/.local/share/Steam/steamapps/workshop/content/255710/

Detect a way to see if modules are enabled ?


## Infos

Author: MrJK
License: GPLv3
Date: October 2020

