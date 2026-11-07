/* Original interface for Motion → Trace → Shape. CC BY 4.0. */
(function () {
  'use strict';
  const M = window.MotionModel;
  const $ = id => document.getElementById(id);
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  let params = { ...M.PRESETS.circle };
  let samples = M.sample(params);
  let time = 0;
  let running = false;
  let frame = null;
  let lastFrame = null;
  $('still').checked = media.matches;
  const set = (id, attr, value) => $(id).setAttribute(attr, String(value));
  const fixed = n => Math.abs(n) < 0.0005 ? '0.000' : n.toFixed(3);
  const pointPath = (points, x, y) => points.map((p, i) => `${i ? 'L' : 'M'}${x(p).toFixed(3)} ${y(p).toFixed(3)}`).join(' ');
  const diamond = (x, y, r) => `M${x} ${y-r}l${r} ${r} -${r} ${r} -${r} -${r}Z`;
  const px = p => 210 + 160 * p.x;
  const py = p => 210 - 160 * p.y;
  const tx = p => 58 + 512 * p.t / M.DURATION;
  const tyX = p => 60 - 28 * p.x;
  const tyY = p => 140 - 28 * p.y;
  function shapeLabel() {
    const phase = params.phase % 360;
    if (params.xCycles === params.yCycles) {
      if (phase === 0 || phase === 180) return 'Line';
      if (phase === 90 || phase === 270) return 'Circle';
      return 'Ellipse';
    }
    if (params.yCycles === params.xCycles * 2 && (phase === 0 || phase === 180)) return 'Figure-eight';
    return 'Lissajous pattern';
  }
  function summary() {
    const s = M.stateAt(params, time);
    return `At ${fixed(time)} model seconds: left-right position ${fixed(s.x)}; up-down position ${fixed(s.y)} model units. ${shapeLabel()}. Left-right repeats ${params.xCycles} times and up-down repeats ${params.yCycles} times in 8 seconds, with a ${params.phase}-degree up-down head start.`;
  }
  function announce(message) { $('announcement').textContent = message; }
  function updateButtons() {
    $('play').disabled = $('still').checked;
    $('play').textContent = running ? 'Pause' : time >= M.DURATION ? 'Replay one cycle' : 'Play one cycle';
    $('step').disabled = time >= M.DURATION;
    $('motionNotice').textContent = $('still').checked ? 'Still mode is on. Step and the time slider remain available.' : 'Still mode turns off continuous playback.';
  }
  function pause(message) {
    running = false;
    if (frame !== null) window.cancelAnimationFrame(frame);
    frame = null;
    lastFrame = null;
    updateButtons();
    if (message) announce(message);
  }
  function redrawGuide() {
    set('shapeGuide', 'd', pointPath(samples, px, py));
    set('xGuide', 'd', pointPath(samples, tx, tyX));
    set('yGuide', 'd', pointPath(samples, tx, tyY));
  }
  function render() {
    const s = M.stateAt(params, time);
    const history = M.historyUntil(samples, time);
    set('shapeTrace', 'd', pointPath(history, px, py));
    set('xTrace', 'd', pointPath(history, tx, tyX));
    set('yTrace', 'd', pointPath(history, tx, tyY));
    for (const id of ['shapeGuide', 'xGuide', 'yGuide']) set(id, 'visibility', $('guide').checked ? 'visible' : 'hidden');
    set('shapeDot', 'cx', px(s)); set('shapeDot', 'cy', py(s));
    set('projection', 'd', `M${px(s)} 370V${py(s)}H50`);
    set('xDot', 'cx', 123 + 95 * s.x);
    set('yDot', 'd', diamond(280, 82 - 50 * s.y, 8));
    set('timeCursor', 'd', `M${tx(s)} 25V175`);
    set('xTimeDot', 'cx', tx(s)); set('xTimeDot', 'cy', tyX(s));
    set('yTimeDot', 'd', diamond(tx(s), tyY(s), 5));
    $('time').value = time;
    $('timeValue').textContent = `${fixed(time)} / 8 s`;
    set('time', 'aria-valuetext', `${fixed(time)} of 8 model seconds`);
    $('xRead').textContent = fixed(s.x); $('yRead').textContent = fixed(s.y);
    $('shapeName').textContent = shapeLabel();
    $('textSummary').textContent = summary();
    $('shapeDesc').textContent = `${summary()} Solid gold ink joins ${history.length} sampled positions so far. ${$('guide').checked ? 'The dashed line previews the complete shape.' : 'The complete guide is hidden.'}`;
    updateButtons();
  }
  function syncParams() {
    for (const key of ['xCycles', 'yCycles', 'phase']) $(key).value = params[key];
    $('xValue').textContent = params.xCycles;
    $('yValue').textContent = params.yCycles;
    const phases = { 0: '0 cycles', 90: '¼ cycle', 180: '½ cycle', 270: '¾ cycle', 360: '1 cycle' };
    $('phaseValue').textContent = phases[params.phase] || `${params.phase}°`;
    set('phase', 'aria-valuetext', `${params.phase} degrees, ${params.phase / 360} of the up-down cycle`);
    for (const [name, preset] of Object.entries(M.PRESETS)) {
      set('preset-' + name, 'aria-pressed', Object.keys(preset).every(key => params[key] === preset[key]));
    }
  }
  function changeModel(next) {
    params = M.validate(next);
    pause();
    time = 0;
    samples = M.sample(params);
    syncParams(); redrawGuide(); render();
    $('exportStatus').textContent = '';
    announce('New experiment, paused at time zero. ' + summary());
  }
  function tick(now) {
    if (!running) return;
    if (lastFrame !== null) time = M.advance(time, Math.max(0, (now - lastFrame) / 1000), Number($('speed').value));
    lastFrame = now;
    render();
    if (time >= M.DURATION) pause('Cycle complete. ' + summary());
    else frame = window.requestAnimationFrame(tick);
  }
  $('play').addEventListener('click', () => {
    if (running) { pause('Paused. ' + summary()); return; }
    if ($('still').checked) return;
    if (time >= M.DURATION) time = 0;
    running = true; lastFrame = null;
    render(); announce('Playing one 8-model-second window. Use Pause at any time.');
    frame = window.requestAnimationFrame(tick);
  });
  $('step').addEventListener('click', () => {
    pause(); time = Math.min(M.DURATION, time + 0.125); render(); announce(summary());
  });
  $('restart').addEventListener('click', () => {
    pause(); time = 0; render(); announce('Restarted and paused. ' + summary());
  });
  $('time').addEventListener('input', () => {
    pause(); time = Math.max(0, Math.min(M.DURATION, Number($('time').value))); render();
  });
  $('time').addEventListener('change', () => announce(summary()));
  for (const key of ['xCycles', 'yCycles', 'phase']) $(key).addEventListener('input', () => {
    changeModel({ ...params, [key]: Number($(key).value) });
  });
  for (const [name, preset] of Object.entries(M.PRESETS)) $('preset-' + name).addEventListener('click', () => changeModel(preset));
  $('guide').addEventListener('change', () => { render(); announce($('guide').checked ? 'Complete guide shown. This does not change the model.' : 'Complete guide hidden. This does not change the model.'); });
  $('still').addEventListener('change', () => {
    if ($('still').checked) pause();
    render(); announce($('still').checked ? 'Still mode on. Use Step or the time slider.' : 'Still mode off. Playback stays paused until you choose Play.');
  });
  $('speed').addEventListener('change', () => {
    // Avoid applying a new speed retroactively to elapsed time before the change.
    lastFrame = null;
    announce(`Playback speed ${$('speed').value} times. Equations and sample data are unchanged.`);
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && running) pause('Paused because the page was hidden.');
  });
  media.addEventListener('change', event => {
    if (event.matches) {
      $('still').checked = true; pause(); render();
      announce('Your device requested reduced motion. Still mode is now on.');
    }
  });
  $('export').addEventListener('click', () => {
    pause();
    try {
      const record = M.record(params, { time, playbackSpeed: Number($('speed').value), showGuide: $('guide').checked, stillMode: $('still').checked });
      const blob = new Blob([JSON.stringify(record, null, 2) + '\n'], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url; link.download = 'motion-trace-shape-experiment.json';
      document.body.appendChild(link); link.click(); link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 10000);
      $('exportStatus').textContent = 'Experiment download requested. Check your browser’s downloads; nothing was uploaded.';
    } catch (error) {
      $('exportStatus').textContent = 'Your browser could not start the download. The experiment is still available here. Try opening the HTML in a full browser.';
    }
  });
  syncParams(); redrawGuide(); render();
}());
