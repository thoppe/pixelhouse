# pixelhouse

[![PyVersion](https://img.shields.io/pypi/pyversions/pixelhouse.svg)](https://img.shields.io/pypi/pyversions/pixelhouse.svg)
[![PyPI](https://img.shields.io/pypi/v/pixelhouse.svg)](https://pypi.python.org/pypi/pixelhouse)

A minimalist drawing library for making beautiful animations in python.
Anything that can be drawn can be moved.
_Very much a work in progress!_

      pip install pixelhouse

## Examples (click for source)

[![Example image: blue woods](examples/blue_woods.png)](examples/blue_woods.py)

[![Example image: Logo](examples/logo_pixelhouse.png)](examples/logo_pixelhouse.py)
[![Example image: Circle Lines](examples/circle_lines.png)](examples/circle_lines.py)

[![](examples/simple_circles.png)](examples/small_demos.py)
[![](examples/teyleen_982.png)](examples/small_demos.py)
[![](examples/teyleen_116.png)](examples/small_demos.py)
[![](examples/moving_circles.gif)](examples/small_demos.py)
[![](examples/checkerboard.gif)](examples/small_demos.py)
[![](examples/pacman.gif)](examples/small_demos.py)
[![](examples/timer.gif)](examples/small_demos.py)

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

#### Layers
+ [x] Blended
+ [x] Additive
+ [x] Subtractive
+ [x] Direct (for primitives)

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
+ [x] Proper library
+ [x] setup.py
+ [x] pip install
+ [x] Context mangager for canvas
+ [ ] Context mangager for animation
+ [ ] Unit tests (started!)
+ [ ] Doc coverage (started!)
+ [ ] Subpixel resolution


## Credits

+ [Travis Hoppe](https://twitter.com/metasemantic?lang=en)

## Projects used 

+ [`opencv`](https://opencv.org/)
+ [Easing functions](https://github.com/semitable/easing-functions)
+ [Bezier curves](https://github.com/reptillicus/Bezier)
