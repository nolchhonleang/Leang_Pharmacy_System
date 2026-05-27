document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  const toggle = document.getElementById('sidebarToggle');
  const topbar = document.querySelector('.app-topbar');

  function closeSidebar() {
    sidebar?.classList.remove('show');
    backdrop?.classList.remove('show');
    document.body.style.overflow = '';
  }

  function openSidebar() {
    sidebar?.classList.add('show');
    backdrop?.classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  toggle?.addEventListener('click', () => {
    if (sidebar?.classList.contains('show')) closeSidebar();
    else openSidebar();
  });

  backdrop?.addEventListener('click', closeSidebar);

  window.addEventListener('resize', () => {
    if (window.innerWidth >= 992) closeSidebar();
  });

  document.querySelectorAll('.app-sidebar .nav-link').forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 992) closeSidebar();
    });
  });

  if (topbar) {
    const onScroll = () => {
      topbar.classList.toggle('scrolled', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  document.querySelectorAll('.alert-dismissible[data-auto-dismiss]').forEach((el) => {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(el);
      alert?.close();
    }, 5000);
  });

  const revealEls = document.querySelectorAll('.panel, .page-header');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach((el) => {
      el.classList.add('reveal');
      io.observe(el);
    });
  }

  const rxLines = document.getElementById('rxLines');
  const addRxLine = document.getElementById('addRxLine');
  if (rxLines && addRxLine) {
    addRxLine.addEventListener('click', () => {
      const first = rxLines.querySelector('.rx-line');
      if (!first) return;
      const clone = first.cloneNode(true);
      clone.style.animation = 'fadeInUp 0.3s ease both';
      clone.querySelectorAll('input').forEach((i) => {
        if (i.type === 'number') i.value = '1';
      });
      rxLines.appendChild(clone);
    });
    rxLines.addEventListener('click', (e) => {
      const btn = e.target.closest('.remove-line');
      if (!btn) return;
      const lines = rxLines.querySelectorAll('.rx-line');
      if (lines.length > 1) btn.closest('.rx-line')?.remove();
    });
  }
});
