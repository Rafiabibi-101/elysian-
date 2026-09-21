import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Elysian",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit's normal interface.
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background: #000;
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stSidebar"],
        footer {
            display: none !important;
        }

        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }

        iframe {
            border: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html, body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    width: 100%;
    height: 100%;
    background: #000;
    font-family: Georgia, serif;
}

#world {
    width: 100vw;
    height: 100vh;
}

#intro {
    position: fixed;
    inset: 0;
    z-index: 20;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    color: white;
    text-align: center;

    background:
        radial-gradient(
            circle at center,
            rgba(35,55,45,.20),
            rgba(0,0,0,.92)
        );

    transition: opacity 2s ease;
}

#intro h1 {
    font-size: clamp(55px, 8vw, 110px);
    margin: 0;
    font-weight: 400;
    letter-spacing: 8px;
    text-shadow: 0 5px 35px rgba(0,0,0,.7);
}

#intro p {
    font-size: 19px;
    letter-spacing: 3px;
    opacity: .85;
}

#enter {
    margin-top: 35px;
    padding: 15px 50px;
    border-radius: 40px;
    border: 1px solid rgba(255,255,255,.7);
    color: white;
    background: rgba(255,255,255,.10);
    font-family: Georgia, serif;
    font-size: 18px;
    cursor: pointer;
    backdrop-filter: blur(8px);
}

#enter:hover {
    background: rgba(255,255,255,.25);
}

#title {
    position: fixed;
    top: 25px;
    left: 30px;
    z-index: 5;
    color: white;
    pointer-events: none;
    text-shadow: 0 3px 15px black;
}

#title h2 {
    margin: 0;
    font-size: 28px;
    letter-spacing: 5px;
    font-weight: 400;
}

#title span {
    font-size: 12px;
    letter-spacing: 2px;
    opacity: .75;
}

#instructions {
    position: fixed;
    bottom: 25px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    color: rgba(255,255,255,.8);
    font-family: Arial, sans-serif;
    font-size: 12px;
    letter-spacing: 1px;
    background: rgba(0,0,0,.22);
    padding: 9px 16px;
    border-radius: 20px;
    backdrop-filter: blur(5px);
    pointer-events: none;
}

#character {
    position: fixed;
    right: 25px;
    top: 25px;
    z-index: 5;
    color: white;
    text-align: right;
    text-shadow: 0 3px 15px black;
    font-family: Georgia, serif;
}

#character strong {
    font-size: 18px;
    letter-spacing: 2px;
}

#character small {
    display: block;
    opacity: .7;
    margin-top: 5px;
}
</style>
</head>

<body>

<div id="world"></div>

<div id="intro">
    <h1>ELYSIAN</h1>
    <p>Not just an app. Your imaginary heaven.</p>
    <button id="enter">ENTER</button>
</div>

<div id="title">
    <h2>ELYSIAN</h2>
    <span>YOUR IMAGINARY HEAVEN</span>
</div>

<div id="character">
    <strong id="characterName"></strong>
    <small id="characterType"></small>
</div>

<div id="instructions">
    WASD / ARROWS — WALK &nbsp; • &nbsp; MOUSE — LOOK AROUND
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/examples/js/controls/PointerLockControls.js"></script>

<script>

// ============================================================
// ELYSIAN
// ============================================================

const container = document.getElementById("world");

const scene = new THREE.Scene();

scene.fog = new THREE.FogExp2(
    0x9db9a8,
    0.0025
);


// ------------------------------------------------------------
// CAMERA
// ------------------------------------------------------------

const camera = new THREE.PerspectiveCamera(
    70,
    window.innerWidth / window.innerHeight,
    0.1,
    3000
);

camera.position.set(0, 7, 70);


// ------------------------------------------------------------
// RENDERER
// ------------------------------------------------------------

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.shadowMap.enabled = true;

renderer.shadowMap.type =
    THREE.PCFSoftShadowMap;

renderer.outputEncoding =
    THREE.sRGBEncoding;

container.appendChild(renderer.domElement);


// ------------------------------------------------------------
// SKY
// ------------------------------------------------------------

const skyGeometry =
    new THREE.SphereGeometry(
        1800,
        32,
        32
    );

const skyMaterial =
    new THREE.MeshBasicMaterial({
        color: 0x87aebf,
        side: THREE.BackSide
    });

const sky =
    new THREE.Mesh(
        skyGeometry,
        skyMaterial
    );

scene.add(sky);


// ------------------------------------------------------------
// LIGHT
// ------------------------------------------------------------

const ambient =
    new THREE.HemisphereLight(
        0xb9d6ff,
        0x40513c,
        1.8
    );

scene.add(ambient);

const sun =
    new THREE.DirectionalLight(
        0xffd5a0,
        3
    );

sun.position.set(
    -250,
    350,
    -300
);

sun.castShadow = true;

sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;

scene.add(sun);


// ------------------------------------------------------------
// GROUND
// ------------------------------------------------------------

const groundGeometry =
    new THREE.PlaneGeometry(
        1200,
        1200,
        100,
        100
    );

const positions =
    groundGeometry.attributes.position;

for (
    let i = 0;
    i < positions.count;
    i++
) {

    const x = positions.getX(i);
    const y = positions.getY(i);

    let height =
        Math.sin(x * 0.015) * 2 +
        Math.cos(y * 0.018) * 2 +
        Math.sin((x + y) * 0.009) * 4;

    positions.setZ(
        i,
        height
    );
}

groundGeometry.computeVertexNormals();

const groundMaterial =
    new THREE.MeshStandardMaterial({
        color: 0x477044,
        roughness: 1
    });

const ground =
    new THREE.Mesh(
        groundGeometry,
        groundMaterial
    );

ground.rotation.x =
    -Math.PI / 2;

ground.receiveShadow = true;

scene.add(ground);


// ------------------------------------------------------------
// MOUNTAINS
// ------------------------------------------------------------

function createMountain(
    x,
    z,
    height,
    width
) {

    const geometry =
        new THREE.ConeGeometry(
            width,
            height,
            7
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x435c58,
            roughness: 1
        });

    const mountain =
        new THREE.Mesh(
            geometry,
            material
        );

    mountain.position.set(
        x,
        height / 2 - 3,
        z
    );

    mountain.rotation.y =
        Math.random() * Math.PI;

    mountain.castShadow = true;

    scene.add(mountain);


    // Snow cap
    const snowGeometry =
        new THREE.ConeGeometry(
            width * .43,
            height * .35,
            7
        );

    const snowMaterial =
        new THREE.MeshStandardMaterial({
            color: 0xe8eee9,
            roughness: 1
        });

    const snow =
        new THREE.Mesh(
            snowGeometry,
            snowMaterial
        );

    snow.position.set(
        x,
        height * .78,
        z
    );

    snow.rotation.y =
        mountain.rotation.y;

    scene.add(snow);
}


createMountain(-260, -270, 180, 110);
createMountain(-100, -310, 240, 130);
createMountain(100, -330, 210, 120);
createMountain(280, -290, 170, 105);

createMountain(-380, -100, 130, 100);
createMountain(380, -100, 150, 110);


// ------------------------------------------------------------
// RIVER
// ------------------------------------------------------------

const riverShape =
    new THREE.Shape();

riverShape.moveTo(-400, 0);

riverShape.bezierCurveTo(
    -200, 40,
    -100, -50,
    0, 0
);

riverShape.bezierCurveTo(
    130, 60,
    220, -50,
    430, 20
);

riverShape.lineTo(430, -55);
riverShape.bezierCurveTo(
    220, -110,
    130, 0,
    0, -60
);

riverShape.bezierCurveTo(
    -100, -110,
    -200, -20,
    -400, -60
);

const riverGeometry =
    new THREE.ShapeGeometry(
        riverShape,
        32
    );

const riverMaterial =
    new THREE.MeshPhysicalMaterial({
        color: 0x4bafd0,
        transparent: true,
        opacity: .72,
        roughness: .15,
        metalness: .05
    });

const river =
    new THREE.Mesh(
        riverGeometry,
        riverMaterial
    );

river.rotation.x =
    -Math.PI / 2;

river.position.set(
    0,
    .7,
    -80
);

scene.add(river);


// ------------------------------------------------------------
// FLOWERS
// ------------------------------------------------------------

const flowerColors = [
    0xffd1dc,
    0xffe28a,
    0xffffff,
    0xbfa4ff,
    0xff8fab,
    0xffa66b
];

function createFlower(
    x,
    z
) {

    const group =
        new THREE.Group();

    const stemGeometry =
        new THREE.CylinderGeometry(
            .025,
            .035,
            .7,
            5
        );

    const stemMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x3b7c42
        });

    const stem =
        new THREE.Mesh(
            stemGeometry,
            stemMaterial
        );

    stem.position.y = .35;

    group.add(stem);


    const petalGeometry =
        new THREE.SphereGeometry(
            .13,
            6,
            6
        );

    const petalMaterial =
        new THREE.MeshStandardMaterial({
            color:
                flowerColors[
                    Math.floor(
                        Math.random() *
                        flowerColors.length
                    )
                ]
        });

    for (
        let i = 0;
        i < 5;
        i++
    ) {

        const petal =
            new THREE.Mesh(
                petalGeometry,
                petalMaterial
            );

        const angle =
            (Math.PI * 2 / 5) * i;

        petal.position.set(
            Math.cos(angle) * .14,
            .75,
            Math.sin(angle) * .14
        );

        group.add(petal);
    }

    group.position.set(
        x,
        0,
        z
    );

    scene.add(group);
}


for (
    let i = 0;
    i < 1000;
    i++
) {

    const x =
        (Math.random() - .5) * 800;

    const z =
        (Math.random() - .5) * 500;

    // Keep some space around the river.
    if (
        Math.abs(z + 80) < 25
    ) continue;

    createFlower(x, z);
}


// ------------------------------------------------------------
// TREES
// ------------------------------------------------------------

function createTree(x, z) {

    const group =
        new THREE.Group();

    const trunk =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                .35,
                .5,
                5,
                8
            ),
            new THREE.MeshStandardMaterial({
                color: 0x62432b
            })
        );

    trunk.position.y = 2.5;

    group.add(trunk);


    const leaves =
        new THREE.Mesh(
            new THREE.ConeGeometry(
                3.5,
                8,
                8
            ),
            new THREE.MeshStandardMaterial({
                color: 0x28563b
            })
        );

    leaves.position.y = 7;

    group.add(leaves);

    group.position.set(
        x,
        0,
        z
    );

    group.castShadow = true;

    scene.add(group);
}


for (
    let i = 0;
    i < 130;
    i++
) {

    const x =
        (Math.random() - .5) * 900;

    const z =
        (Math.random() - .5) * 500;

    if (
        Math.abs(x) < 100 &&
        z > -200
    ) continue;

    createTree(x, z);
}


// ------------------------------------------------------------
// CASTLE
// ------------------------------------------------------------

const castle =
    new THREE.Group();


function castleTower(
    x,
    z,
    height = 28
) {

    const tower =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                5,
                6,
                height,
                10
            ),
            new THREE.MeshStandardMaterial({
                color: 0xd9c5a6
            })
        );

    tower.position.set(
        x,
        height / 2,
        z
    );

    tower.castShadow = true;

    castle.add(tower);


    const roof =
        new THREE.Mesh(
            new THREE.ConeGeometry(
                7,
                12,
                10
            ),
            new THREE.MeshStandardMaterial({
                color: 0x58394f
            })
        );

    roof.position.set(
        x,
        height + 6,
        z
    );

    castle.add(roof);
}


const castleBody =
    new THREE.Mesh(
        new THREE.BoxGeometry(
            70,
            30,
            40
        ),
        new THREE.MeshStandardMaterial({
            color: 0xdcc7aa
        })
    );

castleBody.position.y = 15;

castle.add(castleBody);

castleTower(-32, -15, 40);
castleTower(32, -15, 40);
castleTower(-32, 15, 35);
castleTower(32, 15, 35);


const mainRoof =
    new THREE.Mesh(
        new THREE.ConeGeometry(
            28,
            20,
            4
        ),
        new THREE.MeshStandardMaterial({
            color: 0x62415b
        })
    );

mainRoof.position.y = 40;

mainRoof.rotation.y =
    Math.PI / 4;

castle.add(mainRoof);

castle.position.set(
    180,
    0,
    -230
);

scene.add(castle);


// ------------------------------------------------------------
// HORSES
// ------------------------------------------------------------

function createHorse(
    x,
    z,
    color
) {

    const horse =
        new THREE.Group();

    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                4,
                2.1,
                1.5
            ),
            new THREE.MeshStandardMaterial({
                color: color
            })
        );

    body.position.y = 3;

    horse.add(body);


    const neck =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.2,
                3.4,
                1.2
            ),
            new THREE.MeshStandardMaterial({
                color: color
            })
        );

    neck.position.set(
        1.7,
        4.2,
        0
    );

    neck.rotation.z =
        -.25;

    horse.add(neck);


    const head =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                1.8,
                1.4,
                1.2
            ),
            new THREE.MeshStandardMaterial({
                color: color
            })
        );

    head.position.set(
        2.5,
        5.7,
        0
    );

    horse.add(head);


    // Legs
    for (
        let i = 0;
        i < 4;
        i++
    ) {

        const leg =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    .18,
                    .22,
                    3,
                    6
                ),
                new THREE.MeshStandardMaterial({
                    color: color
                })
            );

        leg.position.set(
            i < 2 ? 1.2 : -1.2,
            1.5,
            i % 2 === 0 ? .5 : -.5
        );

        horse.add(leg);
    }

    horse.position.set(
        x,
        0,
        z
    );

    scene.add(horse);

    return horse;
}


const horses = [];

horses.push(
    createHorse(
        -70,
        -20,
        0xf3eee1
    )
);

horses.push(
    createHorse(
        -25,
        20,
        0x8b5a3c
    )
);

horses.push(
    createHorse(
        55,
        45,
        0x3d3028
    )
);

horses.push(
    createHorse(
        110,
        15,
        0xd5b08a
    )
);


// ------------------------------------------------------------
// PRINCE / PRINCESS
// ------------------------------------------------------------

const names = [
    ["Liora", "Princess"],
    ["Elara", "Princess"],
    ["Aurelia", "Princess"],
    ["Seraphina", "Princess"],
    ["Aren", "Prince"],
    ["Elias", "Prince"],
    ["Rowan", "Prince"]
];

const selected =
    names[
        Math.floor(
            Math.random() * names.length
        )
    ];

document.getElementById(
    "characterName"
).textContent =
    selected[0];

document.getElementById(
    "characterType"
).textContent =
    selected[1];


function createCharacter() {

    const person =
        new THREE.Group();

    const dress =
        new THREE.Mesh(
            new THREE.ConeGeometry(
                1.5,
                3.5,
                12
            ),
            new THREE.MeshStandardMaterial({
                color:
                    selected[1] === "Princess"
                    ? 0xe8a9c7
                    : 0x5875a8
            })
        );

    dress.position.y = 2;

    person.add(dress);


    const head =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .7,
                16,
                16
            ),
            new THREE.MeshStandardMaterial({
                color: 0xf1c6a8
            })
        );

    head.position.y = 4.3;

    person.add(head);


    const hair =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                .78,
                16,
                16
            ),
            new THREE.MeshStandardMaterial({
                color: 0x4a2b23
            })
        );

    hair.position.y = 4.7;

    person.add(hair);


    person.position.set(
        20,
        0,
        10
    );

    scene.add(person);

    return person;
}


const character =
    createCharacter();


// ------------------------------------------------------------
// FIREFLIES
// ------------------------------------------------------------

const fireflyGeometry =
    new THREE.BufferGeometry();

const fireflyPositions = [];

for (
    let i = 0;
    i < 250;
    i++
) {

    fireflyPositions.push(
        (Math.random() - .5) * 500,
        Math.random() * 12 + 1,
        (Math.random() - .5) * 300
    );
}

fireflyGeometry.setAttribute(
    "position",
    new THREE.Float32BufferAttribute(
        fireflyPositions,
        3
    )
);

const fireflies =
    new THREE.Points(
        fireflyGeometry,
        new THREE.PointsMaterial({
            color: 0xffeaa0,
            size: .35,
            transparent: true,
            opacity: .8
        })
    );

scene.add(fireflies);


// ------------------------------------------------------------
// CONTROLS
// ------------------------------------------------------------

const controls =
    new THREE.PointerLockControls(
        camera,
        document.body
    );

const enter =
    document.getElementById("enter");

enter.addEventListener(
    "click",
    () => {

        document.getElementById(
            "intro"
        ).style.opacity = "0";

        setTimeout(() => {
            document.getElementById(
                "intro"
            ).style.display = "none";
        }, 2000);

        controls.lock();

        startAmbientSound();
    }
);


const keys = {};

document.addEventListener(
    "keydown",
    event => {
        keys[event.code] = true;
    }
);

document.addEventListener(
    "keyup",
    event => {
        keys[event.code] = false;
    }
);


// ------------------------------------------------------------
// AMBIENT AUDIO
// ------------------------------------------------------------

let audioStarted = false;

function startAmbientSound() {

    if (audioStarted) return;

    audioStarted = true;

    try {

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        const audio =
            new AudioContext();

        const master =
            audio.createGain();

        master.gain.value = .025;

        master.connect(
            audio.destination
        );


        // Soft drone
        const oscillator =
            audio.createOscillator();

        oscillator.type = "sine";

        oscillator.frequency.value =
            196;

        const gain =
            audio.createGain();

        gain.gain.value = .18;

        oscillator.connect(gain);
        gain.connect(master);

        oscillator.start();


        // Second harmonic
        const oscillator2 =
            audio.createOscillator();

        oscillator2.type =
            "sine";

        oscillator2.frequency.value =
            293.66;

        const gain2 =
            audio.createGain();

        gain2.gain.value = .045;

        oscillator2.connect(gain2);
        gain2.connect(master);

        oscillator2.start();


        // Very soft wind noise
        const buffer =
            audio.createBuffer(
                1,
                audio.sampleRate * 2,
                audio.sampleRate
            );

        const data =
            buffer.getChannelData(0);

        for (
            let i = 0;
            i < data.length;
            i++
        ) {

            data[i] =
                Math.random() * 2 - 1;
        }

        const noise =
            audio.createBufferSource();

        noise.buffer = buffer;
        noise.loop = true;

        const filter =
            audio.createBiquadFilter();

        filter.type = "lowpass";
        filter.frequency.value = 650;

        const noiseGain =
            audio.createGain();

        noiseGain.gain.value = .035;

        noise.connect(filter);
        filter.connect(noiseGain);
        noiseGain.connect(master);

        noise.start();

    } catch (error) {

        console.log(
            "Ambient audio unavailable."
        );
    }
}


// ------------------------------------------------------------
// ANIMATION
// ------------------------------------------------------------

const clock =
    new THREE.Clock();

function animate() {

    requestAnimationFrame(
        animate
    );

    const delta =
        Math.min(
            clock.getDelta(),
            .05
        );

    const speed =
        28 * delta;


    if (controls.isLocked) {

        if (
            keys["KeyW"] ||
            keys["ArrowUp"]
        ) {
            controls.moveForward(speed);
        }

        if (
            keys["KeyS"] ||
            keys["ArrowDown"]
        ) {
            controls.moveForward(-speed);
        }

        if (
            keys["KeyA"] ||
            keys["ArrowLeft"]
        ) {
            controls.moveRight(-speed);
        }

        if (
            keys["KeyD"] ||
            keys["ArrowRight"]
        ) {
            controls.moveRight(speed);
        }

        // Don't let the player fly away.
        camera.position.y = 7;
    }


    // Horse breathing / gentle movement.
    horses.forEach(
        (horse, index) => {

            horse.position.y =
                Math.sin(
                    performance.now() *
                    .001 +
                    index
                ) * .04;
        }
    );


    // Character slowly moves.
    character.position.x +=
        Math.sin(
            performance.now() * .0003
        ) * .005;

    character.rotation.y =
        Math.sin(
            performance.now() * .0002
        ) * .5;


    // Fireflies drift.
    fireflies.rotation.y +=
        delta * .015;


    // Slowly move clouds / sky feeling.
    sky.rotation.y +=
        delta * .002;


    renderer.render(
        scene,
        camera
    );
}

animate();


// ------------------------------------------------------------
// RESIZE
// ------------------------------------------------------------

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }
);

</script>

</body>
</html>
"""

components.html(
    html,
    height=900,
    scrolling=False
)
