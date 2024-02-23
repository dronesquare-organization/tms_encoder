from typing import Tuple, List
from math import dist, atan, pi

import numpy as np
from numpy import inf


class Point:
    """2차원 점"""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.xy = (self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)

    def __xor__(self, point):
        """
        - 두 point 사이의 최단 거리를 구하는 연산자입니다.
        - 사용법: p1 ^ p2
        """
        if not isinstance(point, Point):
            raise Exception
        return dist(self.xy, point.xy)

    def __repr__(self) -> str:
        return f"<Point x={self.x}, y={self.y}>"


class Line:
    """2차원 선분"""

    def __init__(self, p1: Point, p2: Point):
        if not (isinstance(p1, Point) and isinstance(p2, Point)):
            raise Exception
        self.is_valid = not (p1.x == p2.x and p1.y == p2.y)
        self.p1 = p1.copy()
        self.p2 = p2.copy()

    def copy(self):
        return Line(self.p1.copy(), self.p2.copy())

    @property
    def slope(self) -> float:
        """선분의 기울기, y=ax+b 에서의 a"""
        x_delta = self.p2.x - self.p1.x
        y_delta = self.p2.y - self.p1.y
        if x_delta == 0:
            return inf  # 수직선은 기울기가 무한대
        return y_delta / x_delta

    @property
    def intercept(self) -> float:
        """선분의 절편, y=ax+b 에서의 b"""
        # b = y-ax
        return self.p1.y - (self.slope * self.p1.x)  # 수직선은 -무한대

    @property
    def angle(self) -> float:
        """선분의 기울기 각도 (범위: 0 ~ 90 )"""

        # 직각삼각형에서 각 축의 길이
        x_delta = abs(self.p1.x - self.p2.x)
        y_delta = abs(self.p1.y - self.p2.y)
        if x_delta == 0:
            return 90.0  # 수직선은 90도
        return atan(y_delta / x_delta) * (180 / pi)

    @property
    def length(self) -> float:
        """선분의 길이"""
        # 두 점의 최단거리
        return self.p1 ^ self.p2

    def inner_points(self, step: float = 1) -> List[Point]:
        """
        - 선을 따라 일정 간격을 가지는 점(Point)들을 담은 리스트를 반환합니다.
        - step : 점 사이의 간격(미터)
        """
        # p2 - p1 을 해야 부호 방향이 p1 -> p2가 됌
        x_delta = self.p2.x - self.p1.x
        y_delta = self.p2.y - self.p1.y

        if x_delta == 0:  # x축 기준으로 계산하므로 수직선은 따로 처리
            delta = step if y_delta > 0 else -step
            y_list = list(np.arange(self.p1.y, self.p2.y, delta))
            if y_list[-1] != self.p2.y:
                y_list.append(self.p2.y)
            return [Point(self.p1.x, y) for y in y_list]

        # 점 간격과 선 길이의 비율
        ratio = step / self.length

        # x축 y축에 위 비율을 적용
        x_step = x_delta * ratio
        y_step = y_delta * ratio

        inner_x, inner_y = self.p1.xy

        inner_point_list = []
        while (inner_x < self.p2.x) if x_delta > 0 else (inner_x > self.p2.x):
            # 범위 안에서 step 간격으로 Point를 넣습니다.
            inner_point_list.append(Point(x=inner_x, y=inner_y))
            inner_x += x_step
            inner_y += y_step
        # 마지막으로 끝점(p2)을 넣습니다.
        inner_point_list.append(Point(x=self.p2.x, y=self.p2.y))

        return inner_point_list

    def direction(self) -> Tuple[float, float]:
        return (self.p2.x - self.p1.x) / self.length, (
            self.p2.y - self.p1.y
        ) / self.length

    def perpendicular_direction(
        self,
    ) -> Tuple[float, float]:  # 수직선의 기울기 = - 선분의 기울기
        ux, uy = self.direction()
        return -uy, ux

    def __repr__(self) -> str:
        return f"<Line p1={self.p1}, p2={self.p2}>"


class Polygon:
    """2차원 다각형"""

    def __init__(self, *points: Point):
        self.points = [p.copy() for p in points]
        if self.area < 0:  # 시계 반대방향이어햐 한다.
            self.points.reverse()

        self.lines = []
        p1 = self.points[-1]
        for p2 in self.points:  # 시계 반대방향 정렬 보장
            self.lines.append(Line(p1, p2))
            p1 = p2

    def copy(self):
        return Polygon(*self.points)

    @property
    def is_valid(self) -> bool:
        """다각형을 구성하는 선분이 겹치면 False"""

        def ccw(p1, p2, p3):
            """
            - 2차원 평면에서 CCW 계산
            - p1, p2, p3을 이용하여 공식 계산
            - https://snowfleur.tistory.com/98
            """
            return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

        segments = [
            (self.points[i], self.points[(i + 1) % len(self.points)])
            for i in range(len(self.points))
        ]  # 입력받은 점들이 이루는 선분을 저장하는 리스트.

        for i in range(len(segments)):  # 각 선분들의 교차점 확인.
            for j in range(i + 1, len(segments)):
                p1, p2 = segments[i]  # a, b
                q1, q2 = segments[j]  # c, d
                if (
                    ccw(p1, p2, q1) * ccw(p1, p2, q2) < 0
                    and ccw(q1, q2, p1) * ccw(q1, q2, p2) < 0
                ):  # i번째 선분 p1-p2(a-b)와 j번째 선분 q1-q2(c-d)
                    return False
        return True  # 교차점이 없음

    @property
    def area(self):
        max_idx = len(self.points) - 1
        for idx, point in enumerate(self.points):
            # 시계 반대방향이라고 가정하고 그래프 구조를 만든다.
            left_idx = left if (left := idx + 1) <= max_idx else 0
            point.left = self.points[left_idx]

        a = sum([obj.x * obj.left.y for obj in self.points])
        b = sum([obj.y * obj.left.x for obj in self.points])

        return (a - b) / 2

    def __contains__(self, point: Point):
        """
        - 포인트가 다각형 내부에 위치하는지 판별하는 in 연산자 구현
        - Point(...) in Polygon(...) -> bool
        """
        # https://bowbowbow.tistory.com/24 다각형 내부 판별 알고리즘
        right_intersection = 0
        for line in self.lines:
            # 점의 y가 선분 양 끝 y사이에 있으면 점에서 x축으로 뻗는 직선은 무조건 선분과 접함
            if line.p1.y <= point.y <= line.p2.y:
                # 반직선이 오른쪽에서 접하는지는 여기서 판별
                if (
                    line.slope == 0 or line.slope == inf
                ):  # 선분이 수평이거나 수직인 경우
                    if point.x < line.p1.x and point.x < line.p2.x:
                        right_intersection += 1
                    continue  # 이렇게 안하면 0으로 나누고 에러뜸
                if point.x <= (point.y - line.intercept) / line.slope:
                    # (점의 x) <= (선분이 점과 동일한 y값일 때의 x)
                    right_intersection += 1
        return True if 1 == right_intersection % 2 else False

    def __repr__(self) -> str:
        return f"<Polygon {self.points}>"
