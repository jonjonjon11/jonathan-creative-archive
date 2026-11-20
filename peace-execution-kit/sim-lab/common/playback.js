export function createPlayback(initial = 1) {
  let speed = initial;
  let paused = false;
  let t = 0;
  let lastTs = performance.now();

  return {
    get speed() { return speed; },
    get paused() { return paused; },
    get time() { return t; },
    setSpeed(v) { speed = Number(v) || 0; },
    togglePause() { paused = !paused; },
    reset() {
      t = 0;
      paused = false;
      lastTs = performance.now();
    },
    tick() {
      const now = performance.now();
      const dt = (now - lastTs) / 1000;
      lastTs = now;
      if (!paused) t += dt * speed;
      return { dt, t };
    }
  };
}

