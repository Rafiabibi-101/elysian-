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
<meta name="viewport" content="width=device-width,initial-scale=1">

<style>
html,body{
    margin:0;
    padding:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#02030a;
}

canvas{
    display:block;
}

#intro{
    position:fixed;
    inset:0;
    z-index:100;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    background:
        radial-gradient(
            circle at center,
            rgba(30,20,65,.92),
            rgba(1,2,8,.98)
        );
    color:white;
    font-family:Arial,sans-serif;
    text-align:center;
    transition:opacity 1.5s;
}

#intro h1{
    font-size:clamp(55px,9vw,120px);
    font-weight:200;
    letter-spacing:18px;
    margin:0;
    color:#fff;
    text-shadow:
        0 0 8px #00eaff,
        0 0 25px #00eaff,
        0 0 60px #ff0088;
}

#intro p{
    margin-top:18px;
    letter-spacing:7px;
    color:#aab4d0;
}

#enter{
    margin-top:45px;
    padding:17px 45px;
    background:rgba(0,220,255,.05);
    border:1px solid #00eaff;
    color:#00eaff;
    font-size:14px;
    letter-spacing:5px;
    cursor:pointer;
    border-radius:3px;
    box-shadow:0 0 15px rgba(0,234,255,.2);
}

#enter:hover{
    background:#00eaff;
    color:#02030a;
    box-shadow:
        0 0 20px #00eaff,
        0 0 70px #00eaff;
}

#hud{
    position:fixed;
    top:18px;
    left:20px;
    z-index:10;
    color:rgba(255,255,255,.65);
    font:12px Arial;
    letter-spacing:3px;
    opacity:0;
    transition:opacity 2s;
    pointer-events:none;
}
</style>
</head>

<body>

<div id="intro">
    <h1>NEON CITY</h1>
    <p>THE CITY NEVER SLEEPS</p>
    <button id="enter">ENTER</button>
</div>

<div id="hud">
    NEON DISTRICT · 02:17 AM
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<script>

let scene;
let camera;
let renderer;
let clock;

let yaw = 0;
let pitch = 0;

const keys = {};

let mouseDown = false;
let lastX = 0;
let lastY = 0;

let rain;
let cars = [];


// ============================================================
// START
// ============================================================

window.addEventListener("load", function(){

    createWorld();

    document.getElementById("enter").onclick = function(){

        document.getElementById("intro").style.opacity = "0";
        document.getElementById("hud").style.opacity = "1";

        setTimeout(function(){
            document.getElementById("intro").style.display = "none";
        },1500);

        startAudio();
    };

});


// ============================================================
// CREATE WORLD
// ============================================================

function createWorld(){

    scene = new THREE.Scene();

    scene.background =
        new THREE.Color(0x02030b);

    scene.fog =
        new THREE.FogExp2(
            0x070817,
            0.008
        );


    camera =
        new THREE.PerspectiveCamera(
            70,
            window.innerWidth /
            window.innerHeight,
            .1,
            2000
        );


    /*
        THE PLAYER IS HERE.

        Surrounded by buildings.
    */

    camera.position.set(
        0,
        2.4,
        30
    );


    renderer =
        new THREE.WebGLRenderer({
            antialias:true
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


    document.body.appendChild(
        renderer.domElement
    );


    clock =
        new THREE.Clock();


    createSky();
    createLights();
    createRoad();
    createBuildings();
    createNeon();
    createStreetLights();
    createCars();
    createRain();
    createSteam();
    createOverheadStructures();

    setupControls();

    animate();
}


// ============================================================
// SKY
// ============================================================

function createSky(){

    const sky =
        new THREE.Mesh(

            new THREE.SphereGeometry(
                1000,
                32,
                32
            ),

            new THREE.MeshBasicMaterial({
                color:0x02030c,
                side:THREE.BackSide
            })

        );

    scene.add(sky);


    // moon

    const moon =
        new THREE.Mesh(

            new THREE.SphereGeometry(
                18,
                32,
                32
            ),

            new THREE.MeshBasicMaterial({
                color:0x9bb8ff
            })

        );

    moon.position.set(
        -180,
        170,
        -400
    );

    scene.add(moon);
}


// ============================================================
// LIGHTS
// ============================================================

function createLights(){

    const ambient =
        new THREE.HemisphereLight(
            0x24345e,
            0x020207,
            1.5
        );

    scene.add(ambient);


    const blue =
        new THREE.PointLight(
            0x00bfff,
            18,
            350
        );

    blue.position.set(
        -35,
        30,
        -80
    );

    scene.add(blue);


    const pink =
        new THREE.PointLight(
            0xff0088,
            18,
            350
        );

    pink.position.set(
        35,
        25,
        -140
    );

    scene.add(pink);
}


// ============================================================
// ROAD
// ============================================================

function createRoad(){

    const road =
        new THREE.Mesh(

            new THREE.PlaneGeometry(
                50,
                1800
            ),

            new THREE.MeshStandardMaterial({
                color:0x070910,
                roughness:.16,
                metalness:.7
            })

        );


    road.rotation.x =
        -Math.PI/2;

    scene.add(road);


    // wet road strips

    for(let i=-2;i<=2;i++){

        const strip =
            new THREE.Mesh(

                new THREE.PlaneGeometry(
                    .25,
                    1800
                ),

                new THREE.MeshBasicMaterial({
                    color:
                        i===0
                        ? 0x00aaff
                        : 0x22283d,
                    transparent:true,
                    opacity:
                        i===0?.55:.35
                })

            );

        strip.rotation.x =
            -Math.PI/2;

        strip.position.set(
            i*7,
            .015,
            0
        );

        scene.add(strip);
    }


    // sidewalks

    for(const x of [-32,32]){

        const sidewalk =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    14,
                    1,
                    1800
                ),

                new THREE.MeshStandardMaterial({
                    color:0x11131d,
                    roughness:.6
                })

            );

        sidewalk.position.set(
            x,
            .5,
            0
        );

        scene.add(sidewalk);
    }
}


// ============================================================
// BUILDINGS
// ============================================================

function createBuildings(){

    /*
       DENSE CITY WALLS

       Buildings are placed continuously
       on both sides of the street.
    */

    for(
        let z=-850;
        z<850;
        z+=30
    ){

        createBuilding(-1,z);
        createBuilding(1,z);

    }


    // distant towers

    for(let i=0;i<80;i++){

        const b =
            createBuilding(
                Math.random()>.5?1:-1,
                -850+
                Math.random()*1700
            );

        b.position.x *= 1.7;
    }
}


function createBuilding(side,z){

    const width =
        18+
        Math.random()*18;

    const depth =
        24+
        Math.random()*28;

    const height =
        45+
        Math.random()*150;


    const colors=[
        0x0b0d19,
        0x101223,
        0x131528,
        0x0d101c,
        0x18172a
    ];


    const material =
        new THREE.MeshStandardMaterial({
            color:
                colors[
                    Math.floor(
                        Math.random()*colors.length
                    )
                ],
            roughness:.6,
            metalness:.25
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


    building.position.set(

        side *
        (36+
        Math.random()*12),

        height/2,

        z
    );


    scene.add(building);


    createWindows(
        building,
        side,
        width,
        depth,
        height
    );


    return building;
}


// ============================================================
// WINDOWS
// ============================================================

function createWindows(
    building,
    side,
    width,
    depth,
    height
){

    const windowColors=[
        0x00eaff,
        0xff0088,
        0xffb300,
        0x725cff
    ];


    for(
        let y=7;
        y<height-5;
        y+=7
    ){

        for(
            let i=0;
            i<4;
            i++
        ){

            if(Math.random()<.68){

                const color =
                    windowColors[
                        Math.floor(
                            Math.random()*
                            windowColors.length
                        )
                    ];


                const w =
                    new THREE.Mesh(

                        new THREE.PlaneGeometry(
                            2.7,
                            1.25
                        ),

                        new THREE.MeshBasicMaterial({
                            color:color,
                            transparent:true,
                            opacity:
                                .3+
                                Math.random()*.7
                        })

                    );


                w.position.set(

                    building.position.x
                    -
                    side*
                    (width/2+.03),

                    y,

                    building.position.z
                    +
                    (-depth/2+3+i*5)
                );


                w.rotation.y =
                    side>0
                    ? -Math.PI/2
                    : Math.PI/2;


                scene.add(w);
            }
        }
    }
}


// ============================================================
// NEON SIGNS
// ============================================================

function createNeon(){

    const words=[
        "NOVA",
        "NEON",
        "VOID",
        "TOKYO",
        "NEXUS",
        "SYNTH",
        "LUNA",
        "ARIA",
        "CYBER",
        "ZEN",
        "BAR",
        "HOTEL",
        "CLUB",
        "24H"
    ];


    for(let i=0;i<100;i++){

        const canvas =
            document.createElement("canvas");

        canvas.width=512;
        canvas.height=180;


        const ctx =
            canvas.getContext("2d");


        const pink =
            Math.random()>.5;


        ctx.fillStyle="#05050c";

        ctx.fillRect(
            0,0,512,180
        );


        ctx.font=
            "bold 65px Arial";

        ctx.textAlign="center";
        ctx.textBaseline="middle";

        ctx.shadowBlur=35;

        ctx.shadowColor=
            pink
            ? "#ff0088"
            : "#00eaff";


        ctx.fillStyle=
            pink
            ? "#ff3bac"
            : "#42efff";


        ctx.fillText(
            words[
                Math.floor(
                    Math.random()*
                    words.length
                )
            ],
            256,
            90
        );


        const texture =
            new THREE.CanvasTexture(
                canvas
            );


        const sign =
            new THREE.Mesh(

                new THREE.PlaneGeometry(
                    12,
                    4.2
                ),

                new THREE.MeshBasicMaterial({
                    map:texture,
                    transparent:true
                })

            );


        const side =
            Math.random()>.5
            ? 1
            : -1;


        sign.position.set(

            side*
            (30+
            Math.random()*9),

            7+
            Math.random()*100,

            -820+
            Math.random()*1640

        );


        sign.rotation.y =
            side>0
            ? -Math.PI/2
            : Math.PI/2;


        scene.add(sign);
    }
}


// ============================================================
// STREET LIGHTS
// ============================================================

function createStreetLights(){

    for(
        let z=-800;
        z<800;
        z+=28
    ){

        createLamp(-18,z);
        createLamp(18,z);
    }
}


function createLamp(x,z){

    const pole =
        new THREE.Mesh(

            new THREE.CylinderGeometry(
                .12,
                .18,
                9
            ),

            new THREE.MeshStandardMaterial({
                color:0x292d3a,
                metalness:.8
            })

        );


    pole.position.set(
        x,
        4.5,
        z
    );

    scene.add(pole);


    const color =
        Math.random()>.5
        ? 0x00eaff
        : 0xff0088;


    const lamp =
        new THREE.PointLight(
            color,
            5,
            45
        );


    lamp.position.set(
        x,
        9,
        z
    );


    scene.add(lamp);
}


// ============================================================
// CARS
// ============================================================

function createCars(){

    for(let i=0;i<24;i++){

        const car =
            new THREE.Group();


        const body =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    5,
                    1.4,
                    9
                ),

                new THREE.MeshStandardMaterial({
                    color:
                        Math.random()>.5
                        ? 0x101522
                        : 0x17101e,
                    metalness:.8,
                    roughness:.2
                })

            );


        body.position.y=1;

        car.add(body);


        const neon =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    4,
                    .15,
                    .2
                ),

                new THREE.MeshBasicMaterial({
                    color:0xff004c
                })

            );


        neon.position.set(
            0,
            1.5,
            4.55
        );

        car.add(neon);


        const headlights =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    4,
                    .15,
                    .2
                ),

                new THREE.MeshBasicMaterial({
                    color:0x9eefff
                })

            );


        headlights.position.set(
            0,
            1.5,
            -4.55
        );

        car.add(headlights);


        car.position.set(

            Math.random()>.5
            ? -9
            : 9,

            0,

            -800+
            Math.random()*1600

        );


        car.userData.speed=
            20+
            Math.random()*30;


        scene.add(car);

        cars.push(car);
    }
}


// ============================================================
// RAIN
// ============================================================

function createRain(){

    const count=7000;

    const geometry =
        new THREE.BufferGeometry();

    const positions=[];


    for(let i=0;i<count;i++){

        positions.push(

            (Math.random()-.5)*160,

            Math.random()*120,

            (Math.random()-.5)*700
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
            color:0x9ddfff,
            size:.16,
            transparent:true,
            opacity:.65
        });


    rain =
        new THREE.Points(
            geometry,
            material
        );


    scene.add(rain);
}


// ============================================================
// STEAM
// ============================================================

function createSteam(){

    for(let i=0;i<30;i++){

        const steam =
            new THREE.Mesh(

                new THREE.CylinderGeometry(
                    1.5,
                    2.5,
                    10,
                    10,
                    1,
                    true
                ),

                new THREE.MeshBasicMaterial({
                    color:0x8790a5,
                    transparent:true,
                    opacity:.055,
                    side:THREE.DoubleSide
                })

            );


        steam.position.set(

            Math.random()>.5
            ? -25
            : 25,

            5,

            -800+
            Math.random()*1600
        );


        scene.add(steam);
    }
}


// ============================================================
// OVERHEAD CITY STRUCTURES
// ============================================================

function createOverheadStructures(){

    for(
        let z=-700;
        z<700;
        z+=100
    ){

        const bridge =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    85,
                    2,
                    5
                ),

                new THREE.MeshStandardMaterial({
                    color:0x151a2a,
                    metalness:.8
                })

            );


        bridge.position.set(
            0,
            32+
            Math.random()*25,
            z
        );


        scene.add(bridge);


        // neon strip

        const glow =
            new THREE.Mesh(

                new THREE.BoxGeometry(
                    80,
                    .25,
                    .25
                ),

                new THREE.MeshBasicMaterial({
                    color:
                        Math.random()>.5
                        ? 0xff0088
                        : 0x00eaff
                })

            );


        glow.position.set(
            0,
            bridge.position.y-1,
            z
        );


        scene.add(glow);
    }
}


// ============================================================
// CONTROLS
// ============================================================

function setupControls(){

    window.addEventListener(
        "keydown",
        function(e){

            keys[
                e.key.toLowerCase()
            ]=true;
        }
    );


    window.addEventListener(
        "keyup",
        function(e){

            keys[
                e.key.toLowerCase()
            ]=false;
        }
    );


    window.addEventListener(
        "mousedown",
        function(e){

            mouseDown=true;

            lastX=e.clientX;
            lastY=e.clientY;
        }
    );


    window.addEventListener(
        "mouseup",
        function(){

            mouseDown=false;
        }
    );


    window.addEventListener(
        "mousemove",
        function(e){

            if(!mouseDown)
                return;


            const dx=
                e.clientX-lastX;

            const dy=
                e.clientY-lastY;


            lastX=e.clientX;
            lastY=e.clientY;


            yaw-=dx*.0025;

            pitch-=dy*.002;


            pitch=
                Math.max(
                    -1.2,
                    Math.min(
                        1.2,
                        pitch
                    )
                );
        }
    );
}


// ============================================================
// ANIMATION
// ============================================================

function animate(){

    requestAnimationFrame(
        animate
    );


    const delta =
        clock.getDelta();


    // -------------------------
    // MOVEMENT
    // -------------------------

    const speed=
        22*delta;


    let forward=0;
    let sideways=0;


    if(
        keys["w"] ||
        keys["arrowup"]
    )
        forward=1;


    if(
        keys["s"] ||
        keys["arrowdown"]
    )
        forward=-1;


    if(
        keys["a"] ||
        keys["arrowleft"]
    )
        sideways=-1;


    if(
        keys["d"] ||
        keys["arrowright"]
    )
        sideways=1;


    const direction=
        new THREE.Vector3(
            Math.sin(yaw),
            0,
            Math.cos(yaw)
        );


    const right=
        new THREE.Vector3(
            Math.cos(yaw),
            0,
            -Math.sin(yaw)
        );


    camera.position.addScaledVector(
        direction,
        forward*speed
    );


    camera.position.addScaledVector(
        right,
        sideways*speed
    );


    camera.position.y=2.4;


    camera.rotation.order="YXZ";

    camera.rotation.y=yaw;

    camera.rotation.x=pitch;


    // -------------------------
    // RAIN
    // -------------------------

    if(rain){

        const p=
            rain.geometry
            .attributes
            .position
            .array;


        for(
            let i=1;
            i<p.length;
            i+=3
        ){

            p[i]-=55*delta;


            if(p[i]<0)
                p[i]=120;
        }


        rain.geometry
            .attributes
            .position
            .needsUpdate=true;
    }


    // -------------------------
    // CARS
    // -------------------------

    for(const car of cars){

        car.position.z +=
            car.userData.speed*
            delta;


        if(
            car.position.z>850
        ){

            car.position.z=-850;
        }
    }


    renderer.render(
        scene,
        camera
    );
}


// ============================================================
// RESIZE
// ============================================================

window.addEventListener(
    "resize",
    function(){

        camera.aspect=
            window.innerWidth/
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }
);


// ============================================================
// AUDIO
// ============================================================

function startAudio(){

    try{

        const AudioContext=
            window.AudioContext ||
            window.webkitAudioContext;


        if(!AudioContext)
            return;


        const audio=
            new AudioContext();


        const oscillator=
            audio.createOscillator();


        const gain=
            audio.createGain();


        oscillator.type="sine";

        oscillator.frequency.value=48;

        gain.gain.value=.012;


        oscillator.connect(gain);

        gain.connect(
            audio.destination
        );


        oscillator.start();

    }catch(e){}
}

</script>

</body>
</html>
""",
    height=900,
)
