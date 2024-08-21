function showTab(tabName) {
    var i;
    var x = document.getElementsByClassName("tabcontent");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block";
}

// Add event listeners for form submissions
document.getElementById('boxForm').addEventListener('submit', function(e) {
    e.preventDefault();
    generateModel('/api/generate-box', new FormData(this), 'boxCanvasContainer');
});

document.getElementById('pipelineForm').addEventListener('submit', function(e) {
    e.preventDefault();
    generateModel('/api/generate-pipeline', new FormData(this), 'pipelineCanvasContainer');
});

document.getElementById('staircaseForm').addEventListener('submit', function(e) {
    e.preventDefault();
    generateModel('/api/generate-staircase', new FormData(this), 'staircaseCanvasContainer');
});

function generateModel(apiUrl, formData, containerId) {
    fetch(apiUrl, {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(formData)),
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadSTLModel(`/static/${data.file_url}`, containerId);
        } else {
            console.error(data.error);
            alert('An error occurred: ' + data.error);
        }
    })
    .catch(error => {
        console.error(error);
        alert('An error occurred: ' + error);
    });
}

function loadSTLModel(url, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear previous content
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.enableZoom = true;

    const loader = new THREE.STLLoader();
    loader.load(url, function(geometry) {
        const material = new THREE.MeshNormalMaterial();
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        camera.position.set(0, 0, 250);
        const animate = function() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        };
        animate();
    });
}

