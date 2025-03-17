import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.136.0/build/three.module.js';

// Scene Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Load Earth Texture
const textureLoader = new THREE.TextureLoader();
textureLoader.load('textures/alpha.jpg', (texture) => {
    createDottedEarth(texture);
});

function createDottedEarth(texture) {
    const sphereGeometry = new THREE.BufferGeometry();
    const radius = 5;
    const segments = 64;
    const positions = [];
    const colors = [];
    const color = new THREE.Color();

    // Create a canvas to extract pixel color data
    const canvas = document.createElement('canvas');
    canvas.width = texture.image.width;
    canvas.height = texture.image.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(texture.image, 0, 0);
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;

    // Generate Points for Sphere
    for (let i = 0; i < segments; i++) {
        for (let j = 0; j < segments; j++) {
            const theta = (i / segments) * Math.PI;
            const phi = (j / segments) * 2 * Math.PI;

            const x = radius * Math.sin(theta) * Math.cos(phi);
            const y = radius * Math.sin(theta) * Math.sin(phi);
            const z = radius * Math.cos(theta);

            positions.push(x, y, z);

            // Convert spherical coordinates to UV mapping
            const u = j / segments;
            const v = i / segments;
            const pixelX = Math.floor(u * canvas.width);
            const pixelY = Math.floor(v * canvas.height);
            const index = (pixelY * canvas.width + pixelX) * 4;

            // Extract RGB values from the image
            const r = imageData[index] / 255;
            const g = imageData[index + 1] / 255;
            const b = imageData[index + 2] / 255;
            color.setRGB(r, g, b);

            colors.push(color.r, color.g, color.b);
        }
    }

    sphereGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    sphereGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const sphereMaterial = new THREE.PointsMaterial({
        vertexColors: true,
        size: 0.05,
    });

    const sphere = new THREE.Points(sphereGeometry, sphereMaterial);
    scene.add(sphere);

    camera.position.z = 10;

    // Mouse Drag Rotation
    let isDragging = false;
    let previousMouseX = 0;

    document.addEventListener("mousedown", (event) => {
        isDragging = true;
        previousMouseX = event.clientX;
    });

    document.addEventListener("mouseup", () => {
        isDragging = false;
    });

    document.addEventListener("mousemove", (event) => {
        if (isDragging) {
            let deltaX = event.clientX - previousMouseX;
            sphere.rotation.y += deltaX * 0.005;
            previousMouseX = event.clientX;
        }
    });

    // Animation Loop
    function animate() {
        requestAnimationFrame(animate);
        sphere.rotation.y += 0.002;  // Slow rotation effect
        renderer.render(scene, camera);
    }

    animate();

    // Resize Handling
    window.addEventListener('resize', () => {
        renderer.setSize(window.innerWidth, window.innerHeight);
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
    });
}
