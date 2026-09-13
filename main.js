// Mobile nav
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');

menuToggle.addEventListener('click', () => {
  const open = mobileMenu.classList.toggle('open');
  mobileMenu.setAttribute('aria-hidden', String(!open));
  menuToggle.setAttribute('aria-expanded', String(open));
});

mobileMenu.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    mobileMenu.classList.remove('open');
    mobileMenu.setAttribute('aria-hidden', 'true');
    menuToggle.setAttribute('aria-expanded', 'false');
  });
});

// Form
document.getElementById('contactForm').addEventListener('submit', function (e) {
  e.preventDefault();
  const btn = this.querySelector('button[type="submit"]');
  btn.textContent = 'Sending…';
  btn.disabled = true;

  // Replace with Formspree, EmailJS, or your own endpoint
  setTimeout(() => {
    btn.textContent = 'Request sent — we\'ll be in touch shortly.';
    btn.style.cssText = 'background:#10b981;border-color:#10b981;color:#fff;';
    this.querySelectorAll('input, select, textarea').forEach(el => el.value = '');
  }, 1200);
});
