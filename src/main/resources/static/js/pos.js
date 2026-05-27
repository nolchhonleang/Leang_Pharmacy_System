(function () {
  const searchInput = document.getElementById('posSearch');
  const resultsEl = document.getElementById('posResults');
  const cartBody = document.getElementById('cartBody');
  const cartEmpty = document.getElementById('cartEmpty');
  const subtotalEl = document.getElementById('cartSubtotal');
  const form = document.getElementById('posForm');
  if (!searchInput || !form) return;

  const cart = new Map();
  let debounceTimer;

  function money(n) {
    return '$' + Number(n).toFixed(2);
  }

  function renderCart() {
    cartBody.innerHTML = '';
    let subtotal = 0;
    if (cart.size === 0) {
      cartEmpty.style.display = 'block';
    } else {
      cartEmpty.style.display = 'none';
      cart.forEach((item) => {
        subtotal += item.price * item.qty;
        const tr = document.createElement('tr');
        tr.style.animation = 'fadeInUp 0.25s ease both';
        tr.innerHTML = `
          <td class="fw-semibold">${item.name}${item.rx ? ' <span class="badge badge-pill badge-rx">Rx</span>' : ''}</td>
          <td class="text-end">${money(item.price)}</td>
          <td class="text-center" style="width:90px">
            <input type="number" min="1" max="${item.max}" value="${item.qty}" class="form-control form-control-sm text-center cart-qty" data-id="${item.id}"/>
          </td>
          <td class="text-end">${money(item.price * item.qty)}</td>
          <td><button type="button" class="btn btn-sm btn-outline-danger cart-remove" data-id="${item.id}"><i class="bi bi-x"></i></button></td>
          <input type="hidden" name="medicineId" value="${item.id}"/>
          <input type="hidden" name="quantity" value="${item.qty}" class="cart-qty-hidden" data-id="${item.id}"/>`;
        cartBody.appendChild(tr);
      });
    }
    subtotalEl.textContent = money(subtotal);
  }

  function addToCart(m) {
    const existing = cart.get(m.id);
    const qty = existing ? existing.qty + 1 : 1;
    if (qty > m.available) {
      alert('Only ' + m.available + ' in stock');
      return;
    }
    cart.set(m.id, {
      id: m.id,
      name: m.name,
      price: Number(m.unitPrice),
      qty,
      max: m.available,
      rx: m.requiresPrescription,
    });
    renderCart();
  }

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = searchInput.value.trim();
    if (q.length < 1) {
      resultsEl.innerHTML = '<p class="text-muted small mb-0">Type to search medicines…</p>';
      return;
    }
    debounceTimer = setTimeout(async () => {
      resultsEl.innerHTML = '<p class="text-muted small mb-0"><span class="spinner-border spinner-border-sm"></span> Searching…</p>';
      try {
        const res = await fetch('/api/v1/pos/search?q=' + encodeURIComponent(q) + '&limit=15');
        const items = await res.json();
        if (!items.length) {
          resultsEl.innerHTML = '<p class="text-muted small mb-0">No matches</p>';
          return;
        }
        resultsEl.innerHTML = '';
        items.forEach((m, i) => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'list-group-item list-group-item-action d-flex justify-content-between align-items-center pos-search-hit';
          btn.style.animationDelay = `${Math.min(i, 8) * 0.03}s`;
          btn.innerHTML = `<span><code class="me-2">${m.sku}</code>${m.name}</span>
            <span><span class="badge ${m.available <= 5 ? 'badge-stock-low' : 'badge-stock-ok'} me-2">${m.available}</span>${money(m.unitPrice)}</span>`;
          btn.addEventListener('click', () => addToCart(m));
          resultsEl.appendChild(btn);
        });
      } catch {
        resultsEl.innerHTML = '<p class="text-danger small mb-0">Search failed</p>';
      }
    }, 200);
  });

  resultsEl.addEventListener('click', (e) => e.preventDefault());

  cartBody.addEventListener('click', (e) => {
    const rm = e.target.closest('.cart-remove');
    if (rm) {
      cart.delete(Number(rm.dataset.id));
      renderCart();
    }
  });

  cartBody.addEventListener('change', (e) => {
    if (!e.target.classList.contains('cart-qty')) return;
    const id = Number(e.target.dataset.id);
    const item = cart.get(id);
    let qty = parseInt(e.target.value, 10);
    if (qty < 1) qty = 1;
    if (qty > item.max) qty = item.max;
    item.qty = qty;
    cart.set(id, item);
    renderCart();
  });

  form.addEventListener('submit', (e) => {
    if (cart.size === 0) {
      e.preventDefault();
      alert('Add at least one item to the cart');
    }
  });

  resultsEl.innerHTML = '<p class="text-muted small mb-0">Type to search medicines…</p>';
})();
