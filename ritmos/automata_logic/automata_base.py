# ritmos/automata_logic/automata_base.py

class AutomataMealy:
    """
    Implementa la lógica de una Máquina de Mealy genérica.
    Maneja el estado interno y la lógica de transición/salida.
    """
    def __init__(self, lambda_table):
        # La tabla lambda (la lista de salidas, ej: LAMBDA_ROCK)
        self.lambda_table = lambda_table
        
        # El número de estados se infiere de la longitud de la tabla
        self.num_estados = len(lambda_table)
        
        # El estado inicial (siempre 0)
        self.estado_actual = 0

    def get_next_output(self):
        """
        Calcula la salida para el estado actual y luego transiciona 
        al siguiente estado.
        """
        
        # 1. Obtener la salida (el instrumento) del estado actual
        #    (En Mealy, la salida está en la *transición*, 
        #    así que usamos el estado actual como índice)
        output = self.lambda_table[self.estado_actual]
        
        # 2. Transicionar al siguiente estado (Función Delta: (q + 1) % N)
        #    Usamos el módulo (%) para el bucle (ej: 15 + 1 = 16 % 16 = 0)
        self.estado_actual = (self.estado_actual + 1) % self.num_estados
        
        # 3. Retornar el símbolo de salida (ej: 'B', 'C', 'H', '-')
        return output

    def reset(self):
        """ Reinicia el autómata a su estado inicial. """
        self.estado_actual = 0

# ritmos/automata_logic/automata_base.py

# ... (Clase AutomataMealy arriba) ...

class AutomataAceptador:
    """
    Clase base para un AFD Aceptador.
    Recorre una cadena de entrada y decide si es válida.
    """
    def __init__(self, delta, q0, F):
        self.delta = delta       # Diccionario de transiciones
        self.q0 = q0             # Estado inicial
        self.F = F               # Conjunto de estados finales (aceptación)
        self.estado_actual = q0

    def analizar_cadena(self, cadena: str) -> bool:
        self.estado_actual = self.q0
        
        # Limpiamos la cadena para que sea una lista de símbolos
        # Si viene como "B-H-C", separamos por guiones si es necesario,
        # o asumimos que la cadena es iterable.
        # Aquí asumiremos que el input puede ser una lista o string.
        
        # Si es un string largo con guiones, lo partimos
        if isinstance(cadena, str) and '-' in cadena:
             simbolos = cadena.split('-')
        else:
             simbolos = list(cadena)

        for simbolo in simbolos:
            # Limpieza básica (quitar espacios vacíos)
            simbolo = simbolo.strip()
            if not simbolo: continue

            # Lógica de Transición
            # Verificamos si existe una transición para este símbolo desde el estado actual
            if self.estado_actual in self.delta:
                if simbolo in self.delta[self.estado_actual]:
                    # AVANZAR: Hay una flecha explícita
                    self.estado_actual = self.delta[self.estado_actual][simbolo]
                
                # NOTA DE DISEÑO:
                # Si el símbolo NO está en el diccionario, ¿qué hacemos?
                # Opción A: Ir a un estado de error implícito (Rechazo inmediato).
                # Opción B: Ignorarlo (quedarse en el mismo sitio).
                # Para este clasificador robusto, usaremos Opción B (Ignorar relleno).
                # Solo avanzamos si detectamos los golpes CLAVE.
            
        # Al finalizar la cadena, ¿estamos en un estado final?
        return self.estado_actual in self.F