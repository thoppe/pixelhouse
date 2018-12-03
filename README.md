# pixelhouse

[![PyVersion](https://img.shields.io/pypi/pyversions/pixelhouse.svg)](https://img.shields.io/pypi/pyversions/pixelhouse.svg)
[![PyPI](https://img.shields.io/pypi/v/pixelhouse.svg)](https://pypi.python.org/pypi/pixelhouse)

A minimalist drawing library for making beautiful animations in python.
Anything that can be drawn can be moved.  Comes with beautiful gradients, instagram-like filters, and elastic transforms.

_Very much a work in progress!_

      pip install pixelhouse

## Examples (click for source)

[![Example image: blue woods](examples/figures/blue_woods.png)](examples/blue_woods.py)

[![Example image: Logo](examples/figures/logo_pixelhouse.png)](examples/logo_pixelhouse.py)
[![Example image: Circle Lines](examples/figures/circle_lines.png)](examples/circle_lines.py)

[![](examples/figures/simple_circles.png)](examples/small_demos.py)
[![](examples/figures/teyleen_982.png)](examples/small_demos.py)
[![](examples/figures/teyleen_116.png)](examples/small_demos.py)
[![](examples/figures/moving_circles.gif)](examples/small_demos.py)
[![](examples/figures/checkerboard.gif)](examples/small_demos.py)
[![](examples/figures/pacman.gif)](examples/small_demos.py)


_Submit your examples as an issue/pull request or post to twitter under #pixelhouse to have them showcased here!_

## Wishlist / Roadmap

#### Primitives 
+ [x] Line
+ [x] Circle
+ [x] Ellipse
+ [x] Polyline
+ [x] Backgrounds
+ [x] Text
+ [ ] Beizer curves

#### Transforms
+ [x] Rotation
+ [x] Translation
+ [x] Scale
+ [x] Elastic distortions

#### Gradients
+ [x] Linear gradients with transparent elements
+ [x] Discrete gradients

#### Layers
+ [x] Blended
+ [x] Additive
+ [x] Subtractive

#### Filters
+ [x] Blur
+ [x] Instagram-style filters (keras not needed)

#### Easing
+ [x] Named easing, Pennser equations
+ [x] Generic beizer easing

#### Color/Palettes
+ [x] Named colors
+ [x] Top palettes

#### File IO
+ [x] Save to gif
+ [x] Save to mp4 
+ [ ] Load from gif
+ [ ] Load from mp4

#### Devops
+ [x] Unified class for artists
+ [x] Hide cv2 weird colorspace, BGR -> RGB
+ [x] Subpixel resolution for primitives
+ [x] Proper library
+ [x] setup.py
+ [x] pip install
+ [x] Context mangager for canvas
+ [x] Context mangager for animation (working but not nested)
+ [ ] Unit tests (started!)
+ [ ] Doc coverage (started!)


## Credits

+ [Travis Hoppe](https://twitter.com/metasemantic?lang=en)

## Projects used 

+ [`opencv`](https://opencv.org/)
+ [Easing functions](https://github.com/semitable/easing-functions)
+ [Bezier curves](https://github.com/reptillicus/Bezier)

## Press

+ [python weekly](https://mailchi.mp/pythonweekly/python-weekly-issue-374)
