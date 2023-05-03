# AI Final Project

## Abstract

When agent_environment.py is run it will attempt to call an API for Stable Diffusionv1.5 using my API key. This will generate an image of the player's choosing to be the player character for that playthrough of the game. If the API doesn't generate a successful image it will just use the last image that is saved. The program will then create an initial map of cities and run it through a Genetic Algorithm to find the best map where the cities are equally spaced and placed realistically. The game will generate random routes between the cities and let the player travel between the routes to get try and get to the final city. As the player is traveling to different cities, there is a chance that the player will enter combat with a bandit. In combat, the player can choose between sword, arrow, or fire and try to beat the bandit. If the player loses then the bandit will take some of their gold. But if the player wins, then they will take some gold from the bandit. If the player reaches the final city then the game will end, with the player winning. But if the player loses all their gold either from traveling or losing to a bandit, then the game will end with the player will lose.

## AI components
<ol>
	<li> Text to Image Generation
	<li>Perlin Noise
	<li>Genetic Algorithm
	<li>Optional AI Player
</ol>


## Problems Solved

Making this game brings up lots of challenges and issues. Firstly I wanted every experience to be different for every player or playthrough. I also wanted to make sure my game map wasn't just an flat map that has cities randomly placed on it. Lastly, I wanted the player to be able to choose for an AI to play the game for them. Luckily, I was able to solve all of these issues with AI or AI techniques, like text to image generation, Perlin noise, and genetic algorithm.

Text to image generation allowed for the user to customize their experience every time they play the game. For example if the player wants to play as a well-armored knight they can. This AI gives the player more freedom in how they want their game and world to play out.

Generating a map was the next issue. For that the Perlin noise algorithm was used to generate a random map and then another library was used to convert it to a heat map. The Perlin noise algorithm works by applying pseudo-random changes to a variable to generate different looks around the image. The Perlin noise image is used as the background for the fighting scene when the player finds a bandit. When the heat map is generated it is used as the game map, but when cities are added it brings up the issue of poorly placed cities. For example, cities might be in the lake or on mountains.

In order to make the city placement realistic the genetic algorithm was used. The Genetic Algorithm takes in the world then runs it through the algorithm to try and make it as realistic as possible. This is so the player doesn't have all their cities clumped together or in the middle of lakes or mountains. It does this by using a fitness function that improves the fitness of cities that aren't close together and are in between a certain height range. The final result is always better than the initial map although the player will only ever see the final result.

There is also an optional AI player that will play the whole game including the combat if the player wishes. This will randomly select a city to travel to until it finds a city that is connected. If the combat player AI is also enabled then the AI will also fight the bandit using a random number to try and beat the bandit. This will continue until the player either wins or loses. Although this option is available, it requires the player to go into two files and change a few lines of code, so it is not recommended unless you know what you are doing. More info can be found in the #Running the Game section.

## Running the Game

In order to start the game, run the agent_environment.py. This will ask you in the console for a description of what you want your character to look like. Once that image is generated it will be saved as character.png under the assets folder. The world will then be generated and displayed. Now you can press a number 1-9 and it will attempt to move you to that city if it is connected via a path. As you are traveling, you might encounter a bandit. Encountering a bandit will initiate battle with, all of the battle details will be displayed in the console. Press either S, A, or F to use sword, arrow, or fire respectively. Whoever gets to 0 health will lose. If you win then you will take some of the bandit's gold to be able to travel to more places. However, if you lose then the bandit will rob you and take some of your gold. If you run out of gold then the game is over, but if you find and reach the end city before that happens then you win.

In order to activate the AI player, you need to go into agent_environment.py and uncomment ```#player = PyGameAIPlayer()``` in line 170. This will make it so an AI player moves the character around the map. If you want the AI to also fight the bandit for you, then you will need to go to pygame_combat.py. There you will need to uncomment line 57, ``player = PyGameAICombatPlayer("Legolas")``. You can choose to do either of these or just one if wanted.


## Appendix
Prompt:
	
	  
	how can i get a pygame.Surface from a numpy.ndarray in python

Answer:
		
	import pygame
	import numpy as np

	# Create a 2D numpy.ndarray
	array = np.array([[0, 0, 0], [255, 0, 0], [0, 255, 0]])

	# Create a pygame.Surface object from the numpy.ndarray
	surface = pygame.surfarray.make_surface(array)

	# Display the pygame.Surface object
	pygame.display.set_mode((300, 300))
	pygame.display.blit(surface, (0, 0))
	pygame.display.update()

	# Keep the game running until the user quits
	while True:
	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
	            break

	pygame.quit()


