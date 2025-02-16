from manim import *
from manim.utils.rate_functions import ease_in_out_back

from Lsystem import GosperCurve
import numpy as np

# --------------------------------------
# Constants
# --------------------------------------
CIRCLE_COLOR = GREEN
SQUARE_COLOR = BLUE
RAIL_COLOR = RED
AREA_LABEL_COLOR = MAROON_A
CIRCLE_FILL = GREEN_A

CIRCLE_HIGHLIGHT_OPACITY = 0.65
SQUARE_HIGHLIGHT_OPACITY = 1

CIRCLE_AREA_FORMULA = r'$P_{\displaystyle \circ} = \pi r^2$'
SQUARE_AREA_FORMULA = r'$P_{\scriptscriptstyle \square} = a^2$'

RATIO_FORMULA_COLOR = MAROON_A
RATIO_FORMULA = r'$\frac{P_{\scriptscriptstyle \square}}{P_{\displaystyle \circ}} = \frac{(2r)^2}{\pi r^2} = \frac{4}{\pi}$'
RATIO_FORMULA_SHORT = r'$\frac{P_{\scriptscriptstyle \square}}{P_{\displaystyle \circ}} = \frac{4}{\pi}$'

config.window_position = '830,300'

# --------------------------------------
# Scene Definition
# --------------------------------------
class PiRatio(Scene):
    """
    Demonstrates the ratio of the areas of a square and circle with the same
    diameter/side ratio and illustrates Monte Carlo approximation of Pi.
    """

    def setup(self):
        """
        Called automatically before construct(). Draws the background Gosper Curve.
        """
        self.draw_background()

    def construct(self):
        """
        Main execution method for the scene. Draws shapes, area formulas, ratio
        derivations, and demonstrates a Monte Carlo style approximation for pi.
        """
        self.draw_shapes()
        self.wait()
        self.interactive_embed()

    # ----------------------------------
    # Background
    # ----------------------------------

    def draw_background(self):
        """
        Draws a Gosper Curve in the background. This uses lines generated
        from the Lsystem.GosperCurve.
        """
        lines = GosperCurve.generate_lines(start_point=(3, 10), direction=(0.4, 0))
        lines_obj = VGroup(
            *[
                Line(
                    np.concatenate((line[0], [0])),
                    np.concatenate((line[1], [0])),
                    stroke_width=1,
                    stroke_opacity=0.5,
                    color=PURPLE
                )
                for line in lines
            ]
        )
        self.add(lines_obj)

    # ----------------------------------
    # Shape Creation
    # ----------------------------------

    @staticmethod
    def create_circle(radius):
        """
        Creates a circle with a given radius
        and a VGroup showing radius dot, line, and label.
        """
        circle = Circle(color=CIRCLE_COLOR, fill_color=CIRCLE_FILL, fill_opacity=0, radius=radius)
        radius_dot = Dot(circle.get_center(), color=RAIL_COLOR)
        radius_line = Line(circle.get_center(), circle.get_right(), color=RAIL_COLOR)
        radius_label = Tex("r", color=RAIL_COLOR).next_to(radius_line, UP)
        radius_group = VGroup(radius_dot, radius_line, radius_label)
        return circle, radius_group

    @staticmethod
    def create_square_with_arrows(radius):
        """
        Creates a square with side length 2*radius, along with two lines
        indicating the side length and arrow markers.
        """
        square = Square(side_length=2 * radius, color=SQUARE_COLOR)
        up_shift = UP * (radius + 1)
        length_line_left = Line(up_shift, up_shift + LEFT * radius, color=RAIL_COLOR)
        length_line_right = Line(up_shift, up_shift + RIGHT * radius, color=RAIL_COLOR)
        left_arrow = Arrow(
            length_line_left.get_left(),
            square.get_boundary_point(UL) + UP * 0.25,
            buff=0, stroke_width=3, color=RAIL_COLOR
        )
        right_arrow = Arrow(
            length_line_right.get_right(),
            square.get_boundary_point(UR) + UP * 0.25,
            buff=0, stroke_width=3, color=RAIL_COLOR
        )
        length_line_group = VGroup(length_line_left, length_line_right, left_arrow, right_arrow)
        length_label = Tex("a", color=RAIL_COLOR).next_to(length_line_group, UP)
        return square, length_line_group, length_label

    @staticmethod
    def create_text_label(text, target_object, direction, shift=ORIGIN):
        """
        Helper for creating a Tex label near a given target_object,
        in some direction plus optional shift.
        """
        label = Tex(text, color=AREA_LABEL_COLOR).next_to(target_object, direction).shift(shift)
        return label

    # ----------------------------------
    # Drawing & Animation
    # ----------------------------------

    def draw_shapes(self):
        """
        Main orchestration method for drawing the shapes (circle, square),
        their area labels, and setting up the scene for the pi ratio demonstration.
        """
        # Create shapes
        radius = 2
        circle, radius_group = self.create_circle(radius)
        square, square_length_group, square_length_label = self.create_square_with_arrows(radius)

        # Draw circle
        self.draw_circle_and_radius(circle, radius_group)
        circle_area_label = self.create_text_label(CIRCLE_AREA_FORMULA, circle, RIGHT)
        self.draw_area_label_and_highlight(circle, circle_area_label, CIRCLE_HIGHLIGHT_OPACITY)

        # Draw square and arrows
        self.draw_square_and_arrows(square, square_length_group, square_length_label)
        square_area_label = self.create_text_label(SQUARE_AREA_FORMULA, circle, RIGHT, UP)
        self.draw_area_label_and_highlight(square, square_area_label, SQUARE_HIGHLIGHT_OPACITY)
        self.wait(0.5)

        # Animate radius line / side length equivalence
        self.animate_radius_line_and_square_label(circle, radius_group, square, square_length_label, square_length_group)

        # Move everything to the left and remove the area labels
        all_group = VGroup(circle, square, radius_group, square_length_group, square_length_label, circle_area_label, square_area_label)
        self.animate_move_and_remove_area_labels(all_group, square_area_label, circle_area_label)

        # Show ratio formulas
        self.draw_and_animate_ratio_formula(square, circle, radius_group, square_length_group, square_length_label)

        # Draw random points and animate them for a Monte Carlo approximation
        points = self.draw_points()
        points_in_circle, points_in_square = self.animate_points(points, circle, square)
        self.draw_ratio_calculation(points_in_circle, points_in_square, square)

    def draw_circle_and_radius(self, circle, radius_group):
        """
        Creates the circle and radius line animations.
        """
        self.play(Create(circle, rate_func=ease_in_out_back), run_time=4)
        self.add(radius_group[0])  # Add center dot
        self.play(Create(radius_group[1]))  # Radius line
        self.play(Create(radius_group[2]))  # Label 'r'

    def draw_square_and_arrows(self, square, square_length_group, square_length_label):
        """
        Draws the square and its side arrows/labels.
        """
        # TODO: Check why I'm actually using two lines instead of one.
        self.play(Create(square, rate_func=ease_in_out_back), run_time=5)
        self.play(Create(square_length_group[0]), Create(square_length_group[1]))  # Left and right lines
        self.play(Create(square_length_group[-2]), Create(square_length_group[-1]))  # Left and right arrows
        self.play(Write(square_length_label), run_time=1.5)
        self.wait(0.5)

    def animate_radius_line_and_square_label(self, circle, radius_group, square, square_length_label, square_length_group):
        """
        Demonstrates that the square's side length is 2r by transforming
        the radius line.
        """
        radius_to_line = radius_group[1].copy()
        self.add(radius_to_line)
        self.play(
            Transform(radius_to_line, Line(circle.get_right(), circle.get_left(), color=RED))
        )
        self.play(radius_to_line.animate.move_to(square.get_top()))
        self.wait(0.5)

        # Change length label to a=2r
        self.play(
            Transform(square_length_label, Tex("a=2r", color=RED).next_to(square_length_group, UP)),
            FadeOut(radius_to_line),
            run_time=1.5
        )
        self.wait(1)

    def animate_move_and_remove_area_labels(self, all_group, square_area_label, circle_area_label):
        """
        Moves the shapes to the left and removes the area labels from the scene.
        """
        self.play(all_group.animate.shift(LEFT * 2))
        self.play(
            AnimationGroup(square_area_label.animate.shift(DOWN).fade(1), run_time=1),
            AnimationGroup(circle_area_label.animate.fade(1), run_time=1),
            lag_ratio=.5
        )
        self.remove(square_area_label)

    def draw_and_animate_ratio_formula(self, square, circle, radius_group, square_length_group, square_length_label):
        """
        Writes and shows the ratio formula of square area to circle area,
        then shortens it to 4/pi. Finally, adjusts the shapes for random point
        placement.
        """
        area_formula = Tex(RATIO_FORMULA, color=RATIO_FORMULA_COLOR).next_to(square, RIGHT)
        self.play(Write(area_formula), run_time=5.5)

        area_formula_short = Tex(RATIO_FORMULA_SHORT, color=RATIO_FORMULA_COLOR).next_to(square, RIGHT).shift(DOWN)
        self.play(Write(area_formula_short), run_time=3)

        # Remove labels and transform shapes
        self.play(FadeOut(radius_group, square_length_group, square_length_label, area_formula, area_formula_short))
        self.play(
            Transform(circle, Circle(color=GREEN, fill_color=GREEN_A, fill_opacity=0, radius=4)),
            Transform(square, Square(side_length=8, color=BLUE)),
            run_time=2
        )

    def draw_points(self):
        """
        Creates and draws a random set of Dot objects to be used in the
        Monte Carlo approximation steps. Uses np.random for coordinates.
        """
        np.random.seed(4)
        edge = 39
        points = [(np.random.randint(-edge, edge), np.random.randint(-edge, edge)) for _ in range(250)]
        points_objects = [Dot([0.1 * x, 0.1 * y, 0], radius=0.04, color=RED) for x, y in points]

        # Animate the creation of the first 10 points more slowly, then faster for the rest.
        self.play(Succession(*[Create(point, run_time=1) for point in points_objects[:10]], lag_ratio=.25))
        self.play(Succession(*[Create(point, run_time=0.1) for point in points_objects[10:]], lag_ratio=.07))
        return points_objects

    def animate_points(self, points_objects, circle, square):
        """
        Colors and arranges the random points into those inside the circle
        vs. those outside (but still within the bounding square).
        Then transforms shapes and points for further demonstration.
        """
        circle_radius = 4
        points_in_circle = VGroup()
        points_in_square = VGroup()

        # Separate points into inside/outside circle
        for point in points_objects:
            if point.get_x() ** 2 + point.get_y() ** 2 < circle_radius ** 2:
                points_in_circle.add(point)
            else:
                points_in_square.add(point)

        self.play(
            *[point.animate.set_color(GREEN) for point in points_in_circle],
            *[point.animate.set_color(BLUE) for point in points_in_square],
            run_time=3
        )

        # Arrange points in a grid for clarity
        self.play(
            points_in_circle.animate.arrange_in_grid(cols=20, buff=0.02).next_to(square, RIGHT).shift(UP),
            points_in_square.animate.arrange_in_grid(cols=20, buff=0.02).next_to(square, RIGHT).shift(UP * 3),
            run_time=2
        )

        # Transform circle, square, and shift points
        self.play(
            Transform(circle, Circle(color=GREEN, fill_color=GREEN_A, fill_opacity=0, radius=3).shift(LEFT * 2)),
            Transform(square, Square(side_length=6, color=BLUE).shift(LEFT * 2)),
            points_in_circle.animate.shift(LEFT * 3),
            points_in_square.animate.shift(LEFT * 3),
            run_time=2
        )
        return points_in_circle, points_in_square

    def draw_ratio_calculation(self, points_in_circle, points_in_square, square):
        """
        Displays the final numeric ratio calculation in a MathTex object,
        illustrating the approximation for pi derived from the ratio of
        random points inside the circle vs. total points in the bounding square.
        """
        def create_label():
            template = r'\frac{points_in_circle}{points_in_square + points_in_circle} * 4 \approx result'
            result = (len(points_in_circle) / (len(points_in_square) + len(points_in_circle))) * 4
            return template.replace('points_in_circle', str(len(points_in_circle))) \
                           .replace('points_in_square', str(len(points_in_square))) \
                           .replace('result', f'{result:.3f}')

        circle_points_label = Text(str(len(points_in_circle)), color=GREEN).next_to(points_in_circle, RIGHT)
        square_points_label = Text(str(len(points_in_square)), color=BLUE).next_to(points_in_square, RIGHT)
        self.play(Write(circle_points_label), Write(square_points_label), run_time=1.5)

        # Text coloring is not working. It might be a problem with my TeXworks configuration.
        equation_label = MathTex(create_label()).next_to(square, RIGHT).shift(DOWN)
        # substrings_to_isolate=[str(len(points_in_circle)), str(len(points_in_square))]
        # substrings_to_isolate={str(len(points_in_circle)): GREEN, str(len(points_in_square)): BLUE},
        # equation_label.set_color_by_tex(str(len(points_in_circle)), GREEN)
        # equation_label.set_color_by_tex(str(len(points_in_square)), BLUE)
        self.play(Write(equation_label))

    def draw_area_label_and_highlight(self, shape, label, highlight_opacity):
        """
        Writes an area label near a shape and temporarily highlights the shape.
        """
        shape_copy = shape.copy()
        highlight = shape.animate.scale(1.1).set_fill(opacity=highlight_opacity)
        self.play(
            Write(label, run_time=3),
            AnimationGroup(highlight, rate_func=there_and_back, run_time=3)
        )
        shape.become(shape_copy)