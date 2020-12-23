


var div = document.getElementById("model-3d");
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize(div.offsetWidth, div.offsetHeight);
div.appendChild( renderer.domElement );

const geometry = new THREE.BoxGeometry();
//const material = new THREE.MeshBasicMaterial( { color: 0xddccbb80 } );
var material = new THREE.MeshPhongMaterial({
    vertexColors: THREE.VertexColors,
    //wireframe: true,
    //wireframeLinewidth: 2,
});
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

const light1 = new THREE.PointLight(0xff0044);
light1.position.set(-100, 100, 200);
scene.add(light1);

camera.position.z = 3;
cube.rotation.x += 0.4;

renderer.setClearColor( 0xffffff, 1);

var input_height = document.getElementById("id_height");
var input_lenght = document.getElementById("id_lenght");
var input_width = document.getElementById("id_width");
var div_btu_suggested = document.getElementById("btu-suggested");
var div_btu_required = document.getElementById("btu-required");
var check = document.getElementById("id_terms");
var alert_1 = document.getElementById("alert-1");
var alert_2 = document.getElementById("alert-2");
try {
    var url_item_list = URL["store-item-list"];
} catch (error) {
    var url_item_list = "";
}

input_height.onchange = calculateBTU;
input_height.onclick = calculateBTU;
input_height.oninput = calculateBTU;
input_lenght.onchange = calculateBTU;
input_lenght.onclick = calculateBTU;
input_lenght.oninput = calculateBTU;
input_width.onchange = calculateBTU;
input_width.onclikc = calculateBTU;
input_width.oninput = calculateBTU;
check.onchange = calculateBTU;
check.onclick = calculateBTU;


function animate() {
    requestAnimationFrame( animate );
    //cube.rotation.x += 0.01;
    cube.rotation.y += 0.001;
    if (input_lenght.value > 100) {
        input_lenght.value = 100;
    }
    if (input_height.value > 100) {
        input_height.value = 100;
    }
    if (input_width.value > 100) {
        input_width.value = 100;
    }
    cube.scale.x = input_width.value / 10;
    cube.scale.y = input_height.value / 10;
    cube.scale.z = input_lenght.value / 10;
    renderer.render( scene, camera );
}
animate();



function calculateBTU() {
    if (check.checked) {
        alert_1.classList.add("d-none");
        alert_2.classList.add("d-none");

        with(Math){
            let a = parseFloat(input_lenght.value) * 0.312;
            let b = parseFloat(input_width.value) * 0.312;
            let c = parseFloat(input_height.value) * 0.312;
            let d = 4;
            let e = 0;
            let units3 = 165;
            
            let tmp2 = (d + e) * 400;
            tmp2 = Math.floor((tmp2 * 100) + 0.5) / 100;
            let tmp = a * b * c;
            tmp = Math.floor((tmp * 100) + 0.5) / 100;
            tmp = tmp * units3;
            tmp = tmp + tmp2;
            tmp = Math.floor((tmp * 100) + 0.5) / 100;

            div_btu_required.innerHTML = intcomma(tmp) + " BTU";

            switch(true){
                case tmp >= 1 && tmp <= 9000:
                    div_btu_suggested.innerHTML = intcomma(9000) + " BTU" + '<a href="'+url_item_list+'?btu=9000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 9001 && tmp <= 12000:
                    div_btu_suggested.innerHTML = intcomma(12000) + " BTU" + '<a href="'+url_item_list+'?btu=12000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 12001 && tmp <= 18000:
                    div_btu_suggested.innerHTML = intcomma(18000) + " BTU" + '<a href="'+url_item_list+'?btu=18000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 18001 && tmp <= 24000:
                    div_btu_suggested.innerHTML = intcomma(24000) + " BTU" + '<a href="'+url_item_list+'?btu=24000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 24001 && tmp <= 36000:
                    div_btu_suggested.innerHTML = intcomma(36000) + " BTU" + '<a href="'+url_item_list+'?btu=36000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 36001 && tmp <= 48000:
                    div_btu_suggested.innerHTML = intcomma(48000) + " BTU" + '<a href="'+url_item_list+'?btu=48000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp >= 48001 && tmp <= 60000:
                    div_btu_suggested.innerHTML = intcomma(60000) + " BTU" + '<a href="'+url_item_list+'?btu=60000" id="suggested_items_link" class="btn btn-block btn-light border mt-1">Ver equipos recomendados</a>';
                    break;
                case tmp > 60001:
                    div_btu_suggested.innerHTML = div_btu_required.innerHTML;
                    alert_2.classList.remove("d-none");
                default:
            }
        }
    }
    else{ 
        alert_1.classList.remove("d-none");
        div_btu_required.innerHTML = "";
        div_btu_suggested.innerHTML = "";
        check.focus();
    }
}