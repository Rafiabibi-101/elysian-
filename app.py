import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="NEON CITY",
    page_icon="🌃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

components.html(
r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #02030a;
}

canvas {
    display: block;
}

#intro {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(
            circle at center,
            #151b35 0%,
            #050611 45%,
            #010207 100%
        );
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}

#intro h1 {
    margin: 0;
    font-size: clamp(50px, 9vw, 120px);
    letter-spacing: 18px;
    font-weight: 200;
    text-shadow:
        0 0 10px #00eaff,
        0 0 30px #00eaff,
        0 0 70px #ff00c8;
}

#intro p {
    margin-top: 20px;
    color: #a8b4d8;
    letter-spacing: 6px;
    font-size: 14px;
}

#enter {
    margin-top: 45px;
    padding: 16px 45px;
    border: 1px solid #00eaff;
    background: rgba(0, 234, 255, 0.05);
    color: #00eaff;
    border-radius: 4px;
    font-size: 14px;
    letter-spacing: 5px;
    cursor: pointer;
    transition: .25s;
}

#enter:hover {
    background: #00eaff;
    color: #02030a;
    box-shadow:
        0 0 20px #00eaff,
        0 0 60px #00eaff;
}

#title {
    position: fixed;
    top: 20px;
    left: 25px;
    z-index: 10;
    color: rgba(255,255,255,.7);
    font-family: Arial, sans-serif;
    font-size: 12px;
    letter-spacing: 4px;
    opacity: 0;
    transition: 2s;
    text-shadow: 0 0 10px #00eaff;
}
</style>
</head>

<body>

<div id="intro">
    <h1>NEON CITY</h1>
    <p>WELCOME TO THE NIGHT</p>
    <button id="enter">ENTER THE CITY</button>
</div>

<div id="title">
    SECTOR 07 · 02:17 AM
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
let lastX = 0;
let lastY = 0;

let rain;
let cars = [];


// ======================================================
// ENTER
// ======================================================

document.getElementById("enter").onclick = function() {

    document.getElementById("intro").style.display = "none";
    document.getElementById("title").style.opacity = "1";

    started = true;

    init();

    startSound();
};


// ======================================================
// INIT
// ======================================================

function init() {

    scene = new THREE.Scene();

    scene.background =
        new THREE.Color(0x02030b);

    scene.fog =
        new THREE.FogExp2(
            0x070a18,
            0.018
        );


    camera =
        new THREE.PerspectiveCamera(
            72,
            window.innerWidth /
            window.innerHeight,
            0.1,
            1500
        );

    /*
       IMPORTANT:

       The camera starts IN the street,
       not above the city.
    */

    camera.position.set(
        0,
        2.2,
        45
    );


    renderer =
        new THREE.WebGLRenderer({
            antialias: true
        });

    renderer.setPixelRatio(
        Math.min(
            window.devicePixelRatio,
            2
        )
    );

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

    renderer.shadowMap.enabled = true;

    document.body.appendChild(
        renderer.domElement
    );


    clock = new THREE.Clock();


    createSky();

    createLights();

    createRoad();

    createSidewalks();

    createBuildings();

    createStreetLights();

    createNeonSigns();

    createWindows();

    createRain();

    createCars();

    createSteam();

    animate();
}


// ======================================================
// SKY
// ======================================================

function createSky() {

    const sky =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                700,
                32,
                32
            ),
            new THREE.MeshBasicMaterial({
                color: 0x030511,
                side: THREE.BackSide
            })
        );

    scene.add(sky);


    // distant glow

    const glow =
        new THREE.PointLight(
            0x3925ff,
            12,
            500
        );

    glow.position.set(
        0,
        70,
        -400
    );

    scene.add(glow);
}


// ======================================================
// LIGHTING
// ======================================================

function createLights() {

    const ambient =
        new THREE.HemisphereLight(
            0x172040,
            0x020207,
            1.4
        );

    scene.add(ambient);


    const blue =
        new THREE.PointLight(
            0x00aaff,
            8,
            160
        );

    blue.position.set(
        -30,
        15,
        0
    );

    scene.add(blue);


    const pink =
        new THREE.PointLight(
            0xff0088,
            8,
            160
        );

    pink.position.set(
        30,
        12,
        -30
    );

    scene.add(pink);
}


// ======================================================
// ROAD
// ======================================================

function createRoad() {

    const road =
        new THREE.Mesh(
            new THREE.PlaneGeometry(
                40,
                1000
            ),
            new THREE.MeshStandardMaterial({
                color: 0x090b12,
                roughness: 0.18,
                metalness: 0.55
            })
        );

    road.rotation.x =
        -Math.PI / 2;

    road.position.y =
        -0.05;

    scene.add(road);


    // center line

    for (let z = -480; z < 500; z += 18) {

        const line =
            new THREE.Mesh(
                new THREE.PlaneGeometry(
                    0.35,
                    8
                ),
                new THREE.MeshBasicMaterial({
                    color: 0x55ddff
                })
            );

        line.rotation.x =
            -Math.PI / 2;

        line.position.set(
            0,
            0.01,
            z
        );

        scene.add(line);
    }
}


// ======================================================
// SIDEWALKS
// ======================================================

function createSidewalks() {

    for (const x of [-25, 25]) {

        const sidewalk =
            new THREE.Mesh(
                new THREE.BoxGeometry(
                    10,
                    0.8,
                    1000
                ),
                new THREE.MeshStandardMaterial({
                    color: 0x171924,
                    roughness: 0.5
                })
            );

        sidewalk.position.set(
            x,
            0.4,
            0
        );

        scene.add(sidewalk);
    }
}


// ======================================================
// BUILDINGS
// ======================================================

function createBuildings() {

    /*
       Buildings are deliberately placed
       close to the street.

       This creates the feeling that
       the player is surrounded by the city.
    */

    for (let z = -450; z < 450; z += 32) {

        createBuilding(
            -1,
            z
        );

        createBuilding(
            1,
            z
        );
    }
}


function createBuilding(side, z) {

    const width =
        16 + Math.random() * 15;

    const depth =
        24 + Math.random() * 18;

    const height =
        35 + Math.random() * 120;


    const material =
        new THREE.MeshStandardMaterial({
            color:
                Math.random() > .5
                ? 0x101322
                : 0x161529,

            roughness: 0.7,
            metalness: 0.2
        });


    const building =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                width,
                height,
                depth
            ),
            material
        );


    const x =
        side *
        (31 + Math.random() * 10);


    building.position.set(
        x,
        height / 2,
        z
    );


    building.castShadow = true;

    building.receiveShadow = true;

    scene.add(building);


    createBuildingGlow(
        building,
        side
    );
}


// ======================================================
// BUILDING GLOW
// ======================================================

function createBuildingGlow(
    building,
    side
) {

    const height =
        building.geometry.parameters.height;

    const width =
        building.geometry.parameters.width;

    for (
        let y = 8;
        y < height - 5;
        y += 7
    ) {

        if (Math.random() < 0.75) {

            const color =
                Math.random() > 0.5
                ? 0x00eaff
                : 0xff1493;


            const window =
                new THREE.Mesh(
                    new THREE.PlaneGeometry(
                        2.4,
                        1.1
                    ),
                    new THREE.MeshBasicMaterial({
                        color: color,
                        transparent: true,
                        opacity:
                            0.35 +
                            Math.random() * 0.5
                    })
                );


            window.position.set(
                building.position.x -
                side * (width / 2 + 0.03),

                y,

                building.position.z +
                (Math.random() - .5) *
                building.geometry.parameters.depth
            );


            window.rotation.y =
                side > 0
                ? -Math.PI / 2
                : Math.PI / 2;


            scene.add(window);
        }
    }
}


// ======================================================
// NEON SIGNS
// ======================================================

function createNeonSigns() {

    const signs = [
        "NOVA",
        "TOKYO",
        "VOID",
        "SYNTH",
        "NEXUS",
        "ARIA",
        "ZEN",
        "CYBER",
        "LUNA",
        "ECHO",
        "07",
        "NIGHT"
    ];


    for (let i = 0; i < 45; i++) {

        const text =
            signs[
                Math.floor(
                    Math.random() *
                    signs.length
                )
            ];


        const canvas =
            document.createElement(
                "canvas"
            );

        canvas.width = 512;
        canvas.height = 160;


        const ctx =
            canvas.getContext("2d");


        const pink =
            Math.random() > .5;


        ctx.fillStyle =
            "#050510";

        ctx.fillRect(
            0,
            0,
            512,
            160
        );


        ctx.font =
            "bold 70px Arial";

        ctx.textAlign =
            "center";

        ctx.textBaseline =
            "middle";


        ctx.shadowBlur = 30;

        ctx.shadowColor =
            pink
            ? "#ff0088"
            : "#00eaff";


        ctx.fillStyle =
            pink
            ? "#ff39aa"
            : "#35efff";


        ctx.fillText(
            text,
            256,
            80
        );


        const texture =
            new THREE.CanvasTexture(
                canvas
            );


        const sign =
            new THREE.Mesh(
                new THREE.PlaneGeometry(
                    10,
                    3.2
                ),
                new THREE.MeshBasicMaterial({
                    map: texture,
                    transparent: true
                })
            );


        const side =
            Math.random() > .5
            ? -1
            : 1;


        sign.position.set(
            side *
            (29 + Math.random() * 4),

            7 +
            Math.random() * 45,

            -430 +
            Math.random() * 850
        );


        sign.rotation.y =
            side > 0
            ? -Math.PI / 2
            : Math.PI / 2;


        scene.add(sign);
    }
}


// ======================================================
// STREET LIGHTS
// ======================================================

function createStreetLights() {

    for (
        let z = -450;
        z < 450;
        z += 30
    ) {

        createLamp(-19, z);

        createLamp(19, z);
    }
}


function createLamp(x, z) {

    const pole =
        new THREE.Mesh(
            new THREE.CylinderGeometry(
                0.12,
                0.18,
                9
            ),
            new THREE.MeshStandardMaterial({
                color: 0x262935,
                metalness: .8
            })
        );

    pole.position.set(
        x,
        4.5,
        z
    );

    scene.add(pole);


    const light =
        new THREE.PointLight(
            Math.random() > .5
            ? 0x00ddff
            : 0xff1595,

            3,

            35
        );

    light.position.set(
        x,
        9,
        z
    );

    scene.add(light);


    const bulb =
        new THREE.Mesh(
            new THREE.SphereGeometry(
                0.45,
                8,
                8
            ),
            new THREE.MeshBasicMaterial({
                color:
                    Math.random() > .5
                    ? 0x00eaff
                    : 0xff1493
            })
        );

    bulb.position.set(
        x,
        9,
        z
    );

    scene.add(bulb);
}


// ======================================================
// RAIN
// ======================================================

function createRain() {

    const count = 4500;

    const geometry =
        new THREE.BufferGeometry();

    const positions = [];

    for (
        let i = 0;
        i < count;
        i++
    ) {

        positions.push(
            (Math.random() - .5) * 180,
            Math.random() * 100,
            (Math.random() - .5) * 500
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
            color: 0x9edcff,
            size: 0.18,
            transparent: true,
            opacity: 0.65
        });


    rain =
        new THREE.Points(
            geometry,
            material
        );

    scene.add(rain);
}


// ======================================================
// CARS
// ======================================================

function createCars() {

    for (
        let i = 0;
        i < 12;
        i++
    ) {

        const car =
            createCar();


        car.position.set(
            Math.random() > .5
            ? -9
            : 9,

            0.9,

            -400 +
            Math.random() * 800
        );


        car.userData.speed =
            15 +
            Math.random() * 20;


        scene.add(car);

        cars.push(car);
    }
}


function createCar() {

    const group =
        new THREE.Group();


    const body =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                5,
                1.2,
                10
            ),
            new THREE.MeshStandardMaterial({
                color: 0x11141f,
                metalness: .8,
                roughness: .2
            })
        );

    group.add(body);


    const glow =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                3.8,
                .25,
                .2
            ),
            new THREE.MeshBasicMaterial({
                color: 0xff003c
            })
        );


    glow.position.set(
        0,
        0.5,
        5.1
    );

    group.add(glow);


    const head =
        new THREE.Mesh(
            new THREE.BoxGeometry(
                3.8,
                .25,
                .2
            ),
            new THREE.MeshBasicMaterial({
                color: 0xffffff
            })
        );


    head.position.set(
        0,
        0.5,
        -5.1
    );

    group.add(head);


    return group;
}


// ======================================================
// STEAM
// ======================================================

function createSteam() {

    for (
        let i = 0;
        i < 12;
        i++
    ) {

        const steam =
            new THREE.Mesh(
                new THREE.CylinderGeometry(
                    1.5,
                    2,
                    8,
                    12,
                    1,
                    true
                ),
                new THREE.MeshBasicMaterial({
                    color: 0x8895aa,
                    transparent: true,
                    opacity: .07
                })
            );


        steam.position.set(
            (Math.random() > .5
                ? -1
                : 1) *
            (15 + Math.random() * 10),

            4,

            -400 +
            Math.random() * 800
        );


        scene.add(steam);
    }
}


// ======================================================
// MOVEMENT
// ======================================================

window.addEventListener(
    "keydown",
    function(e) {

        keys[
            e.key.toLowerCase()
        ] = true;
    }
);


window.addEventListener(
    "keyup",
    function(e) {

        keys[
            e.key.toLowerCase()
        ] = false;
    }
);


// ======================================================
// MOUSE
// ======================================================

window.addEventListener(
    "mousedown",
    function(e) {

        if (!started) return;

        dragging = true;

        lastX = e.clientX;
        lastY = e.clientY;
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

        if (!dragging || !started)
            return;


        const dx =
            e.clientX - lastX;

        const dy =
            e.clientY - lastY;


        lastX = e.clientX;
        lastY = e.clientY;


        yaw -= dx * .0025;

        pitch -= dy * .002;


        pitch =
            Math.max(
                -1.3,
                Math.min(
                    1.3,
                    pitch
                )
            );
    }
);


// ======================================================
// ANIMATION
// ======================================================

function animate() {

    requestAnimationFrame(
        animate
    );


    const delta =
        clock.getDelta();


    // ------------------
    // CAMERA
    // ------------------

    const speed =
        18 * delta;


    let forward = 0;
    let side = 0;


    if (
        keys["w"] ||
        keys["arrowup"]
    )
        forward += 1;


    if (
        keys["s"] ||
        keys["arrowdown"]
    )
        forward -= 1;


    if (
        keys["a"] ||
        keys["arrowleft"]
    )
        side -= 1;


    if (
        keys["d"] ||
        keys["arrowright"]
    )
        side += 1;


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
        side * speed
    );


    camera.position.y = 2.2;


    camera.rotation.order =
        "YXZ";

    camera.rotation.y =
        yaw;

    camera.rotation.x =
        pitch;


    // ------------------
    // RAIN
    // ------------------

    if (rain) {

        const positions =
            rain.geometry.attributes
                .position.array;


        for (
            let i = 1;
            i < positions.length;
            i += 3
        ) {

            positions[i] -=
                45 * delta;


            if (positions[i] < 0) {

                positions[i] =
                    100;
            }
        }


        rain.geometry.attributes
            .position.needsUpdate = true;
    }


    // ------------------
    // CARS
    // ------------------

    for (const car of cars) {

        car.position.z +=
            car.userData.speed *
            delta;


        if (car.position.z > 450) {

            car.position.z = -450;
        }
    }


    renderer.render(
        scene,
        camera
    );
}


// ======================================================
// RESIZE
// ======================================================

window.addEventListener(
    "resize",
    function() {

        if (!camera)
            return;


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


// ======================================================
// AMBIENT AUDIO
// ======================================================

function startSound() {

    try {

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;


        if (!AudioContext)
            return;


        const audio =
            new AudioContext();


        const osc =
            audio.createOscillator();


        const gain =
            audio.createGain();


        osc.type = "sine";

        osc.frequency.value =
            48;


        gain.gain.value =
            0.018;


        osc.connect(gain);

        gain.connect(
            audio.destination
        );


        osc.start();

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
