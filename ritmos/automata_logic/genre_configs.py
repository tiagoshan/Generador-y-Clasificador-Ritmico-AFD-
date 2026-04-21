
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
    BOMBO,       # q0  (Tiempo 1 - bombo seco, sin hi-hat: sonido grave abierto)
    SILENCIO,    # q1
    HIHAT,       # q2
    SILENCIO,    # q3

    HIHAT_CAJA,  # q4  (Contratiempo fuerte: caja + hi-hat)
    SILENCIO,    # q5
    HIHAT,       # q6
    SILENCIO,    # q7

    BOMBO,       # q8  (Tiempo 3 - bombo seco)
    SILENCIO,    # q9
    HIHAT,       # q10
    SILENCIO,    # q11

    HIHAT_CAJA,  # q12 (Contratiempo fuerte)
    SILENCIO,    # q13
    HIHAT,       # q14
    SILENCIO     # q15
]

# Repique de timbal colombiano
LAMBDA_CUMBIA_FILL = [
    CAJA,        # q12
    BOMBO,       # q13
    CAJA,        # q14
    BOMBO        # q15
]

# ── Rock Aceptador ──────────────────────────────────────────────────────────
# Reconoce: HB → HC → HB → HC  (bombo+hat y caja+hat siempre juntos)
# Si aparece un bombo seco (B) entre HB y HC, es estado muerto (no es rock).

Q_ROCK_0    = 'q0'
Q_ROCK_1    = 'q1'
Q_ROCK_2    = 'q2'
Q_ROCK_3    = 'q3'
Q_ROCK_F    = 'q_fin'
_Q_ROCK_DEAD = 'q_dead'

DELTA_ROCK_ACEPTADOR = {
    Q_ROCK_0:    {HIHAT_BOMBO: Q_ROCK_1},
    Q_ROCK_1:    {HIHAT_CAJA: Q_ROCK_2,  BOMBO: _Q_ROCK_DEAD},
    Q_ROCK_2:    {HIHAT_BOMBO: Q_ROCK_3},
    Q_ROCK_3:    {HIHAT_CAJA: Q_ROCK_F,  BOMBO: _Q_ROCK_DEAD},
    _Q_ROCK_DEAD: {},
}

# ── Reggaetón Aceptador ──────────────────────────────────────────────────────
# Reconoce el dembow: HB → H → C  (kick+hihat, hihat solo, caja sola)
# Si en lugar de C aparece HC (caja+hat = estilo rock), estado muerto.

Q_REGGAETON_0    = 'q0'
Q_REGGAETON_1    = 'q1'
Q_REGGAETON_2    = 'q2'
Q_REGGAETON_F    = 'q_fin'
_Q_REGGAETON_DEAD = 'q_dead'

DELTA_REGGAETON_ACEPTADOR = {
    Q_REGGAETON_0:    {HIHAT_BOMBO: Q_REGGAETON_1},
    Q_REGGAETON_1:    {HIHAT: Q_REGGAETON_2},
    Q_REGGAETON_2:    {CAJA: Q_REGGAETON_F, HIHAT_CAJA: _Q_REGGAETON_DEAD},
    _Q_REGGAETON_DEAD: {},
}

# ── Hip-Hop Aceptador ────────────────────────────────────────────────────────
# Reconoce la síncopa: (B|HB) → B → (C|HC)  (doble bombo antes de la caja)
# Si la caja llega antes del segundo bombo, estado muerto (no es hip-hop).

Q_HIPHOP_0    = 'q0'
Q_HIPHOP_1    = 'q1'
Q_HIPHOP_2    = 'q2'
Q_HIPHOP_F    = 'q_fin'
_Q_HIPHOP_DEAD = 'q_dead'

DELTA_HIPHOP_ACEPTADOR = {
    Q_HIPHOP_0:    {BOMBO: Q_HIPHOP_1, HIHAT_BOMBO: Q_HIPHOP_1},
    Q_HIPHOP_1:    {BOMBO: Q_HIPHOP_2, CAJA: _Q_HIPHOP_DEAD, HIHAT_CAJA: _Q_HIPHOP_DEAD},
    Q_HIPHOP_2:    {CAJA: Q_HIPHOP_F,  HIHAT_CAJA: Q_HIPHOP_F},
    _Q_HIPHOP_DEAD: {},
}

# ── Cumbia Aceptador ─────────────────────────────────────────────────────────
# Reconoce: B → HC → B → HC  (bombo seco alternado con contratiempo)
# Si aparece HB (bombo con hat) mientras se rastrea el patrón, estado muerto:
# la cumbia nunca mezcla bombo con hi-hat en los tiempos principales.

Q_CUMBIA_0    = 'q0'
Q_CUMBIA_1    = 'q1'
Q_CUMBIA_2    = 'q2'
Q_CUMBIA_3    = 'q3'
Q_CUMBIA_F    = 'q_fin'
_Q_CUMBIA_DEAD = 'q_dead'

DELTA_CUMBIA_ACEPTADOR = {
    Q_CUMBIA_0:    {BOMBO: Q_CUMBIA_1},
    Q_CUMBIA_1:    {HIHAT_CAJA: Q_CUMBIA_2,  HIHAT_BOMBO: _Q_CUMBIA_DEAD},
    Q_CUMBIA_2:    {BOMBO: Q_CUMBIA_3,        HIHAT_BOMBO: _Q_CUMBIA_DEAD},
    Q_CUMBIA_3:    {HIHAT_CAJA: Q_CUMBIA_F,   HIHAT_BOMBO: _Q_CUMBIA_DEAD},
    _Q_CUMBIA_DEAD: {},
}