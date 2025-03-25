import abc
import math
import random
import numpy as np
from typing import Iterable, Self, Generator, Any
import base


ORIGINAL_MAGNITUDE = 2

class LimitedStore:
    def __init__(self,size:int):
        self._size = size
        self._store = []

    def add(self,item):
        self._store.insert(0,item)
        self._store = self._store[:self._size]

    
    def get(self):
        return self._store
    

class Agent:
    def __init__(self, position: base.Vector, velocity: base.Vector):
        self.position = position
        self.velocity = velocity

    def move(self):
        self.position.coordinates += self.velocity.coordinates
        # self.position.x += self.velocity.x
        # self.position.y += self.velocity.y

    def check_bounds(self, max_x: int, max_y: int):
        # Reflect off the boundaries by reversing velocity if out of bounds
        if self.position.x > max_x or self.position.x < 0:
            x = self.velocity.x
            self.velocity.x = -1 * x
        if self.position.y > max_y or self.position.y < 0:
            y = self.velocity.y
            self.velocity.y = -1 * y


    def sense(self,agents:list[Self]) -> Self:

        closest_agent = None
        min_dst = np.inf

        for agent in self._get_non_self_agents(agents):
            dp = agent.position - self.position
            if abs(dp.x) > 100 or abs(dp.y) > 100:
                continue
            cos_theta = measure_cos_theta(self.velocity,dp)
            if cos_theta < 0.5:
                continue

            dst = np.linalg.norm(dp.coordinates)
            if dst < min_dst:
                min_dst = dst
                closest_agent = agent
        
        return closest_agent
    
    def turn(self,target_position,alpha):

        vector_to_target = target_position.coordinates - self.position.coordinates
        new_coordinates = ((1-alpha) * self.velocity.coordinates) + alpha * vector_to_target
        new_magnitude = np.sqrt(np.linalg.norm(new_coordinates))
        self.velocity.coordinates = new_coordinates * (ORIGINAL_MAGNITUDE / new_magnitude)


    def _get_non_self_agents(self,agents:list[Self]) -> Generator[Self, Any, None]:
        
        for agent in agents:
            if agent is not self:
                yield agent
    

    def __str__(self) -> str:
        return f"{self.position},{self.velocity}"
    

def measure_cos_theta(v1:base.Vector,v2:base.Vector) -> float:
    dot_product = np.dot(v1.coordinates,v2.coordinates)
    
    # not calculating the norm if angle is smaller than 0 to save computation
    if dot_product > 0 :
        norm =  np.linalg.norm(v1.coordinates) * np.linalg.norm(v2.coordinates)
    else:
        norm = 1
    return dot_product / norm


class AgentFactory(abc.ABC):

    @abc.abstractmethod
    def build(self,position:base.Vector) -> Agent:
        pass


class RandomVelocityAgentFactory(AgentFactory):

    def build(self,position) -> Agent:

        position = base.Vector(position)
        angle = random.uniform(0,3.14)

        x = ORIGINAL_MAGNITUDE*math.cos(angle)
        y = ORIGINAL_MAGNITUDE*math.sin(angle)
        velocity = base.Vector(np.array([x,y]))
        result = Agent(position,velocity)
        return result
    
class FixedVelocityAgentFactory(AgentFactory):

    def __init__(self,velocity:base.Vector):
        self._velocity = velocity

    def build(self,position:base.Vector) -> Agent:

        position = base.Vector(position.coordinates)
        result = Agent(position,self._velocity)
        return result
    


def make_n_agents(n:int,centre:base.Vector|list[base.Vector],factory:AgentFactory) -> Iterable[Agent]:
    
    assert n > 0

    if isinstance(centre,base.Vector):
        centres = [centre] * n
    elif isinstance(centre,list):
        assert len(centre) == n , "Centres length should equal n"
        centres = centre
    else:
        raise TypeError("centre is expected to be int or list")

    for c in centres:
        yield factory.build(np.array(c.coordinates))


class SpatialGrid:
    def __init__(self, cell_size: int, world_size: tuple[int, int]):
        self.cell_size = cell_size
        self.world_size = world_size
        self.grid = {}

    def _get_cell(self, position: base.Vector) -> tuple[int, int]:
        return int(position.x // self.cell_size), int(position.y // self.cell_size)

    def add_agent(self, agent: Agent):
        cell = self._get_cell(agent.position)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(agent)

    def get_nearby_agents(self, position: base.Vector) -> list[Agent]:
        cell = self._get_cell(position)
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbor_cell = (cell[0] + dx, cell[1] + dy)
                if neighbor_cell in self.grid:
                    neighbors.extend(self.grid[neighbor_cell])
        return neighbors

    def clear(self):
        self.grid.clear()