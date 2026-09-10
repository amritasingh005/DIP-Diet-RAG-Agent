/**
 * DIP Diet RAG Agent — Global App JavaScript
 * Initialises tooltips, dropdowns, and shared utilities.
 */

document.addEventListener('DOMContentLoaded', function () {

  // ── Bootstrap tooltips ─────────────────────────────────────────────────
  document.querySelectorAll('[title]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover', delay: { show: 600, hide: 100 } });
  });

  // ── Auto-render markdown in agent-content divs ─────────────────────────
  document.querySelectorAll('.agent-content.markdown-body[data-raw]').forEach(el => {
    const raw = el.getAttribute('data-raw');
    if (raw && typeof marked !== 'undefined') {
      el.innerHTML = marked.parse(raw);
      el.removeAttribute('data-raw');
    }
  });

  // ── Flash message auto-dismiss ─────────────────────────────────────────
  document.querySelectorAll('.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });

  // ── Active nav link highlighting ───────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    }
  });
});
