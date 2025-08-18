[![Pytest](https://github.com/pascal-brand38/py-responsiveimage/actions/workflows/python-app.yml/badge.svg)](https://github.com/pascal-brand38/py-responsiveimage/actions/workflows/python-app.yml)

[![Pypi version](https://img.shields.io/pypi/v/responsiveimage.svg)](https://pypi.org/project/responsiveimage)
[![Pypi Download](https://img.shields.io/pypi/dm/responsiveimage.svg)](https://pypi.org/project/responsiveimage)

# Introduction

**responsiveimage** is a python package aimed at building responsive version of images.

Supported formats are:
* image: webp, jpg, png, gif and svg
* video: mp4, mts, avi, wmv, mov
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

  As an example, using ```--size 1024,512 --add-name _big,_small```, an image ```img.jpg``` will be rescaled with 1024px and named ```img_big.jpg```, and another one rescaled at 512px and named ```img_small.jpg```

* ```--mp4-as-gif```: from a mp4 file, the gif and the webp animated versions are created, using ```ffmpeg```

* ```--crop <x1,y1,x2,y2>``` crops the original image using ```(x1,y1)``` as the top-left point (x being the horizontal position in px), and ```(x2,y2)``` being the bottom-right point.

* ```--recursive``` to scan recursively the source directory. The directory tree is kept in destination

* ```--format <f1,f2>``` to used to only process files of provided format. You can
  for example process only jpg and png to exclude videos.
  The default value is ```jpg,png,webp,gif,svg,mp4,mts,avi,wmv,mov```

* ```--copy``` copy the files instead of transforming them. Of course, the creation date is updated accordingly,
  for example using the json data

* ```--force```: recreate the scaled versions of the images, even when they exist.

<br>

_____________________
# Releases

## 1.6.0
* --copy option behavior update: copy the files instead of transforming them. Of course,
  the creation date is updated accordingly,
  for example using the json dat

## 1.5.0
* json from google photo with any suffix
* fall-back when exif is wrong
* --copy option

## 1.4.0
* animated gif and webp uses --size option

## 1.3.0
* Multiprocessing on images

## 1.2.0
* Supported formats:
  webp, jpg, png, gif and svg, mp4, mts, avi, wmv, mov
* New options:
  * --format
  * --recursive

## 1.1.1
* Fix mp4: no upscale, along max size.
* Fix HEIC format

## 1.1.0

Following capabilities are added:
* ```--height```
* ```--add-name```
* ```--crop```
* ```--force```


## 1.0.0

Initial version


# Development steps

* python -m build
* python -m pip install .
* check the following before pushing (sse .github/workflows/pyton-app.yml)
    * flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    * flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    * pylint --indent-string='  ' --disable C0103,C0200,C0301,C0325,R0912,R0913,R0914,R0915,R0917,R1705,W0511,W0621,W0613,W0702,W0718 $(git ls-files '*.py')
    * pytest tests/png.py tests/export_to_webp.py tests/mp4.py tests/crop.py


To publish:
```
Update version in pyproject.toml
git tag "x.y.z"
git push --tags
rm -rf dist src/*.egg-info
python -m build
python -m twine upload dist/* --verbose --skip-existing
    id = __token__
    password: py-XXX  (the private API token)
```
