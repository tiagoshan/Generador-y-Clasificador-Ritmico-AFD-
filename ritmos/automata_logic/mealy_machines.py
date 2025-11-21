# ritmos/automata_logic/mealy_machines.py

import random
from .automata_base import AutomataMealy
from .genre_configs import (
    LAMBDA_ROCK, LAMBDA_ROCK_FILL, 
    LAMBDA_REGGAETON, LAMBDA_REGGAETON_FILL,
    LAMBDA_HIPHOP, LAMBDA_HIPHOP_FILL
)

class RockMealy(AutomataMealy):
    def __init__(self):
        super().__init__(lambda_table=LAMBDA_ROCK)
        self.en_modo_fill = False
        self.pasos_fill_restantes = 0
        self.indice_fill = 0

    def get_next_output(self):
        # 1. Lógica de Bifurcación (Probabilidad)
        # La decisión se toma justo antes de entrar al estado 12 (el último cuarto)
        if self.estado_actual == 12 and not self.en_modo_fill:
            # 30% de probabilidad de hacer una variación
            if random.random() < 0.3:
                self.en_modo_fill = True
                self.indice_fill = 0
                # La variación dura 4 pasos (sustituye q12, q13, q14, q15)
                self.pasos_fill_restantes = 4 

        # 2. Calcular Salida
        output = ""
        
        if self.en_modo_fill:
            # Estamos en el camino alternativo (Abajo en tu diagrama)
            output = LAMBDA_ROCK_FILL[self.indice_fill]
            
            # Avanzar contadores del fill
            self.indice_fill += 1
            self.pasos_fill_restantes -= 1
            
            # Avanzar el estado "fantasma" para mantener sincronía
            self.estado_actual = (self.estado_actual + 1) % self.num_estados
            
            # Si terminamos el fill, apagar el modo
            if self.pasos_fill_restantes == 0:
                self.en_modo_fill = False
                
        else:
            # Estamos en el camino normal (Arriba en tu diagrama)
            # Usamos la lógica normal de la clase padre
            output = super().get_next_output()

        return output

    def generar_secuencia(self, pasos: int):
        """
        Sobreescribimos este método para devolver una LISTA, no un string.
        Esto es necesario para manejar símbolos como 'HB'.
        """
        secuencia_completa = []
        self.reset() # Asegurar empezar desde 0
        
        for _ in range(pasos):
            simbolo = self.get_next_output()
            secuencia_completa.append(simbolo)
        
        # Retornamos la lista directa (Ej: ["HB", "-", "H", ...])
        return secuencia_completa

# (La clase ReggaetonMealy se queda igual, pero asegúrate de que 
# generar_secuencia devuelva lista si la vas a usar)
class ReggaetonMealy(AutomataMealy):
    def __init__(self):
        # Inicializar con el patrón base
        super().__init__(lambda_table=LAMBDA_REGGAETON)
        # Variables para el control de variación
        self.en_modo_fill = False
        self.pasos_fill_restantes = 0
        self.indice_fill = 0

    def get_next_output(self):
        # 1. Lógica de Bifurcación
        # En el estado 12 decidimos si hacemos un "Corte" de Reggaeton
        if self.estado_actual == 12 and not self.en_modo_fill:
            # 25% de probabilidad de variación
            if random.random() < 0.25:
                self.en_modo_fill = True
                self.indice_fill = 0
                self.pasos_fill_restantes = 4

        output = ""
        
        if self.en_modo_fill:
            # Camino Alternativo (El Corte)
            output = LAMBDA_REGGAETON_FILL[self.indice_fill]
            
            self.indice_fill += 1
            self.pasos_fill_restantes -= 1
            self.estado_actual = (self.estado_actual + 1) % self.num_estados
            
            if self.pasos_fill_restantes == 0:
                self.en_modo_fill = False
        else:
            # Camino Normal (Dembow)
            output = super().get_next_output()

        return output

    def generar_secuencia(self, pasos: int):
        secuencia_completa = []
        self.reset()
        for _ in range(pasos):
            simbolo = self.get_next_output()
            secuencia_completa.append(simbolo)
        return secuencia_completa
    
class HipHopMealy(AutomataMealy):
    def __init__(self):
        super().__init__(lambda_table=LAMBDA_HIPHOP)
        self.en_modo_fill = False
        self.pasos_fill_restantes = 0
        self.indice_fill = 0

    def get_next_output(self):
        # Lógica de Bifurcación
        if self.estado_actual == 12 and not self.en_modo_fill:
            # 25% de probabilidad de variación
            if random.random() < 0.25:
                self.en_modo_fill = True
                self.indice_fill = 0
                self.pasos_fill_restantes = 4

        output = ""

        if self.en_modo_fill:
            output = LAMBDA_HIPHOP_FILL[self.indice_fill]
            self.indice_fill += 1
            self.pasos_fill_restantes -= 1
            self.estado_actual = (self.estado_actual + 1) % self.num_estados

            if self.pasos_fill_restantes == 0:
                self.en_modo_fill = False
        else:
            output = super().get_next_output()

        return output

    def generar_secuencia(self, pasos: int):
        secuencia_completa = []
        self.reset()
        for _ in range(pasos):
            secuencia_completa.append(self.get_next_output())
        return secuencia_completa