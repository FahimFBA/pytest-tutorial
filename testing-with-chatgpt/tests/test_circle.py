import math

import pytest
import source.shapes as shapes

class TestCircle:

    def setup_method(self, method):
        print(f"Setting up {method}")
        self.circle = shapes.Circle(10)

    def teardown_method(self, method):
        print(f"Tearing down {method}")
        del self.circle

    def test_area(self):
        assert self.circle.area() == math.pi * self.circle.radius ** 2

    def test_one(self):
        assert True

    def test_two(self):
        assert True

    def perimeter(self):
        result = self.circle.perimeter()
        expected_result = 2 * math.pi * self.circle.radius
        assert result == expected_result


    def test_not_same_area_rectangle(self, my_rectangle):
        assert self.circle.area() != my_rectangle.area()