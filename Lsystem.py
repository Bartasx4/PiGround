import math
import numpy as np


class GosperCurve:
    """
    Represents the Gosper curve (also known as the Peano-Gosper curve or flowsnake)
    in the context of L-systems.

    The Gosper curve is a space-filling curve that can be generated iteratively using
    L-system (Lindenmayer system) rules. This class provides functionalities to generate
    the pattern for a specified number of stages, and convert that pattern into a
    corresponding list of line segments based on a starting point and direction.

    :ivar RULES: The L-system rules to generate the Gosper curve.
    :type RULES: dict[str, str]
    :ivar AXIOM: The starting point for the L-system.
    :type AXIOM: str
    :ivar ROTATION_ANGLE: The rotation angle in degrees for interpreting "+" and "-"
        symbols in the L-system pattern.
    :type ROTATION_ANGLE: int
    """
    RULES = {
        'A': 'A-B--B+A++AA+B-',
        'B': '+A-BB--B-A++A+B',
    }
    AXIOM = 'A'
    ROTATION_ANGLE = 60  # Extracted constant for rotation angle in degrees

    @staticmethod
    def generate_pattern(current_stage: str = None, stages_count: int = 5, rules: dict[str, str] = None) -> str:
        """Generates the L-system pattern for the specified number of stages."""
        current_stage = current_stage or GosperCurve.AXIOM
        rules = rules or GosperCurve.RULES
        for _ in range(stages_count - 1):  # -1 because the axiom is the first stage
            next_stage = ''
            for char in current_stage:
                next_stage += rules.get(char, char)
            current_stage = next_stage
        return current_stage

    @staticmethod
    def generate_lines(pattern: str = None, start_point=(0, 0), direction=(1, 0)) -> list[tuple[np.ndarray, np.ndarray]]:
        if pattern is None:
            pattern = GosperCurve.generate_pattern()
        current_position = np.array(start_point)
        direction = np.array(direction)
        lines = []
        for char in pattern:
            if char in ['A', 'B']:
                new_position = current_position + direction
                lines.append((current_position, new_position))
                current_position = new_position
            elif char == '-':
                direction = rotate_vector(direction, -GosperCurve.ROTATION_ANGLE)
            elif char == '+':
                direction = rotate_vector(direction, GosperCurve.ROTATION_ANGLE)
        return lines


def rotate_vector(vector: tuple[float, float], angle_degrees: float) -> tuple[float, float]:
    """
    Rotates a 2D vector by a specified angle in degrees.
    """
    angle_radians = math.radians(angle_degrees)
    cos_theta = math.cos(angle_radians)
    sin_theta = math.sin(angle_radians)

    x_new = vector[0] * cos_theta - vector[1] * sin_theta
    y_new = vector[0] * sin_theta + vector[1] * cos_theta
    return x_new, y_new
