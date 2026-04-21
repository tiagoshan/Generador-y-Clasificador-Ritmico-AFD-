from .automata_base import AutomataMealy
from .genre_configs import (
    LAMBDA_ROCK, LAMBDA_ROCK_FILL,
    LAMBDA_REGGAETON, LAMBDA_REGGAETON_FILL,
    LAMBDA_HIPHOP, LAMBDA_HIPHOP_FILL,
    LAMBDA_CUMBIA, LAMBDA_CUMBIA_FILL,
)


class RockMealy(AutomataMealy):
    def __init__(self):
        super().__init__(LAMBDA_ROCK, LAMBDA_ROCK_FILL)


class ReggaetonMealy(AutomataMealy):
    def __init__(self):
        super().__init__(LAMBDA_REGGAETON, LAMBDA_REGGAETON_FILL)


class HipHopMealy(AutomataMealy):
    def __init__(self):
        super().__init__(LAMBDA_HIPHOP, LAMBDA_HIPHOP_FILL)


class CumbiaMealy(AutomataMealy):
    def __init__(self):
        super().__init__(LAMBDA_CUMBIA, LAMBDA_CUMBIA_FILL)
