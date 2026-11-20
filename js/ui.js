// Small shared helpers for building screens.

export function esc(value) {
  return String(value ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

let toastTimer;
export function toast(message, action) {
  const el = document.getElementById('toast');
  el.innerHTML = `<span>${esc(message)}</span>`;
  if (action) {
    const b = document.createElement('button');
    b.textContent = action.label;
    b.addEventListener('click', () => { el.hidden = true; action.run(); });
    el.appendChild(b);
  }
  el.hidden = false;
  clearTimeout(toastTimer);
  if (!action) toastTimer = setTimeout(() => { el.hidden = true; }, 2200);
}

export function checkChip(verified) {
  return verified
    ? '<span class="chip ok">✓ Verified</span>'
    : '<span class="chip nc">Needs check</span>';
}

export function firstPhoto(content, speciesId, role = 'leaf') {
  const list = content.photos[speciesId] || [];
  return list.find((p) => p.role === role) || list[0];
}

// Shown on the Progress screen. Keep in step with VERSION in sw.js.
export const APP_VERSION = '0.3.0';
