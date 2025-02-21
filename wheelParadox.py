from manim import *
from Lsystem import GosperCurve

BIG_CIRCLE_RADIUS = 1.5
BIG_CIRCLE_LENGTH = 3 * PI
BIG_CIRCLE_COLOR = GREEN
SMALL_CIRCLE_COLOR = BLUE
START_POINT = LEFT * PI * 1.5
TITLE = "Aristotle's  Wheel  Paradox"


class WheelVisualizer:
    """
    Visualizes a wheel, consisting of a circle and a rolling line.
    Manages the appearance, motion, and optional ghost trail.
    """

    def __init__(self, scene, target, radius, color, max_length=2 * PI, shift=ORIGIN):
        """
        Initializes the visualizer for a wheel.

        Parameters:
        - scene: The current Scene instance.
        - target: A reference circle defining the wheel's position.
        - radius: Radius of the circle.
        - color: Visual color of the circle and line.
        - max_length: Maximum rolling line length.
        - shift: Offset for circle placement.
        """
        self.scene = scene
        self.target = target
        self.start_point = target.get_center()
        self.radius = radius
        self.color = color
        self.max_length = max_length
        self.shift = shift
        self.circle = self.create_arc()
        self.line = self.create_line()
        self.ghost_circle = None
        self.scene.add(self.line)

    def create_arc(self):
        """
        Creates an arc representing the wheel as it rolls.
        """
        angle = (2 * PI) - ((2 * PI) * ((self.target.get_x() - self.start_point[0]) / self.max_length))
        return Arc(radius=self.radius,
                   color=self.color,
                   start_angle=1.5 * PI,
                   angle=max(angle, 0),
                   arc_center=self.target.get_center() + self.shift).set_z_index(2)

    def create_line(self):
        """
        Creates a rolling line beneath the wheel.
        """
        start_point = self.start_point + self.shift + np.array((0, -self.radius, 0))
        end_point = self.target.get_center() + self.shift + np.array((0, -self.radius, 0))
        length = min(float(end_point[0]), self.start_point[0] + self.max_length)
        end_point = np.array((length, end_point[1], 0))
        return Line(start=start_point, end=end_point, color=self.color)

    def add_ghost(self):
        """
        Adds a semi-transparent 'ghost' circle to trail the wheel's path.
        """
        self.ghost_circle = Circle(radius=self.radius, stroke_opacity=0.5, color=GRAY).move_to(
            self.target.get_center() + self.shift).set_z_index(0)
        self.scene.add(self.ghost_circle)
        self.ghost_circle.add_updater(lambda obj: obj.move_to(self.line.get_end() + np.array((0, self.radius, 0))))

    def set_updaters(self):
        """
        Sets updaters to enable rolling arc and line animation.
        """
        self.circle.add_updater(self._update_arc)
        self.line.add_updater(self._update_line)

    def remove_updaters(self):
        """
        Removes updaters to stop animations on arc and line.
        """
        self.circle.clear_updaters()
        self.line.clear_updaters()
        self.ghost_circle.clear_updaters()

    def _update_arc(self, obj):
        """
        Updates the arc during animation.
        """
        obj.become(self.create_arc())

    def _update_line(self, obj):
        """
        Updates the rolling line during animation.
        """
        obj.become(self.create_line())


class WheelParadox(Scene):
    """
    Main Scene demonstrating Aristotle's Wheel Paradox.
    Consists of a title, animations, and explanations.
    """

    def construct(self):
        """
        Constructs and displays the visual demonstration.
        """
        self.draw()

    def draw(self):
        """
        Draws all components of the paradox: background, title, and animations.
        """
        self.draw_background()
        self.create_title()
        self.first_part()
        self.second_part()

    def draw_background(self):
        """
        Draws a Gosper Curve in the background for visual appeal.
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

    def create_title(self):
        """
        Creates and animates the title of the scene.
        """
        title = Text(TITLE, font_size=32, gradient=(BLUE_D, BLUE)).move_to(UP * 3.5)
        self.play(Write(title), run_time=3.5)

    def create_circles(self, radius, circle_length, circle_shift, small_circle_length, small_circle_shift):
        """
        Creates large and small circles with ghost trails and animations.

        Parameters:
        - radius: Radius of the larger circle.
        - circle_length: Rolling length of the large circle.
        - circle_shift: Position offset for the large circle.
        - small_circle_length: Rolling length of the small circle.
        - small_circle_shift: Position offset for the small circle.

        Returns:
        Tuple of large circle, small circle, and help circle (marker).
        """
        help_circle = Circle(radius=radius, fill_opacity=0, stroke_opacity=0).move_to(START_POINT)
        circle = WheelVisualizer(self, help_circle, radius, BIG_CIRCLE_COLOR, circle_length, circle_shift)
        small_circle = WheelVisualizer(self, help_circle, radius / 2, SMALL_CIRCLE_COLOR, small_circle_length,
                                       small_circle_shift)
        self.play(Create(circle.circle), Create(small_circle.circle), run_time=3)
        circle.add_ghost()
        small_circle.add_ghost()
        circle.set_updaters()
        small_circle.set_updaters()
        return circle, small_circle, help_circle

    def remove_circles(self, circle, small_circle):
        """
        Removes circles and their animations from the scene.
        """
        circle.remove_updaters()
        self.remove(circle.circle, circle.ghost_circle)
        small_circle.remove_updaters()
        self.remove(small_circle.circle, small_circle.ghost_circle)
        self.play(Uncreate(circle.line), Uncreate(small_circle.line), run_time=2)

    def first_part(self):
        """
        Animates the first part of the paradox showing different motion paths.
        """
        small_circle_length = 1.5 * PI
        big_circle_shift = UP * 1
        small_circle_shift = DOWN * 2.5
        circle, small_circle, help_circle = self.create_circles(BIG_CIRCLE_RADIUS,
                                                                BIG_CIRCLE_LENGTH,
                                                                big_circle_shift,
                                                                small_circle_length,
                                                                small_circle_shift)
        self.play(help_circle.animate.shift(RIGHT * BIG_CIRCLE_LENGTH), run_time=5)
        self.wait(1)
        self.remove_circles(circle, small_circle)

    def second_part(self):
        """
        Animates the second part of the paradox comparing rolling distances.
        """
        small_circle_length = BIG_CIRCLE_LENGTH
        big_circle_shift = ORIGIN
        small_circle_shift = ORIGIN
        circle, small_circle, help_circle = self.create_circles(BIG_CIRCLE_RADIUS,
                                                                BIG_CIRCLE_LENGTH,
                                                                big_circle_shift,
                                                                small_circle_length,
                                                                small_circle_shift)
        moving_line = Line(start=help_circle.get_center(), end=circle.circle.get_last_point(),
                           color=ORANGE).set_z_index(5)
        static_line = Line(start=help_circle.get_center(), end=circle.circle.get_last_point(),
                           color=ORANGE).set_z_index(5)
        self.play(Create(moving_line), run_time=2)
        self.add(static_line)
        self.wait(1)
        moving_line.add_updater(lambda obj: obj.become(Line(
            start=help_circle.get_center(),
            end=circle.circle.get_last_point(),
            color=ORANGE
        )))
        self.play(help_circle.animate.shift(RIGHT * BIG_CIRCLE_LENGTH), run_time=8)