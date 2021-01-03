# Cities Skylines: Mod It!

This is a standalone web app to manage your Cities Skylines mods. It relies on a nifty web interface with powerful tagging facility. It mainly relies on the ModList mod, that provides an easy way to load list of mods. 

So far, there is no good solutions to manage mods with Cities Skylines, either you use the impracticale game interface, either you use the even worst interface of the Steam Workshop. This tools is an attempt to solve this issue.


### Project status

The project is under heavy development, use at your own risks. The base source code is not stable at all and may need heavy rework. Any help is appreciated.


### Features

* Mirror Steam Workshop
* Allow to tag mods and organise them in playlists
* Allow to import and export modlists


## Quickstart

### Local development with Virtualenv

This will setup a basic development environment to let you patch the code and see directly your changes in your browser.

```
$ make run-venv
```
This will install locally Python virtualenv and the project dependencies if there are not installed. Once done, it will start the webserver locally, on [127.0.0.1:5000](http://127.0.0.1:5000/).

### Development with Docker

To be done.


## Infos

Author: MrJK
License: GPLv3
Date: October 2020

