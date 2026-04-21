from .automata_base import AutomataAceptador
from .genre_configs import (
    DELTA_ROCK_ACEPTADOR, Q_ROCK_0, Q_ROCK_F,
    DELTA_REGGAETON_ACEPTADOR, Q_REGGAETON_0, Q_REGGAETON_F,
    DELTA_HIPHOP_ACEPTADOR, Q_HIPHOP_0, Q_HIPHOP_F,
    DELTA_CUMBIA_ACEPTADOR, Q_CUMBIA_0, Q_CUMBIA_F,
)


class RockAceptador(AutomataAceptador):
    def __init__(self):
        super().__init__(DELTA_ROCK_ACEPTADOR, Q_ROCK_0, {Q_ROCK_F})


class ReggaetonAceptador(AutomataAceptador):
    def __init__(self):
        super().__init__(DELTA_REGGAETON_ACEPTADOR, Q_REGGAETON_0, {Q_REGGAETON_F})


class HipHopAceptador(AutomataAceptador):
    def __init__(self):
        super().__init__(DELTA_HIPHOP_ACEPTADOR, Q_HIPHOP_0, {Q_HIPHOP_F})


class CumbiaAceptador(AutomataAceptador):
    def __init__(self):
        super().__init__(DELTA_CUMBIA_ACEPTADOR, Q_CUMBIA_0, {Q_CUMBIA_F})
