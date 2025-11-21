let audioContext = null;
let audioBuffers = {};
let isPlaying = false;
let proximoTiempoDeNota = 0.0;
let indiceNotaActual = 0;
let secuenciaActual = []; // Array para soportar símbolos dobles
let bpm = 120.0;
let timerID = null;

// Ruta base para los archivos de sonido
const RUTA_SONIDOS = window.STATIC_URL + 'ritmos/sounds/';

async function cargarSonido(url, simbolo) {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    try {

        const response = await fetch(url);
        const arrayBuffer = await response.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        audioBuffers[simbolo] = audioBuffer;
        console.log(`Sonido ${simbolo} cargado.`);
    } catch (e) {
        console.error(`Error cargando sonido ${simbolo}:`, e);
    }
}

async function precargarSonidos() {
    console.log("Precargando sonidos...");
    try {
        await cargarSonido(RUTA_SONIDOS + 'B.wav?v=2', 'B'); //?v=2 para evitar caché
        await cargarSonido(RUTA_SONIDOS + 'C.wav?v=2', 'C');
        await cargarSonido(RUTA_SONIDOS + 'H.wav?v=2', 'H');
        console.log("¡Sonidos listos!");
    } catch (e) {
        console.error("Error fatal en precarga:", e);
    }
}

function reproducirSonido(simbolo) {
    if (!audioBuffers[simbolo] || !audioContext) return;
    
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffers[simbolo];
    source.connect(audioContext.destination);
    source.start(0);
}

//generador

function programador() {
    while (proximoTiempoDeNota < audioContext.currentTime + 0.1) {
        const simbolo = secuenciaActual[indiceNotaActual];
        
        if (simbolo && simbolo !== '-') {
            if (simbolo.length > 1) {
                for (let i = 0; i < simbolo.length; i++) {
                    reproducirSonido(simbolo[i]);
                }
            } else {
                reproducirSonido(simbolo);
            }
        }
        
        // Usa la variable global 'bpm'
        const duracionSemicorchea = (60.0 / bpm) / 4.0;
        proximoTiempoDeNota += duracionSemicorchea;
        
        indiceNotaActual = (indiceNotaActual + 1) % secuenciaActual.length;
    }
    timerID = window.setTimeout(programador, 25.0);
}

async function play() {
    if (isPlaying) return;
    
    if (typeof stopGame === "function" && isGaming) stopGame();

    if (!audioContext) await precargarSonidos();
    if (audioContext.state === 'suspended') await audioContext.resume();
    
    isPlaying = true;

    // Actualizar BPM 
    bpm = document.getElementById('bpm').value;
    const compases = document.getElementById('measures').value;
    const genero = document.getElementById('genreSelect').value; 

    const display = document.getElementById('sequenceDisplay');
    display.textContent = "Generando...";

    try {
        const response = await fetch(`/api/generate/${genero}/${compases}/`);
        const data = await response.json();
        
        if (data.error) {
            display.textContent = data.error;
            isPlaying = false;
            return;
        }

        secuenciaActual = data.sequence;
        display.textContent = secuenciaActual.join(" - ");

        indiceNotaActual = 0;
        proximoTiempoDeNota = audioContext.currentTime;
        programador();

    } catch (e) {
        console.error(e);
        display.textContent = "Error de conexión.";
        isPlaying = false;
    }
}

function stop() {
    isPlaying = false;
    window.clearTimeout(timerID);
}

// modo de juego

let isGaming = false;
let gameStep = 0;
let gameNextNoteTime = 0.0;
let gameTimerID = null;

const TARGET_PATTERN = [
    'B', null, null, null,
    'C', null, null, null,
    'B', null, null, null,
    'C', null, null, null
];

function gameLoop() {
    while (gameNextNoteTime < audioContext.currentTime + 0.1) {
        
        // hi hat solo si es par
        if (gameStep % 2 === 0) {
            reproducirSonido('H');
        }

        // actualizar paso
        gameStep = (gameStep + 1) % 16;

        // avanzar tiempo
        const secondsPerStep = (60.0 / bpm) / 4.0; 
        gameNextNoteTime += secondsPerStep;
    }
    gameTimerID = setTimeout(gameLoop, 25);
}

function checkHit(instrumentoTocado) {
    if (!isGaming) return;
    reproducirSonido(instrumentoTocado);

    const feedbackEl = document.getElementById('feedbackDisplay');
    let stepEvaluado = (gameStep === 0) ? 15 : gameStep - 1; 
    const esperado = TARGET_PATTERN[stepEvaluado];

    if (esperado === instrumentoTocado) {
        feedbackEl.textContent = "¡BIEN! ";
        feedbackEl.className = "feedback-good";
    } else {
        if (esperado === null) {
            feedbackEl.textContent = "¡A DESTIEMPO! ";
        } else {
            feedbackEl.textContent = "¡MAL! ";
        }
        feedbackEl.className = "feedback-bad";
    }
}

function startGame() {
    if (isGaming) return;
    if (isPlaying) stop(); // parar generador

    if (!audioContext) precargarSonidos();
    if (audioContext && audioContext.state === 'suspended') audioContext.resume();

    isGaming = true;
    gameStep = 15;
    gameNextNoteTime = audioContext.currentTime;
    
    // bpm prederminador para el juego
    bpm = 80;
    if(document.getElementById('bpm')) document.getElementById('bpm').value = bpm;

    document.getElementById('startGameButton').style.display = 'none';
    document.getElementById('stopGameButton').style.display = 'block';
    
    const fb = document.getElementById('feedbackDisplay');
    fb.textContent = "¡Sigue el Ritmo!";
    fb.className = "feedback-neutral";
    
    gameLoop();
}

function stopGame() {
    isGaming = false;
    clearTimeout(gameTimerID);
    document.getElementById('startGameButton').style.display = 'block';
    document.getElementById('stopGameButton').style.display = 'none';
    
    const fb = document.getElementById('feedbackDisplay');
    fb.textContent = "Juego Terminado";
    fb.className = "feedback-neutral";
}

//iniciazión de eventos

window.addEventListener('DOMContentLoaded', () => {
    
    // controles generador 
    const playBtn = document.getElementById('playButton');
    const stopBtn = document.getElementById('stopButton');
    const bpmInput = document.getElementById('bpm');

    if(playBtn) playBtn.addEventListener('click', play);
    if(stopBtn) stopBtn.addEventListener('click', stop);

    // actualizar BPM en tiempo real
    if(bpmInput) {
        bpmInput.addEventListener('input', function() {
            bpm = parseFloat(this.value) || 120;
        });
    }

    // controles 
    const startInfoBtn = document.getElementById('startGameButton');
    const stopInfoBtn = document.getElementById('stopGameButton');
    const btnKick = document.getElementById('btnKick');
    const btnSnare = document.getElementById('btnSnare');

    if(startInfoBtn) startInfoBtn.addEventListener('click', startGame);
    if(stopInfoBtn) stopInfoBtn.addEventListener('click', stopGame);
    
    if(btnKick) btnKick.addEventListener('mousedown', () => checkHit('B'));
    if(btnSnare) btnSnare.addEventListener('mousedown', () => checkHit('C'));

    // teclado solo suena si el juego está activo
    window.addEventListener('keydown', (e) => {
        if (!isGaming) return; // bloqueo 

        if (e.key.toLowerCase() === 'b') {
            checkHit('B');
        }
        if (e.key.toLowerCase() === 'c') {
            checkHit('C');
        }
    });

    precargarSonidos().catch(e => console.error(e));

    // bpm por género
    const genreSelect = document.getElementById('genreSelect');
    const bpmPorGenero = { 'rock': 120, 'reggaeton': 90, 'hiphop': 85, 'cumbia': 100 };

    if(genreSelect) {
        genreSelect.addEventListener('change', function() {
            const val = this.value;
            if (bpmPorGenero[val]) {
                bpmInput.value = bpmPorGenero[val];
                bpm = bpmPorGenero[val];
                
                bpmInput.style.backgroundColor = '#333';
                setTimeout(() => bpmInput.style.backgroundColor = '', 200);
            }
        });
    }

    // tabs
    const tabGen = document.getElementById('tabGenerator');
    const tabGame = document.getElementById('tabGame');
    
    const secGen = document.getElementById('generatorSection');
    const secGame = document.getElementById('gameSection');

    function switchTab(target) {
        // detener cualquier sonido al cambiar
        stop(); 
        stopGame();

        if (target === 'generator') {
            if(tabGen) tabGen.classList.add('active');
            if(tabGame) tabGame.classList.remove('active');
            
            if(secGen) secGen.style.display = 'flex';
            if(secGame) secGame.style.display = 'none';
        } else {
            if(tabGame) tabGame.classList.add('active');
            if(tabGen) tabGen.classList.remove('active');
            
            if(secGen) secGen.style.display = 'none';
            if(secGame) secGame.style.display = 'flex';
        }
    }

    if(tabGen) tabGen.addEventListener('click', () => switchTab('generator'));
    if(tabGame) tabGame.addEventListener('click', () => switchTab('game'));
});