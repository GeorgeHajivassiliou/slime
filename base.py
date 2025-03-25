import abc
import numpy as np
from typing import Self, Iterable
class Vector:

    def __init__(self,coordinates:Iterable):

        assert isinstance(coordinates,np.ndarray)
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]


    def __iter__(self):

        yield self.x
        yield self.y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"
    
    def __sub__(self,other) -> Self:

        result = Vector(self.coordinates - other.coordinates)
        return result
    
    @property
    def x(self) -> float:
        return self.coordinates[0]
    @x.setter
    def x(self,value:float):
        self.coordinates[0] = value
    
    @property
    def y(self) -> float:
        return self.coordinates[1]
    
    @y.setter
    def y(self,value:float) :
        self.coordinates[1] = value


class UserHasQuitException(Exception):
    pass

class Circle:

    def __init__(self, centre: tuple[int, int], radius, colour, alpha):
        self.centre = centre
        self.radius = radius
        self.colour = colour
        self.alpha = alpha


class CircleFactory:

    def __init__(self, radius, colour):
        self._radius = radius
        self._colour = colour

    def build(self,centre,alpha,radius=None) -> Circle:
        if radius is None:
            radius = self._radius
        result = Circle(centre,radius,self._colour,alpha)
        return result


class GameEngineGateway(abc.ABC):
    @abc.abstractmethod
    def make_world(self,shape:tuple):
        pass

    @abc.abstractmethod
    def update_circles(self,circles:list[Circle]):
        pass
    @abc.abstractmethod
    def get_keyboard_displacement(self,step) -> tuple[float,float]:
        pass


