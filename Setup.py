from os import environ

# hide the pyGame startup commercial
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# make pyGame (SDL) behave better when desktop scaling enabled
environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
