(() => {
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Critically-damped-by-default spring, driven by Apple's damping/response params
     rather than raw stiffness. Retargeting mid-flight keeps current value + velocity,
     so it never resets to zero — that's what makes it feel interruptible. */
  class Spring {
    constructor(value, { damping = 1, response = 0.3 } = {}) {
      this.value = value;
      this.velocity = 0;
      this.target = value;
      this.setParams(damping, response);
      this._raf = null;
      this.onUpdate = null;
    }
    setParams(damping, response) {
      const angFreq = (2 * Math.PI) / response;
      this.stiffness = angFreq * angFreq;
      this.damping = 4 * Math.PI * damping / response;
    }
    set(target) {
      this.target = target;
      if (reduceMotion) {
        this.value = target;
        this.velocity = 0;
        this.onUpdate && this.onUpdate(this.value);
        return;
      }
      if (!this._raf) this._tick();
    }
    jump(value) {
      this.value = value;
      this.target = value;
      this.velocity = 0;
      this.onUpdate && this.onUpdate(this.value);
    }
    _tick() {
      let last = performance.now();
      const step = (now) => {
        const dt = Math.min((now - last) / 1000, 1 / 30);
        last = now;
        const springForce = -this.stiffness * (this.value - this.target);
        const dampingForce = -this.damping * this.velocity;
        this.velocity += (springForce + dampingForce) * dt;
        this.value += this.velocity * dt;
        this.onUpdate && this.onUpdate(this.value);
        if (Math.abs(this.value - this.target) < 0.01 && Math.abs(this.velocity) < 0.01) {
          this.value = this.target;
          this.velocity = 0;
          this.onUpdate && this.onUpdate(this.value);
          this._raf = null;
          return;
        }
        this._raf = requestAnimationFrame(step);
      };
      this._raf = requestAnimationFrame(step);
    }
  }
  window.WMSpring = Spring;

  /* ---- Top bar scroll state ---- */
  const topbar = document.getElementById('topbar');
  if (topbar) {
    const onScroll = () => topbar.classList.toggle('scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Glass nav panel: a "drawer" (damping 0.8, response 0.3) sliding in from the left ---- */
  const trigger = document.getElementById('menu-trigger');
  const panel = document.getElementById('glass-panel');
  const scrim = document.getElementById('glass-scrim');
  const closeBtn = document.getElementById('glass-close');
  if (trigger && panel && scrim) {
    let open = false;
    const xSpring = new Spring(-105, { damping: 0.8, response: 0.3 });
    xSpring.onUpdate = (v) => { panel.style.transform = `translateX(${v}%)`; };
    function setPanel(next) {
      open = next;
      scrim.classList.toggle('is-open', open);
      document.body.classList.toggle('panel-open', open);
      trigger.setAttribute('aria-expanded', String(open));
      xSpring.set(open ? 0 : -105);
    }
    trigger.addEventListener('click', () => setPanel(!open));
    scrim.addEventListener('click', () => setPanel(false));
    closeBtn && closeBtn.addEventListener('click', () => setPanel(false));
    panel.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setPanel(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && open) setPanel(false); });
  }

  /* ---- Scroll reveal ---- */
  function initReveal() {
    const revealEls = document.querySelectorAll('.reveal:not(.is-visible)');
    if ('IntersectionObserver' in window && !reduceMotion) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
      revealEls.forEach(el => io.observe(el));
    } else {
      revealEls.forEach(el => el.classList.add('is-visible'));
    }
  }
  window.WMInitReveal = initReveal;
  document.addEventListener('DOMContentLoaded', initReveal);
})();
