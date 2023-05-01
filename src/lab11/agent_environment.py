import sys
import pygame
import random
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer
import numpy as np

from pathlib import Path

# from diffusers import StableDiffusionPipeline
# import torch
import requests

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes
from lab7.ga_cities import setup_GA, solution_to_cities, show_cities, game_fitness
from src.lab5.landscape import elevation_to_rgba

from src.lab5.landscape import get_elevation

pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])

def isConnected(cities, routes, city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]

    for route in routes:
        if (x1, y1) in route and (x2, y2) in route:
            return True
        
    return False


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    n_cities = 10

    playerInput = input("What do you want your character to look like: ")
    actualInput = playerInput + " ,transparent background"
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    image_bytes = query({
        "inputs": actualInput,
    })

    import io
    from PIL import Image

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.save("assets\character.png")

    except:
        print("Error, Using last image")


    sprite_path = "assets/character.png"
    sprite_speed = 1

    elevation_start = get_elevation(size)
    elevation = np.array(elevation_start)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape_pic = elevation_to_rgba(elevation)

    fitness = lambda cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )

    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    cities_t = ga_instance.initial_population[0]
    cities_t = solution_to_cities(cities_t, size)
    ga_instance.run()
    cities_t = ga_instance.best_solution()[0]
    cities = solution_to_cities(cities_t, size)
    cities = map(tuple,cities)
    cities = tuple(cities)

    screen = setup_window(width, height, "Game World Gen Practice")


    landscape= elevation_to_rgba(get_elevation(size))
    landscape_surface = pygame.surfarray.make_surface(landscape)
    #landscape_surface = get_landscape_surface(size)
    
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    #cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]
    
    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    #player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )
    money = 10
    while True:
        #print("Current Money: ", money)
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if money < 0:
                print("You ran out of money. Game Over!")
                break
            
            if int(chr(action)) != state.current_city and not state.travelling:

                if isConnected(cities, routes,state.current_city,int(chr(action))):
                    start = cities[state.current_city]
                    state.destination_city = int(chr(action))
                    destination = cities[state.destination_city]
                    
                    player_sprite.set_location(cities[state.current_city])
                    state.travelling = True
                    print(
                        "Travelling from", state.current_city, "to", state.destination_city
                    )

                    print("Current Balance", money)
                    if elevation[destination[0]][destination[1]] < .45:
                        print("Travel cost is 1")
                        money-=1
                    elif elevation[destination[0]][destination[1]] < .65:
                        print("Travel cost is 2")
                        money-=2
                    else:
                        print("Travel cost is 3")
                        money-=3
                    
                    
                    print("New Total is ", money)
                else:
                    print("Not connected")

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            result = run_pygame_combat(combat_surface, screen, player_sprite)
            if result == -1:
                coins = random.randint(1,3)
                print("You lost", coins, "coins the the bandit")
                money-=coins
                print("You now have", money, "gold")
            elif result == 1:
                coins = random.randint(1,4)
                print("You got", coins, "from defeating the bandits")
                money+=coins
                print("You now have", money, "gold")
            
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
        if money == 0:
            print('You have ran out of money and lost')
            break
