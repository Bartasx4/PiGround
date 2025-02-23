# Pi Animations with Manim

Pi Day is celebrated on March 14th (3/14 in month/day format) because the digits 3, 1, and 4 are the first three digits of π.
This project uses [Manim Community Edition](https://github.com/ManimCommunity/manim) to visualize mathematical concepts through animations.
The animations include a Monte Carlo approximation of π, an illustration of the relationship between a circle’s circumference and π, and a demonstration of Aristotle’s Wheel Paradox.


## About the Project

This repository contains four animations:

### PiGraph Animation
This animation visualizes how the circumference of a circle is related to π.
For a circle with a radius of 0.5, its circumference is exactly π.
The animation shows the circle "unwrapping" its circumference as it rolls along an axis.

Key aspects:
- Visualizes a circle of radius 0.5 and its associated circumference.
- Demonstrates that the unwrapped circumference equals π (approximately 3.14).
- Emphasizes the relationship between the radius and circumference, reinforcing that π is the ratio of a circle's circumference to its diameter.

### Monte Carlo Approximation
This animation demonstrates a Monte Carlo method to approximate π.
In this scene, a circle and a square are drawn, where the square has a side equal to the circle's diameter (2r).
By randomly distributing points in the square and counting how many fall inside the circle, the animation provides a visual approximation of π.

Key aspects:
- Constructs a circle and a bounding square (with side length equal to the circle’s diameter).
- Illustrates that the area of the square is (4/π) times the area of the circle.
- Uses random point generation to approximate the value of π.


### Aristotle's Wheel Paradox
This animation explores a classical geometrical paradox.
Aristotle's Wheel Paradox involves rolling two concentric circles of different sizes.
Although their circumferences differ, the paradox shows that both circles seem to travel the same distance when rolled.

Key aspects:
- Visualizes two concentric circles (one larger and one smaller) rolling simultaneously.
- Highlights the counterintuitive result where both circles cover the same linear distance despite their different circumferences.


### Polygon Approximation
This animation demonstrates how to approximate the circumference of a circle (π) by using the perimeters of inscribed and circumscribed polygons.

Key aspects:
- Visualizes two polygons: one inscribed in the circle and one circumscribed around it.
- Shows how increasing the number of polygon sides improves the accuracy of the approximation.
- Highlights the relationship between the circle's circumference and π through geometric methods.


## Video Preview

### PiGraph Animation
<video src="https://github.com/user-attachments/assets/8c0c0bef-c745-4a5d-92ae-e2ae4dff5866" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>

### PiRatio Animation
<video src="https://github.com/user-attachments/assets/7f1e8691-ed83-4093-976c-a882033543b1" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>

### Aristotle's Wheel Paradox Animation
<video src="https://github.com/user-attachments/assets/479049fa-9144-4ffa-8935-7fc00986267a" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>

### Polygon Approximation Animation
<video src="https://github.com/user-attachments/assets/8ba42ef8-60e1-4316-a921-13a1417e7aad" controls="controls" style="max-width: 400px;">
  Your browser does not support the video tag.
</video>


## Usage

1. Install [Manim Community Edition](https://docs.manim.community/en/stable/installation.html) (version 0.19.0 or later).
2. Render the desired scene by running one of the following commands in your terminal:

   - For the Monte Carlo approximation animation:
     ```
     manim -pqh PiRatio.py PiRatio
     ```
   - For the Aristotle's Wheel Paradox animation:
     ```
     manim -pqh wheelParadox.py WheelParadox
     ```
   - For the PiGraph animation:
     ```
     manim -pqh pigraph.py PiGraph
     ```
   - For the PiPolygonApproximation animation:
     ```
     manim -pqh piPolygonApproximation.py PiPolygonApproximation
     ```

     The generated videos will be stored in the media folder.


## License & Acknowledgments

MIT license.
  

Enjoy and Happy Pi Day (3.14)!  