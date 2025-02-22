from manim import *
from Lsystem import GosperCurve


RADIUS_COLOR = RED
CIRCLE_COLOR = BLUE
TEXT_COLOR = GREEN


class PiGraph(Scene):

    def construct(self):
        self.draw()

    def draw(self):
        self.draw_background()
        self.draw_and_animate_circle()

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

    def draw_and_animate_circle(self):
        # Function to move a dot around the circumference of a circle
        def go_around_circle(obj):
            offset = float(-circle.get_x() + axes.coords_to_point(0, 0)[0])
            # Calculates the new position of the dot on the circle
            new_position = circle.point_at_angle(offset + PI + PI / 2)
            obj.move_to(new_position) # Moves the object (dot) to the calculated position

        # Function for creating a line connecting the circle's center to its edge
        def create_line():
            return Line(
                start=axes.coords_to_point(0, 0), # Line starts at the center of the circle
                end=circle.get_bottom(), # Line ends at the bottom of the circle
                stroke_color=RADIUS_COLOR, # Sets the line's color
                stroke_opacity=0.7 # Makes the line semi-transparent
            ).set_z_index(5) # Ensures the line appears on top of other elements

        # Adds a large tex object displaying the mathematical symbol Pi
        pi_text = Tex(
            r'$\displaystyle \pi$',
            color=GREEN,
            font_size=128+64,
            stroke_width=6,
            stroke_color=GREEN_D
        ).move_to(UP * 3)

        # Creates axes with coordinates and shifts them slightly upwards
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 2, 1],
            x_length=12,
            y_length=6
        ).add_coordinates().shift(UP * 0.5)

        # Creates the circle to be animated
        circle = Circle(radius=1, color=CIRCLE_COLOR).move_to(UP)

        # Creates a dot to mark the circle's radius
        radius_dot = Dot(radius=0.05, color=RADIUS_COLOR).move_to(UP).set_z_index(5)

        # Creates a line to represent the radius extending from the center
        radius_line = Line(start=radius_dot.get_center(), end=radius_dot.get_center() + RIGHT, color=RADIUS_COLOR)
        # Creates text indicating the radius of the circle
        radius_text = Tex(
            r'$r = 0.5$',
            color=RADIUS_COLOR,
            font_size=24
        ).next_to(radius_line, UP)

        # Creates a dummy plot (not visible) for alignment of the label
        func = axes.plot(lambda x: 0)
        # Adds a label for Pi on the axes
        t_label = axes.get_T_label(
            x_val=PI,
            graph=func,
            label=Tex(r'$\pi = 3.14$'),
            triangle_color=RED
        )

        # Animates the writing of the Pi symbol on the screen
        self.play(Write(pi_text), run_time=4.5)
        # Animates the creation of the axes
        self.play(Create(axes), run_time=8)
        self.wait(1.5)

        # Animates the drawing of the radius line and radius dot
        self.play(Create(radius_line), Create(radius_dot), run_time=1.5)
        # Displays the radius label
        self.play(Write(radius_text), run_time=1.5)
        self.wait(1)

        # Animates the drawing of the circle
        self.play(Create(circle), run_time=1.5)
        self.wait(1.5)

        # Removes the radius line and text from the scene
        self.play(Uncreate(radius_line), Uncreate(radius_text), run_time=1.5)

        # Moves the radius dot to the bottom of the circle
        self.play(radius_dot.animate.move_to(circle.get_bottom()), run_time=1)

        # Adds an updater to the dot so it follows the bottom of the circle
        radius_dot.add_updater(lambda obj: obj.move_to(circle.get_bottom()))
        # Moves the circle to the desired position on the axes
        self.play(circle.animate.move_to(axes.coords_to_point(0, 0.5)), run_time=2)
        self.wait(1)

        # Clears the first updater of the dot
        radius_dot.clear_updaters()
        # Adds an updater to make the dot follow the circle's edge
        radius_dot.add_updater(go_around_circle)

        # Creates a line connecting the circle's center to its radius (animated during rotation)
        length_line = create_line()
        self.add(length_line)
        length_line.add_updater(lambda obj: obj.become(create_line()))

        self.wait(0.5)

        # Animates the rotation of the circle around the axes
        self.play(circle.animate.shift(RIGHT * PI * 2), run_time=6)

        # Transforms the dot into the Pi label at its final position
        self.play(Transform(radius_dot, t_label), run_time=1.5)
