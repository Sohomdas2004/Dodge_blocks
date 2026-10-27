import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Dodge the Falling Blocks", page_icon="🎮", layout="centered")

st.title("🎮 Dodge the Falling Blocks")
st.write("Move with **← / →** or **A / D**. Avoid the red blocks and try to beat your score!")

game_html = r"""
<div style="font-family:Arial,sans-serif;text-align:center;color:#f5f5f5;background:#161b28;padding:12px;border-radius:14px;">
  <canvas id="game" width="600" height="700"
    style="width:100%;max-width:600px;height:auto;border:1px solid #30384c;border-radius:10px;display:block;margin:auto;background:#161b28;touch-action:manipulation;"></canvas>
  <div style="margin-top:10px;color:#cbd5e1;font-size:14px">
    Keyboard: ← → or A / D &nbsp; • &nbsp; Mobile: tap left/right side of the game
  </div>
  <button id="restart" style="margin-top:10px;padding:9px 18px;border:0;border-radius:8px;background:#ffd246;color:#171717;font-weight:bold;cursor:pointer">Restart game</button>
</div>

<script>
(() => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const restartBtn = document.getElementById("restart");
  const W = canvas.width, H = canvas.height;
  let player, blocks, score, lastTime, spawnTimer, gameOver, keys, touchDir, animationId;

  function reset() {
    player = { x: W / 2 - 27, y: H - 75, w: 54, h: 24, speed: 390 };
    blocks = [];
    score = 0;
    lastTime = performance.now();
    spawnTimer = 0;
    gameOver = false;
    keys = {};
    touchDir = 0;
    if (animationId) cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame(loop);
  }

  window.addEventListener("keydown", e => {
    if (["ArrowLeft", "ArrowRight", "a", "d", "A", "D"].includes(e.key)) e.preventDefault();
    keys[e.key.toLowerCase()] = true;
  });
  window.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);

  canvas.addEventListener("pointerdown", e => {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    touchDir = x < 0.5 ? -1 : 1;
  });
  canvas.addEventListener("pointerup", () => touchDir = 0);
  canvas.addEventListener("pointercancel", () => touchDir = 0);
  restartBtn.addEventListener("click", reset);

  function draw() {
    ctx.fillStyle = "#161b28";
    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle = "#20283a";
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 50) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += 50) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }

    // Player
    ctx.fillStyle = "#46a0ff";
    ctx.beginPath();
    ctx.roundRect(player.x, player.y, player.w, player.h, 8);
    ctx.fill();
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(player.x + 10, player.y + 5, 7, 5);
    ctx.fillRect(player.x + player.w - 17, player.y + 5, 7, 5);

    // Falling blocks
    blocks.forEach(b => {
      ctx.fillStyle = "#f54b55";
      ctx.beginPath(); ctx.roundRect(b.x, b.y, b.size, b.size, 6); ctx.fill();
      ctx.fillStyle = "#ffd246";
      ctx.beginPath(); ctx.roundRect(b.x + 7, b.y + 7, 8, 8, 2); ctx.fill();
    });

    ctx.fillStyle = "#f5f5f5";
    ctx.font = "bold 27px Arial";
    ctx.fillText("Score: " + Math.floor(score), 18, 38);

    if (gameOver) {
      ctx.fillStyle = "rgba(0,0,0,0.72)";
      ctx.fillRect(0, 0, W, H);
      ctx.textAlign = "center";
      ctx.fillStyle = "#f54b55";
      ctx.font = "bold 58px Arial";
      ctx.fillText("GAME OVER", W / 2, H / 2 - 45);
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 30px Arial";
      ctx.fillText("Your score: " + Math.floor(score), W / 2, H / 2 + 5);
      ctx.fillStyle = "#ffd246";
      ctx.font = "24px Arial";
      ctx.fillText("Press Restart game below", W / 2, H / 2 + 50);
      ctx.textAlign = "left";
    }
  }

  function loop(now) {
    const dt = Math.min((now - lastTime) / 1000, 0.04);
    lastTime = now;

    if (!gameOver) {
      score += dt;
      let direction = 0;
      if (keys["arrowleft"] || keys["a"]) direction -= 1;
      if (keys["arrowright"] || keys["d"]) direction += 1;
      if (touchDir) direction = touchDir;
      player.x += direction * player.speed * dt;
      player.x = Math.max(0, Math.min(W - player.w, player.x));

      spawnTimer += dt;
      const interval = Math.max(0.26, 0.85 - score * 0.004);
      if (spawnTimer >= interval) {
        spawnTimer = 0;
        const size = 34;
        blocks.push({
          x: Math.random() * (W - size),
          y: -size,
          size,
          speed: 240 + Math.random() * 150 + Math.min(score * 3, 240)
        });
      }

      blocks.forEach(b => b.y += b.speed * dt);
      blocks = blocks.filter(b => b.y < H + b.size);

      for (const b of blocks) {
        if (player.x < b.x + b.size && player.x + player.w > b.x &&
            player.y < b.y + b.size && player.y + player.h > b.y) {
          gameOver = true;
          break;
        }
      }
    }

    draw();
    if (!gameOver) animationId = requestAnimationFrame(loop);
  }

  // roundRect is supported by current browsers; provide a fallback for older ones.
  if (!CanvasRenderingContext2D.prototype.roundRect) {
    CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
      r = Math.min(r, w / 2, h / 2);
      this.beginPath();
      this.moveTo(x + r, y); this.arcTo(x + w, y, x + w, y + h, r);
      this.arcTo(x + w, y + h, x, y + h, r); this.arcTo(x, y + h, x, y, r);
      this.arcTo(x, y, x + w, y, r); this.closePath();
      return this;
    };
  }

  reset();
})();
</script>
"""

components.html(game_html, height=820, scrolling=False)

with st.expander("Run this app locally"):
    st.code("python -m pip install -r requirements.txt\nstreamlit run app.py", language="bash")
    st.caption("This is a browser-playable adaptation of the original Pygame game. A desktop Pygame window itself cannot be embedded directly in a Streamlit page.")
