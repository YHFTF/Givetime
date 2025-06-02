class Sakura {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.flowers = [];
    this.maxFlowers = 40;
    this.image = new Image();
    this.image.src = "/static/main/images/sakura.png"; // 실제 경로에 맞게 조정
    this.image.onload = () => {
      this.init();
      requestAnimationFrame(() => this.animate());
    };
  }

  init() {
    this.resize();
    window.addEventListener("resize", () => this.resize());

    for (let i = 0; i < this.maxFlowers; i++) {
      this.flowers.push(this.createFlower());
    }
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createFlower() {
    return {
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      size: 20 + Math.random() * 20,
      vx: -0.5 + Math.random(),
      vy: 1 + Math.random() * 2,
      angle: Math.random() * Math.PI * 2,
      rotation: Math.random() * 0.05,
    };
  }

  drawFlower(f) {
    const { x, y, size, angle } = f;
    this.ctx.save();
    this.ctx.translate(x, y);
    this.ctx.rotate(angle);
    this.ctx.drawImage(this.image, -size / 2, -size / 2, size, size);
    this.ctx.restore();
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    for (let i = 0; i < this.flowers.length; i++) {
      let f = this.flowers[i];
      f.x += f.vx;
      f.y += f.vy;
      f.angle += f.rotation;

      if (
        f.y > this.canvas.height ||
        f.x > this.canvas.width + 50 ||
        f.x < -50
      ) {
        this.flowers[i] = this.createFlower();
        this.flowers[i].y = 0;
      }

      this.drawFlower(f);
    }

    requestAnimationFrame(() => this.animate());
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("sakuraCanvas");
  if (canvas) new Sakura(canvas);
});
