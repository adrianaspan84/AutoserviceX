// === CANVAS SETUP (vienas canvas viskam) ===
const canvas = document.getElementById("auroraCanvas");
const ctx = canvas.getContext("2d");

let w, h;
function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

// === DARK AURORA BACKGROUND (bibliotekos stilius) ===
function drawAurora() {
    const g = ctx.createLinearGradient(0, 0, w, h);
    g.addColorStop(0, "rgba(5, 10, 25, 1)");
    g.addColorStop(0.4, "rgba(20, 0, 40, 0.8)");
    g.addColorStop(0.7, "rgba(0, 30, 60, 0.7)");
    g.addColorStop(1, "rgba(0, 60, 30, 0.7)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
}

// === AUTOMOBILIŲ PAVEIKSLĖLIAI (15 unikalių) ===
let carImages = [
    "/static/img/cars/car1.png",
    "/static/img/cars/car2.png",
    "/static/img/cars/car3.png",
    "/static/img/cars/car4.png",
    "/static/img/cars/car5.png",
    "/static/img/cars/car6.png",
    "/static/img/cars/car7.png",
    "/static/img/cars/car8.png",
    "/static/img/cars/car9.png",
    "/static/img/cars/car10.png",
    "/static/img/cars/car11.png",
    "/static/img/cars/car12.png",
    "/static/img/cars/car13.png",
    "/static/img/cars/car14.png",
    "/static/img/cars/car15.png"
];

// Sumaišome, kad nesikartotų
carImages = carImages.sort(() => Math.random() - 0.5);

// === AUTOMOBILIŲ OBJEKTAI (bibliotekos knygų fizika) ===
const cars = [];
for (let i = 0; i < 15; i++) {
    const img = new Image();
    img.src = carImages[i];

    cars.push({
        x: Math.random() * w,
        y: Math.random() * h,
        width: 140 + Math.random() * 60,
        height: 70 + Math.random() * 30,
        speedX: -0.4 + Math.random() * 0.8,
        speedY: -0.4 + Math.random() * 0.8,
        rotation: Math.random() * Math.PI * 2,
        rotationSpeed: -0.005 + Math.random() * 0.01,
        img: img,
        parallaxFactor: 0.2 + Math.random() * 0.8
    });
}

// === PARALLAX ===
let mouseX = 0, mouseY = 0;
window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX / w - 0.5;
    mouseY = e.clientY / h - 0.5;
});

// === ANIMACIJA (bibliotekos stilius) ===
function animate() {
    ctx.clearRect(0, 0, w, h);

    drawAurora();

    cars.forEach(c => {
        // Judėjimas
        c.x += c.speedX + mouseX * c.parallaxFactor;
        c.y += c.speedY + mouseY * c.parallaxFactor;
        c.rotation += c.rotationSpeed;

        // Wrap-around
        if (c.x < -300) c.x = w + 300;
        if (c.x > w + 300) c.x = -300;
        if (c.y < -300) c.y = h + 300;
        if (c.y > h + 300) c.y = -300;

        // Piešimas
        ctx.save();
        ctx.translate(c.x, c.y);
        ctx.rotate(c.rotation);

        // Glow
        ctx.shadowBlur = 35;
        ctx.shadowColor = "rgba(0, 255, 200, 0.8)";

        ctx.drawImage(c.img, -c.width / 2, -c.height / 2, c.width, c.height);
        ctx.restore();
    });

    requestAnimationFrame(animate);
}

animate();
