import math

# Семейство ошибок
class VectorError(Exception):
    pass

class VectorDimensionError(VectorError):
    pass

class PointError(Exception):
    pass

# Класс многомерной точки
class Point:
    def __init__(self, coordinates):
        if not isinstance(coordinates, (list, tuple)):
            raise PointError("Координаты должны быть списком или кортежем")
        if not all(isinstance(c, (int, float)) for c in coordinates):
            raise PointError("Все координаты должны быть числами")
        self.coordinates = list(coordinates)

    def __str__(self):
        return f"Point({self.coordinates})"

    def __repr__(self):
        return self.__str__()

# Класс вектора, наследник Point
class Vector(Point):
    def __init__(self, coordinates):
        Point.__init__(self, coordinates)

    def __str__(self):
        return f"Vector({self.coordinates})"

    # Модуль вектора
    def modulus(self):
        return math.sqrt(sum(c ** 2 for c in self.coordinates))

    # Умножение на число
    def multiply_by_scalar(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise VectorError("Можно умножать только на число")
        return Vector([c * scalar for c in self.coordinates])

    # Сумма векторов
    def __add__(self, other):
        if not isinstance(other, Vector):
            raise VectorError("Можно складывать только с другим вектором")
        if len(self.coordinates) != len(other.coordinates):
            raise VectorDimensionError("Размерности векторов не совпадают")
        return Vector([a + b for a, b in zip(self.coordinates, other.coordinates)])

    # Разность векторов
    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise VectorError("Можно вычитать только другой вектор")
        if len(self.coordinates) != len(other.coordinates):
            raise VectorDimensionError("Размерности векторов не совпадают")
        return Vector([a - b for a, b in zip(self.coordinates, other.coordinates)])

    # Скалярное умножение
    def dot(self, other):
        if not isinstance(other, Vector):
            raise VectorError("Можно умножать только на другой вектор")
        if len(self.coordinates) != len(other.coordinates):
            raise VectorDimensionError("Размерности векторов не совпадают")
        return sum(a * b for a, b in zip(self.coordinates, other.coordinates))

    # Проверка равенства
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.coordinates == other.coordinates

    # Коллинеарность
    def is_collinear(self, other):
        if not isinstance(other, Vector):
            raise VectorError("Проверка коллинеарности только между векторами")
        if len(self.coordinates) != len(other.coordinates):
            raise VectorDimensionError("Размерности не совпадают")
        ratios = []
        for a, b in zip(self.coordinates, other.coordinates):
            if b == 0:
                if a != 0:
                    return False
                continue
            ratios.append(a / b)
        # Проверяем, все ли ненулевые элементы имеют одинаковое отношение
        ratios = [r for r in ratios if r is not None]
        if not ratios:
            return True  # оба вектора нулевые или один нулевой
        first_ratio = ratios[0]
        return all(math.isclose(r, first_ratio) for r in ratios)

    # Перпендикулярность
    def is_perpendicular(self, other):
        return math.isclose(self.dot(other), 0, abs_tol=1e-9)

    # Вывод информации
    def print_details(self):
        print(f"Vector: {self.coordinates}")
        print(f"Модуль: {self.modulus()}")
        print(f"Умножение на 3: {self.multiply_by_scalar(3).coordinates}")
        print(f"Сумма с самим собой: {(self + self).coordinates}")
        print(f"Разность с самим собой: {(self - self).coordinates}")
        print(f"Скалярное произведение с самим собой: {self.dot(self)}")
        print(f"Равенство с собой: {self == self}")
        print(f"Коллинеарен с самим собой: {self.is_collinear(self)}")
        print(f"Перпендикулярен с самим собой: {self.is_perpendicular(self)}")

# Демонстрация
try:
    v1 = Vector([1, 2, 3])
    v2 = Vector([4, 5, 6])
    v3 = Vector([2, 4, 6])  # коллинеарен с v1
    v4 = Vector([0, 1, 0])  # перпендикулярен v1

    v1.print_details()
    print()

    print(f"v1 + v2: {(v1 + v2).coordinates}")
    print(f"v1 - v2: {(v1 - v2).coordinates}")
    print(f"Скалярное произведение v1 и v2: {v1.dot(v2)}")
    print(f"v1 равен v1: {v1 == v1}")
    print(f"v1 коллинеарен с v3: {v1.is_collinear(v3)}")
    print(f"v1 перпендикулярен v4: {v1.is_perpendicular(v4)}")
    print()

    # Попытка умножения на не число
    try:
        print(v1.multiply_by_scalar("не число"))
    except VectorError as e:
        print(f"Ошибка при умножении: {e}")

    # Попытка сложения векторов разной размерности
    try:
        v5 = Vector([1, 2])
        print(v1 + v5)
    except VectorDimensionError as e:
        print(f"Ошибка при сложении: {e}")

except VectorError as e:
    print(f"Общая ошибка вектора: {e}")
except PointError as e:
    print(f"Ошибка точки: {e}")