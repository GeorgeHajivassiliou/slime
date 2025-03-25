import pygame
import numpy as np
import time
import argparse
from typing import Iterable
import base
import objects
import pygame_interactions




class SlimeMoldSimulation:

    def __init__(self,game_engine:base.GameEngineGateway):
        self._game_engine = game_engine
        self._agents: list[objects.Agent] = []
        self._shape = (720, 720)
        self._grid = objects.SpatialGrid(70, self._shape)
        self._plotted_points = []
        self._agent_positions:list[objects.LimitedStore] = []
        self._circle_factory =  base.CircleFactory(2,(255, 255, 255))
        self._n_steps = 0


    def start(self,n_agents):

        start = base.Vector(np.array([d/2 for d in self._shape]))
        self._game_engine.make_world(self._shape)

        for agent in objects.make_n_agents(n_agents,start,objects.RandomVelocityAgentFactory()):
            self._agents.append(agent)
            self._agent_positions.append(objects.LimitedStore(100))


    def _run_one_timestep(self):

        self._n_steps += 1

        for i,agent in enumerate(self._agents):
            agent.move()
            agent.check_bounds(*self._shape)
            self._grid.add_agent(agent)

        for i,agent in enumerate(self._agents):
            nearby_agents = self._grid.get_nearby_agents(agent.position)

            if (self._n_steps+i) % 5 == 0:
                target_agent = agent.sense(nearby_agents)

                if target_agent is not None:
                    agent.turn(target_agent.position,10)

            self._agent_positions[i].add(tuple(agent.position))


        self._grid.clear()

        all_circles = []
        for agent_positions in self._agent_positions:
            positions = agent_positions.get()
            alpha_range = np.linspace(255,0,len(positions))
            radii = np.linspace(2,3,len(positions))
            circles = [self._circle_factory.build(p,a,r) for p,a,r in zip(positions,alpha_range,radii)]
            all_circles.extend(circles)

        self._game_engine.update_circles(all_circles)

    def try_running_one_timestep(self):
        try: 
            self._run_one_timestep()
        except base.UserHasQuitException:
            pygame.quit()


if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--time_it",action="store_true")
    args = args.parse_args()
    game_engine_gateway = pygame_interactions.GameEngineGateway()
    game = SlimeMoldSimulation(game_engine_gateway)
    game.start(300)


    if args.time_it:
        start = time.time()
        for _ in range(100):
            game.try_running_one_timestep()
        end = time.time()
        print(f"Time taken: {end-start}")

    else:

        while True:
            game.try_running_one_timestep()
