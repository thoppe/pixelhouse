# pixelhouse
A minimalist drawing library for making beautiful animations in python.
_Very much a work in progress!_

## Examples

![](examples/simple_circles.png)
![](examples/simple_rectangle.png)
![](examples/simple_lines.png)
![](examples/teyleen_982.png)
![](examples/teyleen_116.png)

![](examples/instafilters_from_file.png)

![](examples/moving_circles.gif)
![](examples/checkerboard.gif)
![](examples/pacman.gif)
![](examples/timer.gif)


[Example code](generate_demos.py)

## Wishlist / Roadmap

#### Primitives 
+ [x] Line
+ [x] Circle
+ [x] Ellipse
+ [x] Polyline
+ [x] Backgrounds
+ [ ] Text

#### Transforms
+ [x] Rotation
+ [x] Translation
+ [x] Scale
+ [x] Elastic distortion
+ [x] Generic elastic deformations

#### Gradients
+ [x] Linear gradients

#### Layers
+ [x] Additive
+ [x] Subtractive
+ [x] Overlay
+ [x] Direct (for primitives)

#### Filters
+ [x] Blur
+ [x] Instagram-style filters (keras not needed)
+ [ ] Histogram normalization

#### Easing
+ [x] Named easing, Pennser equations
+ [x] Generic beizer easing

#### Color/Palettes
+ [x] Named colors
+ [x] Top palettes
+ [ ] Random palettes

#### File IO
+ [x] Save to gif
+ [x] Save to mp4 
+ [ ] Load from gif
+ [ ] Load from mp4

#### Devops
+ [x] Unified class for artists
+ [x] Proper library
+ [ ] setup.py
+ [ ] pip install
+ [ ] Context mangager for canvas and animation
+ [ ] Unit tests
+ [ ] Doc coverage
+ [ ] Subpixel resolution
+ [x] Hide cv2 weird colorspace, BGR -> RGB


## Credits

+ [Travis Hoppe](https://twitter.com/metasemantic?lang=en)

## Projects used 

+ [`opencv`](https://opencv.org/)
+ [Easing functions](https://github.com/semitable/easing-functions)
+ [Bezier curves](https://github.com/reptillicus/Bezier)
