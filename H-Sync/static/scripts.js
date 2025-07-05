document.addEventListener('DOMContentLoaded', () => {
  // Debug: to check and ensure script runs and canvas works as intended
  console.log('DOMContentLoaded fired');
  const canvas = document.getElementById('particle-canvas');
  console.log('canvas is', canvas);
  if (!canvas) {
    console.error('particle-canvas element not found');
    return;
  }
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    console.error('2D context unavailable');
    return;
  }
  console.log('canvas and context are ready');

  // Particle background engine
  let width, height;
  let particles = [];
  let angle = 0;

  function initParticles() {
    width  = canvas.width  = window.innerWidth;
    height = canvas.height = window.innerHeight;
    particles = [];
    for (let i = 0; i < 100; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 1.5 + 0.5,
        d: Math.random() * 50
      });
    }
  }

  function drawParticles() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = 'rgba(255,255,255,0.8)';
    for (const p of particles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function updateParticles() {
    angle = angle + 0.01;
    for (const p of particles) {
      p.y += Math.cos(angle + p.d) + 0.5; 
      p.x += Math.sin(angle) * 0.5;
      if (p.y > height + 5) {
        p.y = -5;
        p.x = Math.random() * width;
      }
      if (p.x > width + 5) p.x = -5;
      else if (p.x < -5) p.x = width + 5;
    }
  }

  function animate() {
    drawParticles();
    updateParticles();
    requestAnimationFrame(animate);
  }

  // Initialize and start
  window.addEventListener('resize', initParticles);
  initParticles();
  animate();
});

function sendAction(deviceName, action) {
    fetch(`/api/device/${encodeURIComponent(deviceName)}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ action: action })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status) {
            updateStatus(data.status);
        }
        else {
            alert("Error: " + (data.error || "Unknown error"));
        }
    })
    .catch(err => alert("Request failed: " + err));
}


function playMedia(event, deviceName) {
    event.preventDefault();
    const url = event.target.querySelector('input[name="url"]').value;
    fetch(`/api/device/${encodeURIComponent(deviceName)}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ action: "play_media", url })
    })
    .then(res => res.json())
    .then(data => data.status ? updateStatus(data.status) : alert("Error: "+(data.error)))
    .catch(err => alert("Request Failed: "+err));
}


function setVolume(deviceName) {
    const lvl = parseFloat(document.getElementById(`vol-${deviceName}`).value);
    if (isNaN(lvl)) return alert("Enter a Valid Number");
    fetch(`/api/device/${encodeURIComponent(deviceName)}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ action: "set_volume", level: lvl })
    })
    .then(res => res.json())
    .then(data => data.status ? updateStatus(data.status) : alert("Error: "+(data.error||"Unknown")))
    .catch(err => alert("Request Failed: "+err));
}


function playback(deviceName, cmd) {
    fetch(`/api/device/${encodeURIComponent(deviceName)}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ action: "playback", cmd: cmd })
    })
    .then(res => res.json())
    .then(data => data.status ? updateStatus(data.status) : alert("Error: "+(data.error||"Unknown")))
    .catch(err => alert("Request Failed: "+err));
}


function seek(event, deviceName) {
    event.preventDefault();
    const secs = parseFloat(event.target.querySelector('input[name = "seconds"]').value);
    playback(deviceName, `seek:${secs}`);
}

function updateStatus(status) {
    const statusEl = document.getElementById("status-json");
    if (!statusEl) return;   // nothing to update on this page
    statusEl.textContent = JSON.stringify(status, null, 2);
}


function playYouTubeSearch(event, deviceName) {
  event.preventDefault();
  const q = event.target.query.value;
  fetch(`/api/device/${encodeURIComponent(deviceName)}/action`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ action: "play_youtube", query: q })
  })
  .then(r => r.json())
  .then(d => d.status ? updateStatus(d.status) : alert(d.error))
  .catch(e => alert("Error: "+e));
}

document.addEventListener('DOMContentLoaded', () => {
  const anim = lottie.loadAnimation({
    container: document.getElementById('wifi-icon'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/static/animations/wifi.json'
  });
  anim.setSpeed(0.35); // play at 35% speed
  
});

function initSSE() {
  console.log("DOM ready, opening SSE", deviceName);
  const es = new EventSource(`/device/${encodeURIComponent(deviceName)}/events`);

  es.onopen    = () => console.log("SSE connection open");
  es.onmessage = e => showPopup(`Double‑clap detected on ${e.data}!`, 2500);
  es.onerror   = err => {
    console.error("SSE error, reconnecting in 3s", err);
    es.close();
    setTimeout(initSSE, 3000);
  };
}

document.addEventListener('DOMContentLoaded', initSSE);

function showPopup(msg, delay = 3000) {
  const popup = document.createElement('div');
  popup.textContent = msg;
  popup.setAttribute('role', 'status');
  popup.setAttribute('aria-live', 'polite');

  Object.assign(popup.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    background: 'var(--color-muted)',
    color: 'var(--color-text)',
    padding: '1rem 1.5rem',
    borderRadius: '0.5rem',
    fontSize: '2rem',
    zIndex: 10000,
    opacity: '0',
    transition: 'opacity 0.3s ease'
  });

  document.body.appendChild(popup);

  requestAnimationFrame(() => {
    popup.style.opacity = '1';
  });

  setTimeout(() => {
    popup.style.opacity = '0';
    popup.addEventListener('transitionend', () => popup.remove(), { once: true });
  }, delay);
}

//speakers.html
async function castStation({ url, name }) {
        console.log("casting", url, "to", deviceName);
        try {
            const res = await fetch(
            `/api/device/${encodeURIComponent(deviceName)}/action`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "play_media", url })
            }
            );
            const data = await res.json();
            if (data.status) {
            showPopup(`Now playing "${name}" on ${deviceName}`, 2500);
            } else {
            alert("Error: " + (data.error || "Unknown"));
            }
        } catch (err) {
            alert("Request failed: " + err);
        }
        }
