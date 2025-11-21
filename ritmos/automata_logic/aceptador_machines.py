from .automata_base import AutomataAceptador
from .genre_configs import (
    DELTA_ROCK_ACEPTADOR, 
    Q_ROCK_0, 
    Q_ROCK_F
)

class RockAceptador(AutomataAceptador):
    
    # AFD que reconoce patrones de Rock.

    
    def __init__(self):
        super().__init__(
            delta=DELTA_ROCK_ACEPTADOR,
            q0=Q_ROCK_0,
            F={Q_ROCK_F} # Conjunto de estados finales
        )