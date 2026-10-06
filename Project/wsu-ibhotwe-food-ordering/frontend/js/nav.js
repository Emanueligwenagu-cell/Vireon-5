function toggleMobileMenu() {
  document.getElementById('mobile-menu').classList.toggle('open');
}
function closeMobileMenu() {
  document.getElementById('mobile-menu').classList.remove('open');
}
function toggleProfileDropdown() {
  const dd = document.getElementById('profile-dropdown');
  dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
}
function closeDropdown() {
  const dd = document.getElementById('profile-dropdown');
  if (dd) dd.style.display = 'none';
}

function refreshCurrentPage() {
  const page = state.currentPage;
  const el = document.getElementById(page + '-page');
  if (!el) return;
  if (page === 'home') { el.innerHTML = renderHome(); bindHome(); }
  else if (page === 'browse') { el.innerHTML = renderBrowse(); bindBrowse(); }
  else if (page === 'cart') { el.innerHTML = renderCart(); bindCart(); }
  else if (page === 'orders') { el.innerHTML = renderOrders(); bindOrders(); }
  else if (page === 'vendor') { el.innerHTML = renderVendor(); bindVendor(); }
  else if (page === 'game') { el.innerHTML = renderGame(); bindGame(); }
  else if (page === 'login') { el.innerHTML = renderLogin(); bindLogin(); }
  updateNavCart();
}

/* ═══════════════════════════════════════
   LOGOUT / SIGN OUT
═══════════════════════════════════════ */
async function handleLogout() {
  try {
    if (typeof api === 'function') {
      await api('/api/auth/logout', { method: 'POST' });
    } else {
      await fetch('/api/auth/logout', { method: 'POST' });
    }
  } catch (_) { }
  if (typeof state !== 'undefined') {
    state.user = null;
  }
  localStorage.removeItem('ibhotwe_cart');
  sessionStorage.clear();
  window.location.replace('login.html');
}
window.handleLogout = handleLogout;

/* ═══════════════════════════════════════
   CLICK OUTSIDE – close dropdown
═══════════════════════════════════════ */
document.addEventListener('click', function (e) {
  const wrap = document.querySelector('.profile-wrap');
  if (wrap && !wrap.contains(e.target)) closeDropdown();
});


