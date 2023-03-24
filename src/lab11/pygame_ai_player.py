""" Create PyGameAIPlayer class here"""
import pygame
from lab11.turn_combat import CombatPlayer
import random
import time

class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    def selectAction(self, state):
        nextCity = random.randint(48,57)
        return nextCity


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
        while True:
            
            self.weapon = random.randint(0,2)
            time.sleep(1)
            return self.weapon
                    