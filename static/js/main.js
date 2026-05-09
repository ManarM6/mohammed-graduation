/* ═══════════════════════════════════════
   MOHAMMED GRADUATION - MAIN JAVASCRIPT
   ═══════════════════════════════════════ */

// ── Loading Screen ──
window.addEventListener('load', () => {
  setTimeout(() => {
    const ls = document.getElementById('loading-screen');
    if (ls) ls.classList.add('hidden');
  }, 1200);
});

// ── Confetti Engine ──
const confettiCanvas = document.getElementById('confetti-canvas');
const ctx = confettiCanvas ? confettiCanvas.getContext('2d') : null;

function resizeCanvas() {
  if (!confettiCanvas) return;
  confettiCanvas.width  = window.innerWidth;
  confettiCanvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

let confettiPieces = [];
function launchConfetti() {
  if (!ctx) return;
  const colors = ['#D4AF37','#F5D76E','#9B7E28','#FFFFFF','#FFD700','#FFA500'];
  for (let i = 0; i < 120; i++) {
    confettiPieces.push({
      x: Math.random() * confettiCanvas.width,
      y: -20,
      w: Math.random() * 10 + 5,
      h: Math.random() * 6 + 3,
      color: colors[Math.floor(Math.random() * colors.length)],
      rot: Math.random() * 360,
      vx: (Math.random() - 0.5) * 4,
      vy: Math.random() * 4 + 2,
      vr: (Math.random() - 0.5) * 6,
      alpha: 1,
    });
  }
  animateConfetti();
}

function animateConfetti() {
  if (!ctx) return;
  ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
  confettiPieces = confettiPieces.filter(p => p.alpha > 0.05);
  confettiPieces.forEach(p => {
    p.x += p.vx; p.y += p.vy; p.rot += p.vr;
    if (p.y > confettiCanvas.height * 0.7) p.alpha -= 0.02;
    ctx.save();
    ctx.globalAlpha = p.alpha;
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot * Math.PI / 180);
    ctx.fillStyle = p.color;
    ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
    ctx.restore();
  });
  if (confettiPieces.length > 0) requestAnimationFrame(animateConfetti);
  else ctx.clearRect(0, 0, confettiCanvas.width, confettiCanvas.height);
}

window.launchConfetti = launchConfetti;

// ── Smooth scroll for anchor links ──
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      document.querySelector(a.getAttribute('href'))?.scrollIntoView({ behavior: 'smooth' });
    });
  });
});
