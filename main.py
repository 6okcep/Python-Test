import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Retro Pong", page_icon="🏓", layout="centered")
st.title("🏓 Retro Pong")
st.caption("A tiny arcade classic — move your paddle and beat the computer.")
st.balloons()

components.html(
    """
    <style>
      * { box-sizing: border-box; }
      body { margin: 0; background: #090b12; color: #f6f7fb; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; display: flex; justify-content: center; }
      .machine { width: min(760px, 100%); padding: 12px 8px 4px; }
      .screen { border: 3px solid #34384b; border-radius: 12px; padding: 10px; background: #111522; box-shadow: 0 0 0 3px #171a28, 0 16px 36px #0008; }
      canvas { display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; background: #05070b; border: 2px solid #252a3c; border-radius: 4px; outline: none; image-rendering: pixelated; touch-action: none; }
      .hud { display: flex; justify-content: space-between; gap: 12px; padding: 9px 4px 2px; color: #9aa3bd; font-size: 12px; }
      .hud strong { color: #f5d76e; font-size: 18px; }
      .buttons { display: flex; justify-content: center; gap: 8px; margin-top: 8px; }
      button { border: 1px solid #4f5875; border-radius: 6px; background: #20263a; color: #fff; padding: 8px 14px; font: inherit; cursor: pointer; }
      button:hover { background: #2b3450; }
      .help { margin: 10px 2px 0; text-align: center; color: #8993ae; font-size: 12px; line-height: 1.5; }
      .touch { display: flex; justify-content: space-between; margin-top: 8px; }
      .touch button { width: 48%; font-size: 18px; padding: 9px; user-select: none; }
      @media (min-width: 600px) { .touch { display: none; } }
    </style>
    <main class="machine">
      <div class="screen">
        <canvas id="game" width="640" height="360" tabindex="0" aria-label="Retro Pong game"></canvas>
        <div class="hud"><span>PLAYER <strong id="playerScore">0</strong></span><span id="status">READY</span><span>CPU <strong id="cpuScore">0</strong></span></div>
      </div>
      <div class="buttons"><button id="start">Start game</button><button id="pause">Pause</button><button id="reset">Reset</button></div>
      <div class="touch"><button id="up">▲ Move up</button><button id="down">▼ Move down</button></div>
      <div class="help">Mouse: move over the game · Keyboard: W / S or ↑ / ↓ · First to 7 wins</div>
    </main>
    <script>
      const canvas = document.getElementById('game'), ctx = canvas.getContext('2d');
      const W = canvas.width, H = canvas.height;
      const player = { x: 24, y: H / 2 - 38, w: 10, h: 76, speed: 6 }, cpu = { x: W - 34, y: H / 2 - 38, w: 10, h: 76, speed: 3.7 }, ball = { x: W / 2, y: H / 2, r: 7, vx: 4.2, vy: 2.2 };
      let playerScore = 0, cpuScore = 0, running = false, paused = false, upPressed = false, downPressed = false, mouseY = null, lastTime = 0;
      const $ = (id) => document.getElementById(id);
      function resetBall(direction) { ball.x = W / 2; ball.y = H / 2; ball.vx = direction * 4.2; ball.vy = 4.2 * (Math.random() * 0.9 - 0.45); }
      function resetGame() { playerScore = 0; cpuScore = 0; running = false; paused = false; player.y = cpu.y = H / 2 - 38; resetBall(Math.random() > .5 ? 1 : -1); updateHud(); draw(); }
      function updateHud() { $('playerScore').textContent = playerScore; $('cpuScore').textContent = cpuScore; $('status').textContent = !running ? (playerScore >= 7 || cpuScore >= 7 ? 'GAME OVER' : 'READY') : (paused ? 'PAUSED' : 'PLAY'); }
      function movePaddle(p, amount) { p.y = Math.max(0, Math.min(H - p.h, p.y + amount)); }
      function hit(p) { return ball.x - ball.r < p.x + p.w && ball.x + ball.r > p.x && ball.y - ball.r < p.y + p.h && ball.y + ball.r > p.y; }
      function update(dt) {
        const factor = Math.min(dt / 16.67, 2);
        if (upPressed) movePaddle(player, -player.speed * factor);
        if (downPressed) movePaddle(player, player.speed * factor);
        if (!upPressed && !downPressed && mouseY !== null) player.y = Math.max(0, Math.min(H - player.h, mouseY - player.h / 2));
        movePaddle(cpu, Math.max(-cpu.speed * factor, Math.min(cpu.speed * factor, ball.y - cpu.h / 2 - cpu.y)));
        ball.x += ball.vx * factor; ball.y += ball.vy * factor;
        if (ball.y - ball.r < 0 || ball.y + ball.r > H) { ball.vy *= -1; ball.y = Math.max(ball.r, Math.min(H - ball.r, ball.y)); }
        if (hit(player) && ball.vx < 0) { ball.vx = Math.abs(ball.vx) * 1.04; ball.vy += (ball.y - (player.y + player.h / 2)) * .08; }
        if (hit(cpu) && ball.vx > 0) { ball.vx = -Math.abs(ball.vx) * 1.04; ball.vy += (ball.y - (cpu.y + cpu.h / 2)) * .08; }
        if (ball.x < -20) { cpuScore++; resetBall(1); } if (ball.x > W + 20) { playerScore++; resetBall(-1); }
        if (playerScore >= 7 || cpuScore >= 7) running = false; updateHud();
      }
      function draw() {
        ctx.fillStyle = '#05070b'; ctx.fillRect(0, 0, W, H); ctx.strokeStyle = '#252b40'; ctx.setLineDash([8, 12]); ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(W / 2, 0); ctx.lineTo(W / 2, H); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = '#75e6c4'; ctx.fillRect(player.x, player.y, player.w, player.h); ctx.fillStyle = '#f5d76e'; ctx.fillRect(cpu.x, cpu.y, cpu.w, cpu.h); ctx.fillStyle = '#fff'; ctx.fillRect(ball.x - ball.r, ball.y - ball.r, ball.r * 2, ball.r * 2);
        if (!running) { ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.font = 'bold 20px monospace'; ctx.fillText(playerScore >= 7 ? 'YOU WIN!' : cpuScore >= 7 ? 'CPU WINS' : 'PRESS START', W / 2, H / 2 - 8); ctx.font = '12px monospace'; ctx.fillStyle = '#9aa3bd'; ctx.fillText('First to 7 points', W / 2, H / 2 + 18); }
      }
      function loop(time) { if (!lastTime) lastTime = time; if (running && !paused) update(time - lastTime); lastTime = time; draw(); requestAnimationFrame(loop); }
      function startGame() { if (playerScore >= 7 || cpuScore >= 7) resetGame(); running = true; paused = false; canvas.focus(); updateHud(); }
      $('start').onclick = startGame; $('pause').onclick = () => { if (running) { paused = !paused; updateHud(); } }; $('reset').onclick = resetGame;
      window.addEventListener('keydown', (e) => { if (['ArrowUp','ArrowDown','w','s','W','S',' '].includes(e.key)) e.preventDefault(); if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') upPressed = true; if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') downPressed = true; if (e.key === ' ') startGame(); });
      window.addEventListener('keyup', (e) => { if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') upPressed = false; if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') downPressed = false; });
      function movePaddleToMouse(e) {
        const rect = canvas.getBoundingClientRect();
        mouseY = (e.clientY - rect.top) * (H / rect.height);
      }
      function hold(button, setter) {
        button.onpointerdown = () => { mouseY = null; setter(true); };
        button.onpointerup = button.onpointerleave = () => setter(false);
      }
      hold($('up'), (v) => upPressed = v); hold($('down'), (v) => downPressed = v);
      canvas.addEventListener('mousemove', movePaddleToMouse);
      canvas.addEventListener('pointermove', (e) => { if (!e.pointerType || e.pointerType === 'mouse') movePaddleToMouse(e); });
      canvas.addEventListener('mouseleave', () => { mouseY = null; });
      canvas.onclick = () => canvas.focus(); resetGame(); requestAnimationFrame(loop);
    </script>
    """,
    height=540,
    scrolling=False,
)
