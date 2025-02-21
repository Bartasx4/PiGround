# Pi Day (03.14) Animation with Manim

Pi Day is celebrated on March 14th (3/14 in month/day format) because the digits 3, 1, and 4 are the first three digits of π.
This project uses [Manim](https://github.com/ManimCommunity/manim) to visualize mathematical concepts in animations, including a Monte Carlo–style approximation of π and the Aristotle's Wheel Paradox.
 

## About the Project

### Monte Carlo Approximation:
This code demonstrates:
1. Drawing a circle and a square with a side equal to the circle’s diameter (2r)
2. Showing a ratio proof that the square’s area is (4/π × circle’s area).  
3. Randomly distributing points inside the bounding square and determining the fraction that fall inside the circle, providing a visual approximation of π (using the Monte Carlo method).

The scene file ("PiRatio") constructs animation that highlights the area ratio and demonstrates why π ≈ 3.14.  

### Aristotle's Wheel Paradox:
This second animation explores a classical geometrical paradox.
Aristotle's Wheel Paradox demonstrates how rolling two circles of different sizes leads to a surprising result where both the larger and smaller circles seemingly travel the same distance.

Key objectives of this animation:
1. Visualizing the paradox by rolling two concentric circles (one larger, one smaller).  
2. Highlighting the discrepancy between perception (equal distances) and geometry (different circumferences).

## Video Preview

### PiRatio Animation
<video src="https://github.com/user-attachments/assets/7f1e8691-ed83-4093-976c-a882033543b1" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>

### Aristotle's Wheel Paradox Animation
<video src="https://github.com/user-attachments/assets/479049fa-9144-4ffa-8935-7fc00986267a" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>


## Usage

1. Install [Manim Community Edition](https://docs.manim.community/en/stable/installation.html).
2. Render the scene with:
   ```
   manim -pqh PiRatio.py PiRatio
   ```
   to generate the PiRatio video; or:
   ```
   manim -pqh wheelParadox.py WheelParadox
   ```
   to generate the wheelParadox video.
   
   This will create the video and store it in the media folder.


## License & Acknowledgments

MIT license.
  

Enjoy and Happy Pi Day (3.14)!  