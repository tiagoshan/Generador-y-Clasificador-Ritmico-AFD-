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
        # la decisión se toma justo antes de entrar al estado 12 que es el último cuarto
        if self.estado_actual == 12 and not self.en_modo_fill:
            # 20% de probabilidad de meter un fill
            if random.random() < 0.2:
                self.en_modo_fill = True
                self.indice_fill = 0
                # La variación dura 4 pasos 
                self.pasos_fill_restantes = 4 

        # calcula salida
        output = ""
        
        if self.en_modo_fill:
            
            output = LAMBDA_ROCK_FILL[self.indice_fill]
            
            
            self.indice_fill += 1
            self.pasos_fill_restantes -= 1
            
            self.estado_actual = (self.estado_actual + 1) % self.num_estados
            
            # cuando acaba el fill sale
            if self.pasos_fill_restantes == 0:
                self.en_modo_fill = False
                
        else:
            # sin fill
            output = super().get_next_output()

        return output

    def generar_secuencia(self, pasos: int):
        # lista en lugar de string para instrumentos simultaneos
        secuencia_completa = []
        self.reset() 
        
        for _ in range(pasos):
            simbolo = self.get_next_output()
            secuencia_completa.append(simbolo)
        
        return secuencia_completa

class ReggaetonMealy(AutomataMealy):
    def __init__(self):
        super().__init__(lambda_table=LAMBDA_REGGAETON)
        # variables para el control de variación
        self.en_modo_fill = False
        self.pasos_fill_restantes = 0
        self.indice_fill = 0

    def get_next_output(self):

        if self.estado_actual == 12 and not self.en_modo_fill:
            # 20% de probabilidad de variación
            if random.random() < 0.2:
                self.en_modo_fill = True
                self.indice_fill = 0
                self.pasos_fill_restantes = 4

        output = ""
        
        if self.en_modo_fill:
            # fill o corte
            output = LAMBDA_REGGAETON_FILL[self.indice_fill]
            
            self.indice_fill += 1
            self.pasos_fill_restantes -= 1
            self.estado_actual = (self.estado_actual + 1) % self.num_estados
            
            if self.pasos_fill_restantes == 0:
                self.en_modo_fill = False
        else:
            # dembow
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
        if self.estado_actual == 12 and not self.en_modo_fill:
            # 20% de probabilidad de variación
            if random.random() < 0.2:
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