# A nebula simulator

I "programmed" a nebula that evolves with every calculated frame. It features stars, gas clouds, and even pockets of empty space.


Surprisingly, however, I did not program the nebula, the stars, or the gas clouds or the empty space.


I only programmed a handful of simple rules, and these objects emerged spontaneously by themselves. 


This is the power of emergent properties.


Here are the 3 rules I defined in order to create the simulation:


0) The world is a 2D array of cells. Each cell contains energy that is represented as a decimal from 0.0 to 1.0.


1) Conservation of energy: the amount of energy in the system should not increase or decrease.


2) Energy diffusion: like in the real world, energy has a tendency to go from high-energy areas to low-energy areas.


3) Gravity: Every cell exerts a pull on every other cell. The force of the pull increases with the amount of energy the cell contains.


And voila. It's full of stars.


I'm as surprised as you are.


It's a beautiful world we live in, where a number of simple agents can work together to create complex, beautiful, powerful things. Things that were never planned or scripted, but arise anyway, almost as if by magic.


The whole is greater than the sum of its parts.


Like a team. Or a household. Or an army of autonomous killer drones driven by multimodal LLM agents.


Perfection.


Nerdy stuff: This is a 2D cellular automaton, like Conway's Game of Life. I used fast fourier transform to calculate the gravitational forces, and I wrote a custom diffusion algorithm that respects the conservation of energy. Pygame does the rendering. Took me ~1 day to write from scratch, starting with just my imagination.

# How to run

```bash
pip install -r requirements.txt
python simulation.py
```

