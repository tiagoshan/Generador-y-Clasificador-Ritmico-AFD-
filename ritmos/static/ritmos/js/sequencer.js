let audioContext = null;
let audioBuffers = {};
let isPlaying = false;
let proximoTiempoDeNota = 0.0;
let indiceNotaActual = 0;
let secuenciaActual = [];
let bpm = 120.0;
let timerID = null;

const RUTA_SONIDOS = window.STATIC_URL + 'ritmos/sounds/';

async function cargarSonido(url, simbolo) {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    try {
        const response = await fetch(url);
        const arrayBuffer = await response.arrayBuffer();
        audioBuffers[simbolo] = await audioContext.decodeAudioData(arrayBuffer);
    } catch (e) {
        console.error(`Error cargando sonido ${simbolo}:`, e);
    }
}

async function precargarSonidos() {
    await Promise.all([
        cargarSonido(RUTA_SONIDOS + 'B.wav?v=2', 'B'),
        cargarSonido(RUTA_SONIDOS + 'C.wav?v=2', 'C'),
        cargarSonido(RUTA_SONIDOS + 'H.wav?v=2', 'H'),
    ]);
}

// when=0 significa reproducir inmediatamente
function reproducirSonido(simbolo, when = 0) {
    if (!audioBuffers[simbolo] || !audioContext) return;
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffers[simbolo];
    source.connect(audioContext.destination);
    source.start(when);
}

// ── Generador ─────────────────────────────────────────────────────────────

function highlightStep(idx) {
    const display = document.getElementById('sequenceDisplay');
    display.querySelectorAll('.step.active').forEach(el => el.classList.remove('active'));
    const steps = display.querySelectorAll('.step');
    if (steps[idx]) steps[idx].classList.add('active');
}

function programador() {
    while (proximoTiempoDeNota < audioContext.currentTime + 0.1) {
        const simbolo = secuenciaActual[indiceNotaActual];
        const when = proximoTiempoDeNota;
        const idx = indiceNotaActual;

        if (simbolo && simbolo !== '-') {
            // 'HB' → ['H','B'], 'HC' → ['H','C'], 'B'/'C'/'H' → single char
            for (const char of simbolo) {
                reproducirSonido(char, when);
            }
        }

        const delay = Math.max(0, (when - audioContext.currentTime) * 1000);
        setTimeout(() => highlightStep(idx), delay);

        proximoTiempoDeNota += (60.0 / bpm) / 4.0;
        indiceNotaActual = (indiceNotaActual + 1) % secuenciaActual.length;
    }
    timerID = window.setTimeout(programador, 25.0);
}

async function play() {
    if (isPlaying) return;
    if (isGaming) stopGame();

    if (!audioContext) await precargarSonidos();
    if (audioContext.state === 'suspended') await audioContext.resume();

    isPlaying = true;

    bpm = parseFloat(document.getElementById('bpm').value) || 120;
    const compases = document.getElementById('measures').value;
    const genero = document.getElementById('genreSelect').value;

    const display = document.getElementById('sequenceDisplay');
    display.textContent = 'Generando...';

    // Ocultar resultado anterior
    document.getElementById('classifyContainer').style.display = 'none';
    document.getElementById('classifyResult').textContent = '';
    document.getElementById('classifyResult').className = 'classify-result';

    try {
        const response = await fetch(`/api/generate/${genero}/${compases}/`);
        const data = await response.json();

        if (data.error) {
            display.textContent = data.error;
            isPlaying = false;
            return;
        }

        secuenciaActual = data.sequence;
        display.innerHTML = '';
        secuenciaActual.forEach((sym, i) => {
            const span = document.createElement('span');
            span.className = 'step';
            span.textContent = sym;
            display.appendChild(span);
            if (i < secuenciaActual.length - 1) {
                const sep = document.createElement('span');
                sep.className = 'step-sep';
                sep.textContent = ' - ';
                display.appendChild(sep);
            }
        });

        // Mostrar botón de clasificación
        document.getElementById('classifyContainer').style.display = 'flex';

        indiceNotaActual = 0;
        proximoTiempoDeNota = audioContext.currentTime;
        programador();
    } catch (e) {
        console.error(e);
        display.textContent = 'Error de conexión.';
        isPlaying = false;
    }
}

function stop() {
    isPlaying = false;
    window.clearTimeout(timerID);
    document.querySelectorAll('#sequenceDisplay .step.active').forEach(el => el.classList.remove('active'));
}

// ── Clasificador ─────────────────────────────────────────────────────────

async function classify() {
    if (!secuenciaActual.length) return;

    const btn = document.getElementById('classifyButton');
    const resultEl = document.getElementById('classifyResult');

    btn.disabled = true;
    resultEl.className = 'classify-result classify-loading';
    resultEl.textContent = 'Clasificando...';

    try {
        const response = await fetch('/api/classify/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sequence: secuenciaActual }),
        });
        const data = await response.json();

        const detected = Array.isArray(data.genre_detected)
            ? data.genre_detected.join(', ')
            : data.genre_detected;

        const rows = Object.entries(data.results)
            .map(([g, match]) => `<span class="${match ? 'match-yes' : 'match-no'}">${g}: ${match ? '✓' : '✗'}</span>`)
            .join('  ');

        resultEl.innerHTML = `<strong>Género detectado:</strong> ${detected}<br><em>${data.message}</em><br><small>${rows}</small>`;
        resultEl.className = detected === 'Desconocido'
            ? 'classify-result classify-unknown'
            : 'classify-result classify-found';
    } catch (e) {
        resultEl.textContent = 'Error al clasificar.';
        resultEl.className = 'classify-result classify-error';
    } finally {
        btn.disabled = false;
    }
}

// ── Modo Juego ────────────────────────────────────────────────────────────

let isGaming = false;
let gameStep = 0;
let gameNextNoteTime = 0.0;
let gameTimerID = null;
let gameScore = { correct: 0, total: 0, perfect: 0 };
let currentPattern = [];
let gameLoopCount = 0;

const GAME_BPM_START = 80;
const GAME_BPM_MAX   = 160;
const GAME_BPM_STEP  = 8;

const GENRE_PATTERNS = {
    rock: [
        'B', null, null, null,
        'C', null, null, null,
        'B', null, null, null,
        'C', null, null, null,
    ],
    reggaeton: [
        'B', null, 'B', null,
        'C', null, null, null,
        'B', null, 'B', null,
        'C', null, null, null,
    ],
    hiphop: [
        'B', null, null, null,
        'C', null, null, null,
        'B', null, 'B', null,
        'C', null, null, null,
    ],
    cumbia: [
        'B', null, null, null,
        'C', null, 'B', null,
        null, null, 'C', null,
        'B', null, null, null,
    ],
};

function highlightGameStep(idx) {
    const display = document.getElementById('gamePatternDisplay');
    if (!display) return;
    display.querySelectorAll('.game-step.active').forEach(el => el.classList.remove('active'));
    const steps = display.querySelectorAll('.game-step');
    if (steps[idx]) steps[idx].classList.add('active');
}

function renderGamePattern() {
    const display = document.getElementById('gamePatternDisplay');
    if (!display) return;
    display.innerHTML = '';
    currentPattern.forEach((sym) => {
        const span = document.createElement('span');
        span.className = 'game-step' + (sym ? ` target-${sym.toLowerCase()}` : ' empty');
        span.textContent = sym || '·';
        display.appendChild(span);
    });
}

function actualizarBpmDisplay() {
    const el = document.getElementById('gameBpmDisplay');
    if (el) el.textContent = `BPM: ${Math.round(bpm)}`;
}

function gameLoop() {
    while (gameNextNoteTime < audioContext.currentTime + 0.1) {
        if (gameStep % 2 === 0) {
            reproducirSonido('H', gameNextNoteTime);
        }

        const delay = Math.max(0, (gameNextNoteTime - audioContext.currentTime) * 1000);
        const stepIdx = gameStep;
        setTimeout(() => highlightGameStep(stepIdx), delay);

        gameStep = (gameStep + 1) % 16;

        if (gameStep === 0) {
            gameLoopCount++;
            if (gameLoopCount % 2 === 0 && bpm < GAME_BPM_MAX) {
                bpm = Math.min(bpm + GAME_BPM_STEP, GAME_BPM_MAX);
                setTimeout(actualizarBpmDisplay, delay);
            }
        }

        gameNextNoteTime += (60.0 / bpm) / 4.0;
    }
    gameTimerID = setTimeout(gameLoop, 25);
}

function actualizarScore() {
    document.getElementById('scoreValue').textContent = gameScore.correct;
    document.getElementById('scoreTotal').textContent = gameScore.total;
    const perfectEl = document.getElementById('scorePerfect');
    if (perfectEl) perfectEl.textContent = gameScore.perfect;
}

function checkHit(instrumentoTocado) {
    if (!isGaming) return;
    reproducirSonido(instrumentoTocado);

    const feedbackEl = document.getElementById('feedbackDisplay');
    const lastStep = (gameStep - 1 + 16) % 16;
    const prevStep = (gameStep - 2 + 16) % 16;

    gameScore.total++;

    if (currentPattern[lastStep] === instrumentoTocado) {
        feedbackEl.textContent = '¡PERFECTO!';
        feedbackEl.className = 'feedback-perfect';
        gameScore.correct++;
        gameScore.perfect++;
    } else if (currentPattern[prevStep] === instrumentoTocado) {
        feedbackEl.textContent = '¡BIEN!';
        feedbackEl.className = 'feedback-good';
        gameScore.correct++;
    } else if (currentPattern[lastStep] === null) {
        feedbackEl.textContent = '¡A DESTIEMPO!';
        feedbackEl.className = 'feedback-bad';
    } else {
        feedbackEl.textContent = '¡MAL!';
        feedbackEl.className = 'feedback-bad';
    }

    actualizarScore();
}

async function startGame() {
    if (isGaming) return;
    if (isPlaying) stop();

    if (!audioContext) await precargarSonidos();
    if (audioContext.state === 'suspended') await audioContext.resume();

    isGaming = true;
    gameStep = 15;
    gameLoopCount = 0;
    bpm = GAME_BPM_START;
    gameScore = { correct: 0, total: 0, perfect: 0 };

    const genre = document.getElementById('gameGenreSelect')?.value || 'rock';
    currentPattern = GENRE_PATTERNS[genre];
    renderGamePattern();

    const bpmInput = document.getElementById('bpm');
    if (bpmInput) bpmInput.value = bpm;

    gameNextNoteTime = audioContext.currentTime;

    document.getElementById('startGameButton').style.display = 'none';
    document.getElementById('stopGameButton').style.display = 'block';
    document.getElementById('gameBpmDisplay').style.display = 'block';
    actualizarBpmDisplay();

    const scoreEl = document.getElementById('scoreDisplay');
    if (scoreEl) scoreEl.style.display = 'block';
    actualizarScore();

    const fb = document.getElementById('feedbackDisplay');
    fb.textContent = '¡Sigue el Ritmo!';
    fb.className = 'feedback-neutral';

    gameLoop();
}

function stopGame() {
    isGaming = false;
    clearTimeout(gameTimerID);

    document.querySelectorAll('#gamePatternDisplay .game-step.active').forEach(el => el.classList.remove('active'));
    document.getElementById('gameBpmDisplay').style.display = 'none';

    document.getElementById('startGameButton').style.display = 'block';
    document.getElementById('stopGameButton').style.display = 'none';

    const fb = document.getElementById('feedbackDisplay');
    if (gameScore.total > 0) {
        const pct = Math.round((gameScore.correct / gameScore.total) * 100);
        fb.textContent = `Terminado — ${gameScore.correct}/${gameScore.total} (${pct}%) · ${gameScore.perfect} perfectos`;
    } else {
        fb.textContent = 'Juego Terminado';
    }
    fb.className = 'feedback-neutral';
}

// ── Inicialización ────────────────────────────────────────────────────────

window.addEventListener('DOMContentLoaded', () => {
    const playBtn    = document.getElementById('playButton');
    const stopBtn    = document.getElementById('stopButton');
    const bpmInput   = document.getElementById('bpm');
    const genreSelect = document.getElementById('genreSelect');

    if (playBtn) playBtn.addEventListener('click', play);
    if (stopBtn) stopBtn.addEventListener('click', stop);

    if (bpmInput) {
        bpmInput.addEventListener('input', function () {
            bpm = parseFloat(this.value) || 120;
        });
    }

    const classifyBtn = document.getElementById('classifyButton');
    if (classifyBtn) classifyBtn.addEventListener('click', classify);

    const startGameBtn = document.getElementById('startGameButton');
    const stopGameBtn  = document.getElementById('stopGameButton');
    const btnKick      = document.getElementById('btnKick');
    const btnSnare     = document.getElementById('btnSnare');

    if (startGameBtn) startGameBtn.addEventListener('click', startGame);
    if (stopGameBtn)  stopGameBtn.addEventListener('click', stopGame);

    if (btnKick) {
        btnKick.addEventListener('mousedown', () => checkHit('B'));
        btnKick.addEventListener('touchstart', (e) => { e.preventDefault(); checkHit('B'); }, { passive: false });
    }
    if (btnSnare) {
        btnSnare.addEventListener('mousedown', () => checkHit('C'));
        btnSnare.addEventListener('touchstart', (e) => { e.preventDefault(); checkHit('C'); }, { passive: false });
    }

    window.addEventListener('keydown', (e) => {
        if (!isGaming) return;
        if (e.key.toLowerCase() === 'b') checkHit('B');
        if (e.key.toLowerCase() === 'c') checkHit('C');
    });

    const bpmPorGenero = { rock: 120, reggaeton: 90, hiphop: 85, cumbia: 100 };

    if (genreSelect) {
        genreSelect.addEventListener('change', function () {
            const bpmValor = bpmPorGenero[this.value];
            if (bpmValor && bpmInput) {
                bpmInput.value = bpmValor;
                bpm = bpmValor;
                bpmInput.style.backgroundColor = '#333';
                setTimeout(() => { bpmInput.style.backgroundColor = ''; }, 200);
            }
        });
    }

    const tabGen  = document.getElementById('tabGenerator');
    const tabGame = document.getElementById('tabGame');
    const secGen  = document.getElementById('generatorSection');
    const secGame = document.getElementById('gameSection');

    function switchTab(target) {
        stop();
        stopGame();
        const isGen = target === 'generator';
        tabGen.classList.toggle('active', isGen);
        tabGame.classList.toggle('active', !isGen);
        secGen.style.display  = isGen ? 'flex' : 'none';
        secGame.style.display = isGen ? 'none' : 'flex';
    }

    if (tabGen)  tabGen.addEventListener('click',  () => switchTab('generator'));
    if (tabGame) tabGame.addEventListener('click', () => switchTab('game'));

    precargarSonidos().catch(console.error);
});
