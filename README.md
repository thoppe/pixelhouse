# Quad
A minimalist drawing library for making beautiful animations in python.
_Very much a work in progress!_

## Examples

![](examples/simple_circles.png)
![](examples/simple_rectangle.png)
![](examples/simple_lines.png)
![](examples/teyleen_982.png)

![](examples/moving_circles.gif)
![](examples/pacman.gif)
![](examples/checkerboard.gif)
![](examples/timer.gif)


[Example code](generate_demos.py)

## Wishlist / Roadmap

#### Primitives 
+ [x] Line
+ [x] Circle
+ [x] Ellipise
+ [ ] Polyline
+ [ ] Backgrounds
+ [ ] Text

#### Transforms
+ [ ] Rotation
+ [ ] Scale
+ [ ] Shear
+ [ ] Hide abstract cv2, BGR -> RGB
+ [ ] Subpixel resolution

#### Layers
+ [x] Simple additive
+ [x] Simple blend
+ [ ] Alpha additive

#### Filters
+ [ ] Blur
+ [ ] Color mixing
+ [ ] Histogram normlization

#### Easing
+ [x] Named easing, Pennser equations
+ [x] Generic beizer easing

#### Color/Palettes
+ [x] Named colors
+ [x] Top palettes
+ [ ] Random palettes

#### Devops
+ [x] Save to gif
+ [x] Save to mp4 
+ [ ] Load from gif
+ [ ] Load from mp4
+ [ ] Proper library
+ [ ] Unit tests
+ [ ] Doc coverage

## Credits

+ [Travis Hoppe](https://twitter.com/metasemantic?lang=en)

## Projects used 

+ [`opencv`](https://opencv.org/)
+ [Easing functions](https://github.com/semitable/easing-functions)
+ [Bezier curves](https://github.com/reptillicus/Bezier)
