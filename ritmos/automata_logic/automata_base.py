import random

FILL_TRIGGER_STATE = 12
FILL_PROBABILITY = 0.2
FILL_DURATION = 4


class AutomataMealy:
    def __init__(self, lambda_table, fill_table=None):
        self.lambda_table = lambda_table
        self.fill_table = fill_table
        self.num_estados = len(lambda_table)
        self.estado_actual = 0
        self._en_fill = False
        self._fill_restantes = 0
        self._fill_idx = 0

    def get_next_output(self):
        if (self.fill_table
                and self.estado_actual == FILL_TRIGGER_STATE
                and not self._en_fill
                and random.random() < FILL_PROBABILITY):
            self._en_fill = True
            self._fill_idx = 0
            self._fill_restantes = FILL_DURATION

        if self._en_fill:
            output = self.fill_table[self._fill_idx]
            self._fill_idx += 1
            self._fill_restantes -= 1
            self.estado_actual = (self.estado_actual + 1) % self.num_estados
            if self._fill_restantes == 0:
                self._en_fill = False
        else:
            output = self.lambda_table[self.estado_actual]
            self.estado_actual = (self.estado_actual + 1) % self.num_estados

        return output

    def generar_secuencia(self, pasos: int):
        self.reset()
        return [self.get_next_output() for _ in range(pasos)]

    def reset(self):
        self.estado_actual = 0
        self._en_fill = False
        self._fill_restantes = 0
        self._fill_idx = 0


class AutomataAceptador:
    def __init__(self, delta, q0, F):
        self.delta = delta
        self.q0 = q0
        self.F = F
        self.estado_actual = q0

    def analizar_cadena(self, cadena) -> bool:
        self.estado_actual = self.q0

        if isinstance(cadena, list):
            simbolos = cadena
        elif '-' in cadena:
            simbolos = cadena.split('-')
        else:
            simbolos = list(cadena)

        for simbolo in simbolos:
            if isinstance(simbolo, str):
                simbolo = simbolo.strip()
            if not simbolo or simbolo == '-':
                continue
            transitions = self.delta.get(self.estado_actual, {})
            if simbolo in transitions:
                self.estado_actual = transitions[simbolo]

        return self.estado_actual in self.F
