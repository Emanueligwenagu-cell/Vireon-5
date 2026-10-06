const PAGE_URLS = {
  home: 'home.html', browse: 'browse.html', cart: 'cart.html', orders: 'orders.html',
  vendor: 'vendor.html', game: 'game.html', login: 'login.html'
};

async function api(url, options = {}) {
  const opts = { ...options, headers: { 'Content-Type': 'application/json', ...(options.headers || {}) } };
  const res = await fetch(url, opts);
  let data = {};
  try { data = await res.json(); } catch (_) { }
  if (!res.ok) throw new Error(data.detail || 'Request failed');
  return data;
}

async function loadSession() {
  try {
    const data = await api('/api/auth/me');
    state.user = data.user;
    if (state.user.role === 'vendor') {
      const orders = await api('/api/vendor/orders');
      state.orders = orders.orders || [];
      state.vendorMenuItems = ((await api('/api/vendor/menu')).items || []).map(p => ({
        ...p, desc: p.description || '', cat: p.category, img: p.image, vid: p.vendor_id
      }));
      state.vendorOpen = (await api('/api/vendor')).vendor?.is_open ?? true;
    } else {
      const orders = await api('/api/orders');
      state.orders = orders.orders || [];
    }
  } catch (_) {
    state.user = null;
  }
}

/* ═══════════════════════════════════════
   ROLE-BASED ACCESS
   Vendors may only use the vendor page (accept/cancel orders etc).
   Students may do everything except the vendor page.
═══════════════════════════════════════ */
function isVendorOnlyPage(page) { return page === 'vendor'; }
function homePageFor(role) { return role === 'vendor' ? 'vendor.html' : 'home.html'; }

function enforceRoleAccess() {
  if (!state.user) {
    window.location.replace('login.html');
    return false;
  }
  const page = state.currentPage;
  if (state.user.role === 'vendor' && !isVendorOnlyPage(page)) {
    window.location.replace('vendor.html');
    return false;
  }
  if (state.user.role !== 'vendor' && isVendorOnlyPage(page)) {
    window.location.replace('home.html');
    return false;
  }
  return true;
}

function applyRoleNav() {
  if (!state.user) return;
  const isVendor = state.user.role === 'vendor';
  document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(el => {
    const target = el.dataset.page || (el.getAttribute('href') || '').replace('.html', '');
    if (!target) return;
    const vendorLink = target === 'vendor';
    el.style.display = isVendor ? (vendorLink ? '' : 'none') : (vendorLink ? 'none' : '');
  });
  const cartBtn = document.querySelector('.cart-btn');
  if (cartBtn) cartBtn.style.display = isVendor ? 'none' : '';
}

async function pollVendorOrders() {
  if (state.user?.role !== 'vendor') return;
  try {
    const { orders } = await api('/api/vendor/orders');
    state.orders = orders || [];
    if (state.currentPage === 'vendor') refreshVendor();
    updateNavCart();
  } catch (_) { }
}

function navigate(page) {
  if (PAGE_URLS[page]) window.location.href = PAGE_URLS[page];
}
function goBrowseCat(cat) { state.activeCategory = cat; sessionStorage.setItem('ibhotwe_category', cat); navigate('browse'); }
function requireAuth() {
  if (!state.user) { window.location.replace('login.html'); return false; }
  return true;
}
function updateNavCart() {
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  const cnt = cartCount();
  badge.style.display = cnt > 0 ? 'flex' : 'none';
  badge.textContent = cnt;
}
function updateProfileUI() {
  const btn = document.getElementById('profile-btn');
  const name = document.getElementById('dd-name'), email = document.getElementById('dd-email'), pts = document.getElementById('dd-pts');
  if (state.user) {
    if (btn) btn.textContent = state.user.name[0].toUpperCase();
    if (name) name.textContent = state.user.name;
    if (email) email.textContent = state.user.email;
    if (pts) {
      pts.textContent = state.user.role === 'vendor' ? '👨‍🍳 Vendor Account' : `⭐ ${state.user.loyalty_points || 0} loyalty points`;
    }
  }
}
async function boot() {
  if (state.currentPage !== 'login') {
    await loadSession();
    if (!requireAuth()) return;
    if (!enforceRoleAccess()) return;
  } else {
    state.user = null;
    localStorage.removeItem('ibhotwe_cart');
    sessionStorage.clear();
  }
  const cat = sessionStorage.getItem('ibhotwe_category');
  if (cat && state.currentPage === 'browse') { state.activeCategory = cat; sessionStorage.removeItem('ibhotwe_category'); }
  if (state.currentPage === 'home') { document.getElementById('home-page').innerHTML = renderHome(); bindHome(); }
  if (state.currentPage === 'browse') { document.getElementById('browse-page').innerHTML = renderBrowse(); bindBrowse(); }
  if (state.currentPage === 'cart') { document.getElementById('cart-page').innerHTML = renderCart(); bindCart(); }
  if (state.currentPage === 'orders') { document.getElementById('orders-page').innerHTML = renderOrders(); bindOrders(); }
  if (state.currentPage === 'vendor') { document.getElementById('vendor-page').innerHTML = renderVendor(); bindVendor(); }
  if (state.currentPage === 'game') { document.getElementById('game-page').innerHTML = renderGame(); bindGame(); }
  if (state.currentPage === 'login') { document.getElementById('login-page').innerHTML = renderLogin(); bindLogin(); }
  updateNavCart(); updateProfileUI(); applyRoleNav();
  if (state.currentPage === 'vendor' && state.user?.role === 'vendor') {
    setInterval(pollVendorOrders, 5000);
  }
}
document.addEventListener('DOMContentLoaded', boot);
