
# R is the diffusion exchange rate between cells of different energy levels
# G is the gravitational constant

# Interesting combos:
# R = 0.0001
# G = 0.01
# R = 0.00035; G = 0.2  # Circuitboard with Clouds
# R = 0.00001; G = 0.2 # Circuitboard
# R = 0.00035; G = 0.0001 # Slowly Cooling
# R = 0.00035; G = 0.1  # Heat Death or Planet
# R = 0.1; G = 0.1  # Cloud, slowly accumulating at the edges
# R = .0011; G = 0.2 # Planets in clouds
# R = .0015; G = 0.2 # Planets in clouds
# R = .0019; G = 0.3 # Disco Nebula
# R = .14; G = 0.374  # Plasma Clouds
# R = .08; G = 0.32 # Spasming bubbles...
# R = .07; G = 0.30  # Curdling liquid
# R = .07; G = 0.305  # Whirling void bubles

# Note to self, a kind of "git bisect"-inspired control would be interesting...
# buttons that say 'good' and 'bad' to find the best values for R and G

MAP_WIDTH = 90
MAP_HEIGHT = 90

SCREENSIZE_MULTIPLIER = max(MAP_WIDTH, MAP_HEIGHT) // 2

SCREEN_WIDTH = MAP_WIDTH * SCREENSIZE_MULTIPLIER
SCREEN_HEIGHT = MAP_HEIGHT * SCREENSIZE_MULTIPLIER

CELL_WIDTH = SCREEN_WIDTH / MAP_WIDTH
CELL_HEIGHT = SCREEN_HEIGHT / MAP_HEIGHT
