import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Elysian",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #07130f;
    font-family: Georgia, serif;
}

canvas {
    display: block;
}

#intro {
    position: fixed;
    inset: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background:
        radial-gradient(circle at center,
        rgba(255,255,255,0.08),
        rgba(3,12,9,0.97));
    color: white;
    text-align: center;
}

#intro h1 {
    font-size: clamp(48px, 9vw, 110px);
    letter-spacing: 14px;
    margin: 0 0 15px 0;
    font-weight: normal;
}

#intro p {
    font-size: 18px;
    opacity: 0.8;
    letter-spacing: 3px;
    margin-bottom: 40px;
}

#enter {
    padding: 16px 42px;
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 40px;
    background: rgba(255,255,255,0.08);
    color: white;
    font-size: 16px;
    letter-spacing: 4px;
    cursor: pointer;
    transition: 0.3s;
}

#enter:hover {
    background: white;
    color: #17251d;
    transform: scale(1.05);
}

#hud {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 10;
    color: white;
    font-family: Arial, sans-serif;
    font-size: 13px;
    opacity: 0;
    transition: opacity 1s;
    text-shadow: 0 2px 4px black;
    pointer-events: none;
}

#name {
    font-size: 18px;
    margin-bottom: 8px;
}

#instructions {
    opacity: 0.7;
}
</style>
</head>

<body>

<div id="intro">
    <h1>ELYSIAN</h1>
    <p>YOUR IMAGINARY HEAVEN</p>
    <button id="enter">ENTER</button>
</div>

<div id="hud">
    <div id="name"></div>
    <div id="instructions">
        WASD / ARROW KEYS TO WALK · DRAG TO LOOK
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>

let scene;
let camera;
let renderer;
let clock;

let started = false;

const keys = {};

let yaw = 0;
let pitch = 0;

let dragging = false;
let lastMouseX = 0;
let lastMouseY = 0;

const names = [
    "Aurelia",
    "Elara",
    "Seraphina",
    "Celeste",
    "Aurora",
    "Isabella",
    "Rosalie",
    "Luna",
    "Evelyn",
    "Adrian",
    "Julian",
    "Alexander",
    "Sebastian",
    "Lucian",
    "Elias",
    "Orion"
];

document.getElementById("name").innerHTML =
    "You have met " +
    names[Math.floor(Math.random() * names.length)];


// ----------------------------
// ENTER
// ----------------------------

document.getElementById("enter").addEventListener("click", function() {

    document.getElementById("intro").style.display = "none";
    document.getElementById("hud").style.opacity = "1";

    started = true;

    initWorld();

    startAmbientSound();
});


// ----------------------------
// WORLD
// ----------------------------

function initWorld() {

    scene = new THREE.Scene();

    scene.background = new THREE.Color(0x9cc7d8);

    scene.fog = new THREE.FogExp2(
        0x9cc7d8,
        0.0025
    );


    camera = new THREE.PerspectiveCamera(
        65,
        window.innerWidth / window.innerHeight,
        0.1,
        2000
    );

    camera.position.set(
        0,
        7,
        55
    );


    renderer = new THREE.WebGLRenderer({
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

    document.body.appendChild(renderer.domElement);


    clock = new THREE.Clock();


    // LIGHTING

    const hemi = new THREE.HemisphereLight(
        0xcceeff,
        0x526044,
        1.6
    );

    scene.add(hemi);


    const sun = new THREE.DirectionalLight(
        0xfff1c7,
        2
    );

    sun.position.set(
        -100,
        150,
        80
    );

    sun.castShadow = true;

    scene.add(sun);


    // GROUND

    createGround();


    // RIVER

    createRiver();


    // MOUNTAINS

    createMountains();


    // TREES

    for (let i = 0; i < 120; i++) {
        createTree(
            (Math.random() - 0.5) * 600,
            (Math.random() - 0.5) * 500
        );
    }


    // FLOWERS

    for (let i = 0; i < 700; i++) {
        createFlower(
            (Math.random() - 0.5) * 450,
            (Math.random() - 0.5) * 400
        );
    }


    // CASTLE

    createCastle();


    // HORSES

    for (let i = 0; i < 5; i++) {

        createHorse(
            -80 + Math.random() * 160,
            20 + Math.random() * 80
        );

    }


    // FIRE

    createFireflies();


    animate();
}


// ----------------------------
// GROUND
// ----------------------------

function createGround() {

    const geometry =
        new THREE.PlaneGeometry(
            1000,
            1000,
            100,
            100
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x6e9b59,
            roughness: 1
        });

    const ground =
        new THREE.Mesh(
            geometry,
            material
        );

    ground.rotation.x = -Math.PI / 2;

    ground.receiveShadow = true;

    scene.add(ground);
}


// ----------------------------
// RIVER
// ----------------------------

function createRiver() {

    const geometry =
        new THREE.PlaneGeometry(
            40,
            900
        );

    const material =
        new THREE.MeshStandardMaterial({
            color: 0x5ca9c8,
            transparent: true,
            opacity: 0.78,
            roughness: 0.15,
            metalness: 0.05
        });

    const river =
        new THREE.Mesh(
            geometry,
            material
        );

    river.rotation.x = -Math.PI / 2;

    river.position.y = 0.05;

    river.position.x = 15;

    scene.add(river);
}


// ----------------------------
// MOUNTAINS
// ----------------------------

function createMountains() {

    for (let i = 0; i < 18; i++) {

        const height =
            70 + Math.random() * 90;

        const radius =
            60 + Math.random() * 70;

        const geometry =
            new THREE.ConeGeometry(
                radius,
                height,
                7
            );

        const material =
            new THREE.MeshStandardMaterial({
                color: 0x58735e,
                roughness: 1
            });

        const mountain =
            new THREE.Mesh(
                geometry,
                material
            );

        mountain.position.set(
            (Math.random() - 0.5) * 700,
            height / 2,
            -180 - Math.random() * 300
        );

        scene.add(mountain);


        // snow cap

        if (height > 100) {

            const snow =
                new THREE.ConeGeometry(
                    radius * 0.38,
                    height * 0.25,
                    7
                );

            const snowMat =
                new THREE.MeshStandardMaterial({
                    color: 0xf5f6ed
                });

            const snowMesh =
                new THREE.Mesh(
                    snow,
                    snowMat
                );

            snowMesh.position.copy(
                mountain.position
            );

            snowMesh.position.y +=
                height * 0.37;

            scene.add(snowMesh);
        }
    }
}


// ----------------------------
// TREE
// ----------------------------

function createTree(x, z) {

    const group =
        new THREE.Group();


    const trunk =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                1.3,
                2,
                12,
                7
            ),
            new THREE.MeshStandardMaterial({
                color: 0x68472c
            })
        );

    trunk.position.y = 6;

    group.add(trunk);


    for (let i = 0; i < 3; i++) {

        const leaves =
            new THREE.Mesh(
                new THREE.ConeGeometry(
                    7 - i * 1.2,
                    14,
                    8
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x315f3a
                })
            );

        leaves.position.y =
            12 + i * 7;

        group.add(leaves);
    }


    group.position.set(
        x,
        0,
        z
    );

    scene.add(group);
}


// ----------------------------
// FLOWER
// ----------------------------

function createFlower(x, z) {

    const group =
        new THREE.Group();


    const stem =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.06,
                0.08,
                1.8,
                5
            ),
            new THREE.MeshStandardMaterial({
                color: 0x3c743f
            })
        );

    stem.position.y = 0.9;

    group.add(stem);


    const colorList = [
        0xffd1dc,
        0xfff1a8,
        0xffffff,
        0xcdb4ff,
        0xffb7ce
    ];

    const color =
        colorList[
            Math.floor(
                Math.random() * colorList.length
            )
        ];


    for (let i = 0; i < 5; i++) {

        const petal =
            new THREE.Mesh(
                new THREE.SphereGeometry(
                    0.32,
                    8,
                    8
                ),
                new THREE.MeshStandardMaterial({
                    color: color
                })
            );

        const angle =
            (i / 5) * Math.PI * 2;

        petal.position.set(
            Math.cos(angle) * 0.38,
            1.8,
            Math.sin(angle) * 0.38
        );

        group.add(petal);
    }


    const center =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                0.22,
                8,
                8
            ),
            new THREE.MeshStandardMaterial({
                color: 0xffd75a
            })
        );

    center.position.y = 1.8;

    group.add(center);


    group.position.set(
        x,
        0,
        z
    );

    scene.add(group);
}


// ----------------------------
// CASTLE
// ----------------------------

function createCastle() {

    const castle =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                45,
                25,
                28
            ),
            new THREE.MeshStandardMaterial({
                color: 0xe7dfd0
            })
        );

    body.position.y = 12.5;

    castle.add(body);


    for (let i = 0; i < 4; i++) {

        const tower =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    6,
                    6,
                    36,
                    10
                ),
                new THREE.MeshStandardMaterial({
                    color: 0xe9e2d3
                })
            );


        const roof =
            new THREE.Mesh(
                new THREE.ConeGeometry(
                    7,
                    12,
                    10
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x6d4b72
                })
            );


        const positions = [
            [-20, -11],
            [20, -11],
            [-20, 11],
            [20, 11]
        ];


        tower.position.set(
            positions[i][0],
            18,
            positions[i][1]
        );

        roof.position.set(
            positions[i][0],
            42,
            positions[i][1]
        );


        castle.add(tower);
        castle.add(roof);
    }


    castle.position.set(
        0,
        0,
        -80
    );

    scene.add(castle);
}


// ----------------------------
// HORSE
// ----------------------------

function createHorse(x, z) {

    const horse =
        new THREE.Group();


    const brown =
        new THREE.MeshStandardMaterial({
            color: 0x6b4226
        });


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                7,
                3,
                2.5
            ),
            brown
        );

    body.position.y = 4;

    horse.add(body);


    const neck =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                2,
                5,
                2
            ),
            brown
        );

    neck.position.set(
        3,
        6,
        0
    );

    neck.rotation.z = -0.3;

    horse.add(neck);


    const head =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                3,
                2.5,
                2
            ),
            brown
        );

    head.position.set(
        4.5,
        8,
        0
    );

    horse.add(head);


    for (let i = 0; i < 4; i++) {

        const leg =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    0.35,
                    0.45,
                    4
                ),
                brown
            );

        leg.position.set(
            i < 2 ? -2 : 2,
            2,
            i % 2 === 0 ? -0.8 : 0.8
        );

        horse.add(leg);
    }


    horse.position.set(
        x,
        0,
        z
    );

    horse.scale.setScalar(0.8);

    scene.add(horse);
}


// ----------------------------
// FIREFLIES
// ----------------------------

function createFireflies() {

    const geometry =
        new THREE.BufferGeometry();

    const positions = [];

    for (let i = 0; i < 300; i++) {

        positions.push(
            (Math.random() - 0.5) * 300,
            2 + Math.random() * 35,
            (Math.random() - 0.5) * 300
        );
    }


    geometry.setAttribute(
        "position",
        new THREE.Float32BufferAttribute(
            positions,
            3
        )
    );


    const material =
        new THREE.PointsMaterial({
            color: 0xfff6a0,
            size: 0.8,
            transparent: true,
            opacity: 0.8
        });


    const fireflies =
        new THREE.Points(
            geometry,
            material
        );


    scene.add(fireflies);
}


// ----------------------------
// MOVEMENT
// ----------------------------

window.addEventListener(
    "keydown",
    function(e) {

        keys[e.key.toLowerCase()] = true;
    }
);


window.addEventListener(
    "keyup",
    function(e) {

        keys[e.key.toLowerCase()] = false;
    }
);


// ----------------------------
// MOUSE LOOK
// ----------------------------

rendererMouseSetup = function() {

    window.addEventListener(
        "mousedown",
        function(e) {

            if (!started) return;

            dragging = true;

            lastMouseX = e.clientX;
            lastMouseY = e.clientY;
        }
    );


    window.addEventListener(
        "mouseup",
        function() {

            dragging = false;
        }
    );


    window.addEventListener(
        "mousemove",
        function(e) {

            if (!dragging || !started) return;

            const dx =
                e.clientX - lastMouseX;

            const dy =
                e.clientY - lastMouseY;

            lastMouseX = e.clientX;
            lastMouseY = e.clientY;


            yaw -= dx * 0.003;

            pitch -= dy * 0.003;

            pitch =
                Math.max(
                    -1.2,
                    Math.min(1.2, pitch)
                );
        }
    );
};

rendererMouseSetup();


// ----------------------------
// ANIMATION
// ----------------------------

function animate() {

    requestAnimationFrame(animate);


    if (!camera || !renderer) {
        return;
    }


    const delta =
        clock.getDelta();


    const speed =
        25 * delta;


    let forward = 0;
    let sideways = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    ) {
        forward += 1;
    }


    if (
        keys["s"] ||
        keys["arrowdown"]
    ) {
        forward -= 1;
    }


    if (
        keys["a"] ||
        keys["arrowleft"]
    ) {
        sideways -= 1;
    }


    if (
        keys["d"] ||
        keys["arrowright"]
    ) {
        sideways += 1;
    }


    const direction =
        new THREE.Vector3(
            Math.sin(yaw),
            0,
            Math.cos(yaw)
        );


    const right =
        new THREE.Vector3(
            Math.cos(yaw),
            0,
            -Math.sin(yaw)
        );


    camera.position.addScaledVector(
        direction,
        forward * speed
    );


    camera.position.addScaledVector(
        right,
        sideways * speed
    );


    camera.rotation.order = "YXZ";

    camera.rotation.y = yaw;

    camera.rotation.x = pitch;


    renderer.render(
        scene,
        camera
    );
}


// ----------------------------
// RESIZE
// ----------------------------

window.addEventListener(
    "resize",
    function() {

        if (!camera || !renderer) return;

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


// ----------------------------
// SIMPLE AMBIENT SOUND
// ----------------------------

function startAmbientSound() {

    try {

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        if (!AudioContext) return;

        const audio =
            new AudioContext();

        const oscillator =
            audio.createOscillator();

        const gain =
            audio.createGain();

        oscillator.type = "sine";

        oscillator.frequency.value = 110;

        gain.gain.value = 0.025;

        oscillator.connect(gain);

        gain.connect(
            audio.destination
        );

        oscillator.start();

    } catch (e) {

        console.log(
            "Audio unavailable"
        );
    }
}

</script>

</body>
</html>
""",
    height=900,
)
