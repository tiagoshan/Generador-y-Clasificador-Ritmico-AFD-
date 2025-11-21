class AutomataMealy:
    
    # Implementa la lógica de una Máquina de Mealy genérica.
    
    def __init__(self, lambda_table):
        # la lista de salidas
        self.lambda_table = lambda_table
        
        # El número de estados se infiere de la longitud de la tabla
        self.num_estados = len(lambda_table)
        
        # El estado inicial (siempre 0)
        self.estado_actual = 0

    def get_next_output(self):
        
        # Calcula la salida para el estado actual y luego transiciona 
        
        
        # obtener el instrumento del estado actual
        # estado actual como índice
        output = self.lambda_table[self.estado_actual]
        
        # transicionar al siguiente estado Función Delta: (q + 1) % N
        self.estado_actual = (self.estado_actual + 1) % self.num_estados
        
        # Retornar el símbolo de salida
        return output

    def reset(self):
        # reinicia el autómata a su estado inicial. 
        self.estado_actual = 0

class AutomataAceptador:
    
    # clase base para un AFD Aceptador. Recorre una cadena de entrada y decide si es válida.
    
    def __init__(self, delta, q0, F):
        self.delta = delta       # Diccionario de transiciones
        self.q0 = q0             # Estado inicial
        self.F = F               # Conjunto de estados finales (aceptación)
        self.estado_actual = q0

    def analizar_cadena(self, cadena: str) -> bool:
        self.estado_actual = self.q0

        
        # es un string largo con guiones o silencios, se parte
        if isinstance(cadena, str) and '-' in cadena:
             simbolos = cadena.split('-')
        else:
             simbolos = list(cadena)

        for simbolo in simbolos:
            # limpieza
            simbolo = simbolo.strip()
            if not simbolo: continue

            # transición
            # se ve si existe una transición para este símbolo desde el estado actual
            if self.estado_actual in self.delta:
                if simbolo in self.delta[self.estado_actual]:
                    # hay una flech
                    self.estado_actual = self.delta[self.estado_actual][simbolo]
                
        return self.estado_actual in self.F