# ritmos/automata_logic/genre_configs.py

# --- Constantes de Símbolos ---
BOMBO = 'B'
CAJA = 'C'
HIHAT = 'H'
SILENCIO = '-'

# Nuevos Símbolos Combinados
HIHAT_BOMBO = 'HB'  # Suenan a la vez
HIHAT_CAJA = 'HC'   # Suenan a la vez

# --- Configuración ROCK (Normal) ---
# Basado en tu último diagrama (Rock Pro)
LAMBDA_ROCK = [
    HIHAT_BOMBO, # q0  (Tiempo 1.1)
    SILENCIO,    # q1
    HIHAT,       # q2
    SILENCIO,    # q3
    HIHAT_CAJA,  # q4  (Tiempo 2.1 - Backbeat)
    SILENCIO,    # q5
    HIHAT,       # q6
    SILENCIO,    # q7
    HIHAT_BOMBO, # q8  (Tiempo 3.1)
    SILENCIO,    # q9
    HIHAT,       # q10
    SILENCIO,    # q11
    HIHAT_CAJA,  # q12 (Tiempo 4.1 - Backbeat)
    SILENCIO,    # q13
    HIHAT,       # q14
    SILENCIO     # q15
]

# --- Configuración ROCK (Variación / Fill) ---
# Esta secuencia reemplazará los últimos 4 estados (q12-q15)
# cuando ocurra la variación. (Ejemplo: Redoble de Caja)
LAMBDA_ROCK_FILL = [
    HIHAT_CAJA,  # q12 (Golpe fuerte)
    CAJA,        # q13 (Relleno)
    HIHAT_CAJA,  # q14 (Golpe fuerte)
    CAJA         # q15 (Relleno)
]

# --- Configuración REGGAETON (Dembow) ---
# (Se mantiene igual, usando los símbolos simples por ahora)
LAMBDA_REGGAETON = [
    HIHAT_BOMBO, # q0  (Tiempo 1.1 - Tun)
    HIHAT,       # q1
    SILENCIO,    # q2
    CAJA,        # q3  (Tiempo 1.4 - Pa!)
    
    HIHAT_BOMBO, # q4  (Tiempo 2.1 - Tun)
    HIHAT,       # q5
    CAJA,        # q6  (Tiempo 2.3 - Pa!)
    SILENCIO,    # q7
    
    HIHAT_BOMBO, # q8  (Tiempo 3.1 - Tun)
    HIHAT,       # q9
    SILENCIO,    # q10
    CAJA,        # q11 (Tiempo 3.4 - Pa!)
    
    HIHAT_BOMBO, # q12 (Tiempo 4.1 - Tun)
    HIHAT,       # q13
    CAJA,        # q14 (Tiempo 4.3 - Pa!)
    SILENCIO     # q15
]

# --- Configuración REGGAETON (Variación / Corte) ---
# Reemplaza los últimos 4 estados (q12-q15)
# Un corte clásico: "Pa-ka-Pa" (Caja sincopada sin bombo)
LAMBDA_REGGAETON_FILL = [
    CAJA,        # q12
    SILENCIO,    # q13
    CAJA,        # q14
    CAJA         # q15
]
LAMBDA_HIPHOP = [
    HIHAT_BOMBO, # q0  (Tiempo 1.1)
    SILENCIO,    # q1
    HIHAT,       # q2
    BOMBO,       # q3  (Síncopa: Bombo justo antes de la caja)
    
    HIHAT_CAJA,  # q4  (Tiempo 2.1 - Backbeat)
    SILENCIO,    # q5
    HIHAT,       # q6
    SILENCIO,    # q7
    
    HIHAT_BOMBO, # q8  (Tiempo 3.1)
    SILENCIO,    # q9
    BOMBO,       # q10 (Síncopa)
    BOMBO,       # q11 (Síncopa doble antes de la caja)
    
    HIHAT_CAJA,  # q12 (Tiempo 4.1 - Backbeat)
    SILENCIO,    # q13
    HIHAT,       # q14
    SILENCIO     # q15
]

# --- Configuración HIP HOP (Variación / Break) ---
# Un clásico "Breakbeat" al final
LAMBDA_HIPHOP_FILL = [
    CAJA,        # q12
    BOMBO,       # q13
    CAJA,        # q14
    SILENCIO     # q15
]

Q_ROCK_0 = 'q0'      # Esperando 1er Bombo
Q_ROCK_1 = 'q1'      # Vio Bombo, esperando Caja
Q_ROCK_2 = 'q2'      # Vio Caja, esperando 2do Bombo
Q_ROCK_3 = 'q3'      # Vio 2do Bombo, esperando Caja final
Q_ROCK_F = 'q_fin'   # ¡Aceptado! (Completó el patrón)

# Transiciones (Delta)
# Solo definimos las transiciones que AVANZAN.
# La clase base ignorará lo demás (Hi-Hats, silencios).
DELTA_ROCK_ACEPTADOR = {
    Q_ROCK_0: {
        BOMBO: Q_ROCK_1,       # B -> avanza
        HIHAT_BOMBO: Q_ROCK_1  # HB -> avanza
    },
    Q_ROCK_1: {
        CAJA: Q_ROCK_2,
        HIHAT_CAJA: Q_ROCK_2
    },
    Q_ROCK_2: {
        BOMBO: Q_ROCK_3,
        HIHAT_BOMBO: Q_ROCK_3
    },
    Q_ROCK_3: {
        CAJA: Q_ROCK_F,
        HIHAT_CAJA: Q_ROCK_F
    },
    Q_ROCK_F: {

    }
}