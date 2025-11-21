
BOMBO = 'B'
CAJA = 'C'
HIHAT = 'H'
SILENCIO = '-'
HIHAT_BOMBO = 'HB'  # Suenan a la vez
HIHAT_CAJA = 'HC'   # Suenan a la vez

# Rock
LAMBDA_ROCK = [
    HIHAT_BOMBO, # q0  (Tiempo 1.1)
    SILENCIO,    # q1
    HIHAT,       # q2
    SILENCIO,    # q3
    HIHAT_CAJA,  # q4  (Tiempo 2.1 )
    SILENCIO,    # q5
    HIHAT,       # q6
    SILENCIO,    # q7
    HIHAT_BOMBO, # q8  (Tiempo 3.1)
    SILENCIO,    # q9
    HIHAT,       # q10
    SILENCIO,    # q11
    HIHAT_CAJA,  # q12 (Tiempo 4.1 )
    SILENCIO,    # q13
    HIHAT,       # q14
    SILENCIO     # q15
]

# fill rock
LAMBDA_ROCK_FILL = [
    HIHAT_CAJA,  # q12 
    CAJA,        # q13 
    HIHAT_CAJA,  # q14 
    CAJA         # q15 
]

# reguetón
LAMBDA_REGGAETON = [
    HIHAT_BOMBO, # q0  (Tiempo 1.1 - tun)
    HIHAT,       # q1
    SILENCIO,    # q2
    CAJA,        # q3  (Tiempo 1.4 - Pa)
    
    HIHAT_BOMBO, # q4  (Tiempo 2.1 - Tun)
    HIHAT,       # q5
    CAJA,        # q6  (Tiempo 2.3 - Pa)
    SILENCIO,    # q7
    
    HIHAT_BOMBO, # q8  (Tiempo 3.1 - tun)
    HIHAT,       # q9
    SILENCIO,    # q10
    CAJA,        # q11 (Tiempo 3.4 - Pa)
    
    HIHAT_BOMBO, # q12 (Tiempo 4.1 - Tun)
    HIHAT,       # q13
    CAJA,        # q14 (Tiempo 4.3 - Pa)
    SILENCIO     # q15
]

# fill pakapa
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
    
    HIHAT_CAJA,  # q4  (Tiempo 2.1 )
    SILENCIO,    # q5
    HIHAT,       # q6
    SILENCIO,    # q7
    
    HIHAT_BOMBO, # q8  (Tiempo 3.1)
    SILENCIO,    # q9
    BOMBO,       # q10 (Síncopa)
    BOMBO,       # q11 (Síncopa doble antes de la caja)
    
    HIHAT_CAJA,  # q12 (Tiempo 4.1)
    SILENCIO,    # q13
    HIHAT,       # q14
    SILENCIO     # q15
]

# hip hop fill
LAMBDA_HIPHOP_FILL = [
    CAJA,        # q12
    BOMBO,       # q13
    CAJA,        # q14
    SILENCIO     # q15
]
LAMBDA_CUMBIA = [
    HIHAT_BOMBO, # q0  (Tiempo 1)
    SILENCIO,    # q1
    HIHAT,       # q2  (chi)
    SILENCIO,    # q3
    
    HIHAT_CAJA,  # q4  (Tiempo 2 - Contratiempo fuerte)
    SILENCIO,    # q5
    HIHAT,       # q6  (chi)
    SILENCIO,    # q7
    
    HIHAT_BOMBO, # q8  (Tiempo 3)
    SILENCIO,    # q9
    HIHAT,       # q10 (chi)
    SILENCIO,    # q11
    
    HIHAT_CAJA,  # q12 (Tiempo 4)
    SILENCIO,    # q13
    HIHAT,       # q14 (chi)
    SILENCIO     # q15
]

# Un repique clásico de timbal (usando caja)
LAMBDA_CUMBIA_FILL = [
    CAJA,        # q12
    HIHAT,       # q13
    CAJA,        # q14
    HIHAT        # q15
]

Q_ROCK_0 = 'q0'      # Esperando 1er Bombo
Q_ROCK_1 = 'q1'      # Vio Bombo, esperando Caja
Q_ROCK_2 = 'q2'      # Vio Caja, esperando 2do Bombo
Q_ROCK_3 = 'q3'      # Vio 2do Bombo, esperando Caja final
Q_ROCK_F = 'q_fin'   # Aceptado

# Transiciones (Delta)
# Solo se define las transiciones que avanzan
# La clase base ignorará lo demás 
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