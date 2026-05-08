// Nav scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// Mobile hamburger
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
hamburger.addEventListener('click', () => {
  mobileMenu.classList.toggle('open');
});
document.querySelectorAll('.nav__mobile a').forEach(link => {
  link.addEventListener('click', () => mobileMenu.classList.remove('open'));
});

// Smooth scroll for all anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// Fade-in on scroll
const observer = new IntersectionObserver(
  entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  }),
  { threshold: 0.12 }
);

document.querySelectorAll(
  '.pillar__overview, .pillar__text, .pillar__visual, .pf__item, .cta__box'
).forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

// CTA form submission
document.getElementById('ctaForm').addEventListener('submit', e => {
  e.preventDefault();
  const input = e.target.querySelector('input[type="email"]');
  const btn   = e.target.querySelector('button');
  btn.textContent  = 'You\'re on the list ✓';
  btn.style.background = '#16a34a';
  btn.disabled = true;
  input.disabled   = true;
  input.value      = '';
});

// Animate progress bars when visible
const barObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.vc__fill').forEach(bar => {
        const target = bar.style.width;
        bar.style.width = '0';
        requestAnimationFrame(() => {
          bar.style.transition = 'width 1.2s cubic-bezier(0.4,0,0.2,1)';
          bar.style.width = target;
        });
      });
      barObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.3 });

document.querySelectorAll('.visual__card').forEach(card => barObserver.observe(card));

// Typing animation for terminal
const terminalLines = [
  { prompt: true,  text: 'run wallet-tracker.py' },
  { prompt: false, text: '✓ Tracking 12 wallets...', cls: 't__out' },
  { prompt: true,  text: 'run signal-agg.js' },
  { prompt: false, text: '✓ 7 signals aggregated', cls: 't__out' },
  { prompt: true,  text: 'run discord-bot.ts' },
  { prompt: false, text: '✓ Bot online in #alpha', cls: 't__out' },
];

const terminal = document.getElementById('terminal');
if (terminal) {
  const terminalObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        terminal.innerHTML = '';
        let delay = 0;
        terminalLines.forEach(line => {
          delay += 480;
          setTimeout(() => {
            const div = document.createElement('div');
            div.className = 't__line' + (line.cls ? ` ${line.cls}` : '');
            if (line.prompt) {
              div.innerHTML = `<span class="t__prompt">$</span> ${line.text}`;
            } else {
              div.textContent = line.text;
            }
            terminal.appendChild(div);
          }, delay);
        });
        // cursor
        setTimeout(() => {
          const cur = document.createElement('div');
          cur.className = 't__line t__cursor';
          cur.innerHTML = '<span class="t__prompt">$</span> <span class="blink">_</span>';
          terminal.appendChild(cur);
        }, delay + 500);
        terminalObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  terminalObserver.observe(terminal);
}
