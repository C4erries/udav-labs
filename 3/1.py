
from math import isclose
from numbers import Real
from typing import Iterable

EPS = 1e-9


class GeometryError(Exception):
    """Базовая ошибка для геометрических объектов."""


class InvalidIdentifierError(GeometryError):
    """Некорректный идентификатор объекта."""


class InvalidCoordinateError(GeometryError):
    """Некорректные координаты точки."""


class InvalidVertexCountError(GeometryError):
    """Некорректное количество вершин."""


class DegeneratePolygonError(GeometryError):
    """Вырожденный многоугольник."""


class SelfIntersectionError(GeometryError):
    """Самопересекающийся многоугольник."""


class MovementError(GeometryError):
    """Ошибка при перемещении объекта."""


class UnsupportedObjectError(GeometryError):
    """В метод передан объект неверного типа."""


class Point:
    x: float
    y: float

    def __init__(self, x : float, y : float):
        self.x = x
        self.y = y
    


def _is_number(value: object) -> bool:
    return isinstance(value, Real) and not isinstance(value, bool)


def _sign(value: float) -> int:
    if value > EPS:
        return 1
    if value < -EPS:
        return -1
    return 0


def _cross(a: Point, b: Point, c: Point) -> float:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)


def _same_point(first: Point, second: Point) -> bool:
    return isclose(first.x, second.x, abs_tol=EPS) and isclose(
        first.y, second.y, abs_tol=EPS
    )


def _on_segment(a: Point, b: Point, p: Point) -> bool:
    if _sign(_cross(a, b, p)) != 0:
        return False
    return (
        min(a.x, b.x) - EPS <= p.x <= max(a.x, b.x) + EPS
        and min(a.y, b.y) - EPS <= p.y <= max(a.y, b.y) + EPS
    )


def _segments_intersect(a1: Point, a2: Point, b1: Point, b2: Point) -> bool:
    d1 = _sign(_cross(a1, a2, b1))
    d2 = _sign(_cross(a1, a2, b2))
    d3 = _sign(_cross(b1, b2, a1))
    d4 = _sign(_cross(b1, b2, a2))

    if d1 == 0 and _on_segment(a1, a2, b1):
        return True
    if d2 == 0 and _on_segment(a1, a2, b2):
        return True
    if d3 == 0 and _on_segment(b1, b2, a1):
        return True
    if d4 == 0 and _on_segment(b1, b2, a2):
        return True

    return d1 != d2 and d3 != d4


class Polygon:
    vertex_count: int | None = None
    shape_name = "Polygon"

    def __init__(self, identifier: str, vertices: Iterable[Point | tuple[Real, Real]]):
        self.identifier = self._validate_identifier(identifier)
        self._vertices = self._prepare_vertices(vertices)
        self._validate_geometry()

    @staticmethod
    def _validate_identifier(identifier: str) -> str:
        if not isinstance(identifier, str) or not identifier.strip():
            raise InvalidIdentifierError(
                "Идентификатор должен быть непустой строкой."
            )
        return identifier.strip()

    @staticmethod
    def _to_point(value: Point | tuple[Real, Real]) -> Point:
        if isinstance(value, Point):
            return value
        if not isinstance(value, tuple) or len(value) != 2:
            raise InvalidCoordinateError(
                "Координаты вершины должны быть точкой Point или кортежем из двух чисел."
            )
        x, y = value
        if not _is_number(x) or not _is_number(y):
            raise InvalidCoordinateError("Координаты точки должны быть числами.")
        return Point(float(x), float(y))

    def _prepare_vertices(
        self, vertices: Iterable[Point | tuple[Real, Real]]
    ) -> list[Point]:
        result = [self._to_point(vertex) for vertex in vertices]
        if self.vertex_count is not None and len(result) != self.vertex_count:
            raise InvalidVertexCountError(
                f"{self.shape_name} должен содержать {self.vertex_count} вершин(ы)."
            )
        return result

    def _validate_geometry(self) -> None:
        if len(self._vertices) < 3:
            raise InvalidVertexCountError(
                "Многоугольник должен содержать минимум три вершины."
            )

        for index, first in enumerate(self._vertices):
            for second in self._vertices[index + 1 :]:
                if _same_point(first, second):
                    raise DegeneratePolygonError("Вершины не должны совпадать.")

        if self.area() <= EPS:
            raise DegeneratePolygonError(
                "Площадь многоугольника должна быть больше нуля."
            )

        if self._has_self_intersection():
            raise SelfIntersectionError(
                "Ребра многоугольника не должны пересекаться."
            )

    @property
    def vertices(self) -> tuple[Point, ...]:
        return tuple(self._vertices)

    def edges(self) -> list[tuple[Point, Point]]:
        return list(zip(self._vertices, self._vertices[1:] + self._vertices[:1]))

    def area(self) -> float:
        total = 0.0
        for first, second in self.edges():
            total += first.x * second.y - second.x * first.y
        return abs(total) / 2

    def move(self, dx: Real, dy: Real) -> None:
        if not _is_number(dx) or not _is_number(dy):
            raise MovementError("Смещение по осям должно задаваться числами.")
        shift_x = float(dx)
        shift_y = float(dy)
        self._vertices = [
            Point(vertex.x + shift_x, vertex.y + shift_y) for vertex in self._vertices
        ]

    def contains_point(self, point: Point) -> bool:
        inside = False
        for first, second in self.edges():
            if _on_segment(first, second, point):
                return True
            if (first.y > point.y) != (second.y > point.y):
                x_on_edge = first.x + (point.y - first.y) * (second.x - first.x) / (
                    second.y - first.y
                )
                if x_on_edge >= point.x - EPS:
                    inside = not inside
        return inside

    def intersects(self, other: "Polygon") -> bool:
        for first_start, first_end in self.edges():
            for second_start, second_end in other.edges():
                if _segments_intersect(
                    first_start, first_end, second_start, second_end
                ):
                    return True
        return self.contains_point(other.vertices[0]) or other.contains_point(
            self.vertices[0]
        )

    def compare(self, other: "Polygon") -> int:
        if not isinstance(other, Polygon):
            raise UnsupportedObjectError("compare() ожидает другой объект Polygon.")
        area_delta = self.area() - other.area()
        if isclose(area_delta, 0.0, abs_tol=EPS):
            return 0
        return 1 if area_delta > 0 else -1

    def is_intersect(self, other: "Polygon") -> bool:
        if not isinstance(other, Polygon):
            raise UnsupportedObjectError(
                "is_intersect() ожидает другой объект Polygon."
            )
        return self.intersects(other)

    def _has_self_intersection(self) -> bool:
        edges = self.edges()
        edge_count = len(edges)
        for first_index, first_edge in enumerate(edges):
            for second_index in range(first_index + 1, edge_count):
                if self._are_adjacent_edges(first_index, second_index, edge_count):
                    continue
                second_edge = edges[second_index]
                if _segments_intersect(*first_edge, *second_edge):
                    return True
        return False

    @staticmethod
    def _are_adjacent_edges(
        first_index: int, second_index: int, edge_count: int
    ) -> bool:
        if second_index == first_index:
            return True
        if second_index == first_index + 1:
            return True
        return first_index == 0 and second_index == edge_count - 1

    def __str__(self) -> str:
        vertices = ", ".join(f"({v.x:.1f}; {v.y:.1f})" for v in self.vertices)
        return f"{self.shape_name}<{self.identifier}>: {vertices}"


class Triangle(Polygon):
    vertex_count = 3
    shape_name = "Triangle"


class Pentagon(Polygon):
    vertex_count = 5
    shape_name = "Pentagon"


def compare(first: Pentagon, second: Triangle) -> int:
    if not isinstance(first, Pentagon) or not isinstance(second, Triangle):
        raise UnsupportedObjectError(
            "compare() принимает объекты Pentagon и Triangle."
        )
    return first.compare(second)


def is_intersect(first: Pentagon, second: Triangle) -> bool:
    if not isinstance(first, Pentagon) or not isinstance(second, Triangle):
        raise UnsupportedObjectError(
            "is_intersect() принимает объекты Pentagon и Triangle."
        )
    return first.is_intersect(second)


def comparison_to_text(result: int) -> str:
    if result == 0:
        return "Площади равны."
    if result > 0:
        return "Площадь Pentagon больше площади Triangle."
    return "Площадь Triangle больше площади Pentagon."


def main() -> None:
    try:
        pentagon = Pentagon(
            "pent-01",
            [(0, 0), (4, 0), (5, 2), (2.5, 5), (-1, 2)],
        )
        triangle = Triangle("tri-01", [(1, 1), (3, 1), (2, 3.5)])

        print("Созданы объекты:")
        print(pentagon)
        print(triangle)
        print(f"Площадь {pentagon.identifier}: {pentagon.area():.2f}")
        print(f"Площадь {triangle.identifier}: {triangle.area():.2f}")
        print(comparison_to_text(compare(pentagon, triangle)))
        print(f"Есть пересечение: {is_intersect(pentagon, triangle)}")

        triangle.move(6, 0)
        print("\nПосле перемещения Triangle на (6, 0):")
        print(triangle)
        print(f"Есть пересечение: {is_intersect(pentagon, triangle)}")

    except GeometryError as error:
        print(f"Ошибка при работе с корректными объектами: {error}")

    print("\nОбработка исключений:")

    try:
        Triangle("", [(0, 0), (1, 0), (0, 1)])
    except GeometryError as error:
        print(f"1. Ошибка идентификатора: {error}")

    try:
        Triangle("bad-triangle", [(0, 0), (1, 1)])
    except GeometryError as error:
        print(f"2. Ошибка количества вершин: {error}")

    try:
        Pentagon("bad-pentagon", [(0, 0), (3, 0), (1, 2), (2, -1), (0, 2)])
    except GeometryError as error:
        print(f"3. Ошибка геометрии: {error}")

    try:
        pentagon = Pentagon("pent-02", [(0, 0), (4, 0), (5, 2), (2, 5), (-1, 2)])
        pentagon.move("dx", 3)
    except GeometryError as error:
        print(f"4. Ошибка перемещения: {error}")


main()