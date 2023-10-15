[![Pytest](https://github.com/pascal-brand38/py-responsiveimage/actions/workflows/python-app.yml/badge.svg)](https://github.com/pascal-brand38/py-responsiveimage/actions/workflows/python-app.yml)

[![Pypi version](https://img.shields.io/pypi/v/responsiveimage.svg)](https://pypi.org/project/responsiveimage)
[![Pypi Download](https://img.shields.io/pypi/dm/responsiveimage.svg)](https://pypi.org/project/responsiveimage)

# Introduction

**responsiveimage** is a python package aimed at building responsive version of images.

Supported image format are webp, jpg, png, gif and svg.

<br>

____________
# Usage

## Installation

Run ```python -m pip install responsiveimage``` to install the python package.

Also, please install the binaries ```ffmpeg``` and ```optipng```
(using apt-get, pacman, or directly from
[sourceforge](https://optipng.sourceforge.net/))
to further optimize the png version of the sprite.

## Usage

* resize and save all images in ```<srcdir>``` into ```<dstdir>```. New size is 1920px by default (at largest dimension, keep the aspect-ratio), and save quality is:
  * gif and svg: direct copy
  * png: use Pillow library, with Optimize=True
  * jpg: quality=80, progressive, 4:2:2
  * webp: quality=80
  * mp4: use ```ffmpeg``` to scale at 1024

```
python -m responsiveimage --src-dir <srcdir> --dst-dir <dstdir>
```

* ```--export-to-webp```: also export the ```webp``` version of the image

* ```--size <s1,s2...>```: different scaling are generating, instead of the default 1920px.
  The max size will be s1, s2...

* ```--height <s1,s2...>```: different scaling are generating, based on the height which will be
  be s1, s2... Note that ```--size``` and ```--height``` cannot be used at the same time.

* By default, the name of the created responsive versions of the
  image are
  * unchanged if there is a single scaled version of the image
  * or suffixed with ```-s1```, ```-s2```... otherwise.

  Option ```--add-name <name1,name2...>```is used to modify the suffix, in ```name1``` , ```name2```.
  Note that the numbers of sizes or heights must be the same as the one of add-name if provided

  As an example, using ```--size 1024,512 --add-name _big,_small```, an image ```img.jpg``` will be rescaled with 1024px and named ```img_big_.jpg```, and another one rescaled at 512px and named ```img_small_.jpg```

* ```--mp4-as-gif```: from a mp4 file, the gif and the webp animated versions are created, using ```ffmpeg```

* ```--crop <x1,y1,x2,y2>``` crops the original image using ```(x1,y1)``` as the top-left point (x being the horizontal position in px), and ```(x2,y2)``` being the bottom-right point.

* ```--force```: recreate the scaled versions of the images, even when they exist.

<br>

_____________________
# Releases

# Next
* Fix mp4: no upscale, along max size.

## 1.1.0

Following capabilities are added:
* ```--height```
* ```--add-name```
* ```--crop```
* ```--force```


## 1.0.0

Initial version
