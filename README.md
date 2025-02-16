# Pi Day (03.14) Animation with Manim

Pi Day is celebrated on March 14th (3/14 in month/day format) because the digits 3, 1, and 4 correspond to the first three digits of π. This project uses [Manim](https://github.com/ManimCommunity/manim) to visualize the relationship between a circle’s area and the square that bounds it, culminating in a fun Monte Carlo–style approximation of π. 

## About the Project

This code demonstrates:
1. Drawing a circle and a square whose side equals the circle’s diameter (2r).  
2. Showing a ratio proof that the square’s area is (4/π × circle’s area).  
3. Randomly distributing points inside the bounding square and determining the fraction that fall inside the circle, providing a visual approximation for π (Monte Carlo approach).

The scene file (“PiRatio”) constructs animation that highlights the area ratio and demonstrates why π ≈ 3.14.  

## Video Preview
<video src="animations/PiRatio.mp4" controls="controls" style="max-width: 600px;">
  Your browser does not support the video tag.
</video>

## Usage

1. Install [Manim Community Edition](https://docs.manim.community/en/stable/installation.html).  
2. Place the code in a file named “PiRatio.py” (or a similar file name) in your Manim project.  
3. Run the scene with:
   ```
   manim -pqh PiRatio.py PiRatio
   ```
   This will generate a video (the animation mentioned above) in the media folder (default).  

## License & Acknowledgments

MIT license.
  

Enjoy and Happy Pi Day (3.14)!  