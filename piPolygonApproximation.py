from manim import *
from Lsystem import GosperCurve


CIRCLE_COLOR = GREEN
RADIUS_DOT_COLOR = RED_C
RADIUS_COLOR = RED_C
RADIUS_LABEL = r'r=0.5'
RADIUS_LABEL_COLOR = RED
RADIUS_LABEL_FONT_SIZE = 32

LABEL_SIDE_LENGTH_SHIFT = 0.5

LABEL_EXPLANATION = ['The circumference of the circle ', r'$(\pi)$', ' is between the perimeters of polygons.']
LABEL_EXPLANATION_FONT_SIZE = 36
LABEL_EXPLANATION_COLOR = BLUE_D

SMALL_POLYGON_COLOR = WHITE
BIG_POLYGON_COLOR = WHITE

STROKE_WIDTH = 1.5
RADIUS = 2


class PiPolygonApproximation(Scene):

    def construct(self):
        self.draw_background()
        self.draw()
        self.wait()

    def draw(self):
        radius_group = self.draw_circle()
        labels_group = self.first_stage(radius_group)
        self.second_stage(labels_group)

    def draw_background(self):
        """
        Draws a Gosper Curve in the background. This uses lines generated
        from the Lsystem.GosperCurve.
        """
        lines = GosperCurve.generate_lines(start_point=(-4, -9), direction=(-0.4, 0))
        lines_obj = VGroup(
            *[
                Line(
                    np.concatenate((line[0], [0])),
                    np.concatenate((line[1], [0])),
                    stroke_width=1,
                    stroke_opacity=0.4,
                    stroke_color=PURPLE
                )
                for line in lines
            ]
        )
        self.add(lines_obj)

    def create_line(self, radius, current_angle, next_angle, color=WHITE):
        return Line(
            start=(radius * np.array([np.cos(current_angle), np.sin(current_angle), 0])),
            end=(radius * np.array([np.cos(next_angle), np.sin(next_angle), 0])),
            stroke_width=STROKE_WIDTH,
            stroke_color=color
        )

    def get_polygon_perimeter(self, shape, decimals=4) -> float:
        return float(np.round(sum([line.get_arc_length() for line in shape]) / (RADIUS / 0.5), decimals))

    def create_polygons(self, count):
        outer_radius = RADIUS / np.cos(PI / count)
        part = (2 * PI) / count

        big_shape = VGroup()
        small_shape = VGroup()

        current_angle = 0
        for i in range(count):
            next_angle = current_angle + part
            if i == count - 1:
                next_angle = 0
            big_shape.add(self.create_line(outer_radius, current_angle, next_angle, BIG_POLYGON_COLOR))
            small_shape.add(self.create_line(RADIUS, current_angle, next_angle, SMALL_POLYGON_COLOR))
            current_angle = next_angle
        return small_shape, big_shape

    def create_length_labels(self, text, shapes, color=WHITE):
        return VGroup(
            Tex(text, color=color).move_to(shapes[0].get_center() + RIGHT * LABEL_SIDE_LENGTH_SHIFT + UP * LABEL_SIDE_LENGTH_SHIFT),
            Tex(text, color=color).move_to(shapes[1].get_center() + LEFT * LABEL_SIDE_LENGTH_SHIFT + UP * LABEL_SIDE_LENGTH_SHIFT),
            Tex(text, color=color).move_to(shapes[2].get_center() + LEFT * LABEL_SIDE_LENGTH_SHIFT + DOWN * LABEL_SIDE_LENGTH_SHIFT),
            Tex(text, color=color).move_to(shapes[3].get_center() + RIGHT * LABEL_SIDE_LENGTH_SHIFT + DOWN * LABEL_SIDE_LENGTH_SHIFT),
        )

    def draw_polygon_with_labels(self, text, polygon, run_time, color):
        labels = self.create_length_labels(text, polygon, color)
        for i in range(4):
            self.play(
                Create(polygon[i], run_time=run_time),
                Write(labels[i], run_time=run_time),
                rate_func=linear
            )
        self.wait(1)
        return labels

    def draw_polygons(self, polygons_count, pi_perimeter_group, polygons_draw_time, text_update_time, decimal=1, uncreate=True, uncreate_time=1.0):
        small_polygon, big_polygon = self.create_polygons(polygons_count)

        self.play(
            Create(small_polygon),
            Create(big_polygon),
            run_time=polygons_draw_time
        )

        small_polygon_perimeter = Tex(
            f'{self.get_polygon_perimeter(small_polygon):.{decimal}f}',
            color=SMALL_POLYGON_COLOR
        ).next_to(pi_perimeter_group[1], LEFT)

        big_polygon_perimeter = Tex(
            f'{self.get_polygon_perimeter(big_polygon):.{decimal}f}',
            color=BIG_POLYGON_COLOR
        ).next_to(pi_perimeter_group[1], RIGHT)

        self.play(
            Transform(pi_perimeter_group[0], small_polygon_perimeter),
            Transform(pi_perimeter_group[2], big_polygon_perimeter),
            run_time=text_update_time
        )
        if uncreate:
            self.play(
                Uncreate(small_polygon),
                Uncreate(big_polygon),
                run_time=uncreate_time
            )

        return small_polygon, big_polygon

    def draw_circle(self):
        circle = Circle(radius=RADIUS, color=CIRCLE_COLOR)
        radius_dot = Dot(radius=0.05, color=RADIUS_DOT_COLOR)
        radius_line = Line(start=radius_dot.get_center(), end=radius_dot.get_center() + RIGHT * RADIUS, color=RADIUS_COLOR)
        radius_label = Tex(RADIUS_LABEL, color=RADIUS_LABEL_COLOR, font_size=RADIUS_LABEL_FONT_SIZE).next_to(radius_line, UP)

        self.play(Create(radius_dot), run_time=1)
        self.play(Create(radius_line), run_time=1.5)
        self.play(Create(circle), run_time=3)
        self.play(Write(radius_label), run_time=2)

        return VGroup(radius_dot, radius_line, radius_label)

    def first_stage(self, radius_group):
        count = 4
        small_polygon, big_polygon = self.create_polygons(count)
        small_polygon_perimeter = Tex(f'{self.get_polygon_perimeter(small_polygon):.1f}', color=SMALL_POLYGON_COLOR).next_to(big_polygon, RIGHT)
        pi_label = Tex(r'$< \pi <$', color=RED_D).next_to(small_polygon_perimeter, RIGHT)
        big_polygon_perimeter = Tex('4', color=BIG_POLYGON_COLOR).next_to(pi_label, RIGHT)

        pi_perimeter_group = VGroup(small_polygon_perimeter, pi_label, big_polygon_perimeter)
        label_explanation = Tex(
            *LABEL_EXPLANATION,
            font_size=LABEL_EXPLANATION_FONT_SIZE,
            color=LABEL_EXPLANATION_COLOR
        ).next_to(big_polygon, UP)

        big_polygon_labels = self.draw_polygon_with_labels(
            text='1',
            polygon=big_polygon,
            run_time=0.5,
            color=BIG_POLYGON_COLOR
        )
        self.play(ReplacementTransform(big_polygon_labels, big_polygon_perimeter), run_time=2)

        small_polygon_labels = self.draw_polygon_with_labels(
            text=f'{self.get_polygon_perimeter(small_polygon)/4:.1f}',
            polygon=small_polygon,
            run_time=0.5,
            color=SMALL_POLYGON_COLOR
        )

        self.play(ReplacementTransform(small_polygon_labels, small_polygon_perimeter), run_time=2)
        self.play(Write(pi_label), run_time=1.5)
        self.play(Write(label_explanation), run_time=4)

        self.wait(1)
        self.play(Uncreate(radius_group), Uncreate(small_polygon), Uncreate(big_polygon), run_time=1)
        self.wait(1)

        return pi_perimeter_group

    def second_stage(self, pi_perimeter_group):
        self.draw_polygons(5, pi_perimeter_group, 2, 2)
        self.wait(0.5)
        self.draw_polygons(6, pi_perimeter_group, 2, 1.5, uncreate_time=1)
        self.wait(0.5)
        self.draw_polygons(8, pi_perimeter_group, 2, 1, 2, uncreate_time=0.5)
        self.wait(0.5)
        self.draw_polygons(12, pi_perimeter_group, 1.5, 1, 2,False)

        self.wait(0.5)
