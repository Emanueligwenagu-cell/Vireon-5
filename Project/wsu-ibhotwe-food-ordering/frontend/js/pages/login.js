function renderLogin() {
  const d = state.loginData, r = state.regData;
  const isVendorLogin = state.loginRole === 'vendor';
  const isVendorReg = state.regRole === 'vendor';

  return `<div class="login-outer" style="min-height:calc(100vh - 64px)">
    <div class="login-panel">
      <div class="login-panel-blur1"></div><div class="login-panel-blur2"></div>
      <div class="login-panel-content">
        <div class="login-panel-logo">🍲</div>
        <div class="login-panel-brand">Ibhotwe</div>
        <div class="login-panel-sub">Your campus food companion</div>
        <ul class="login-panel-features">
          ${[['🏫', 'Browse vendors across campus'],
    ['🛒', 'Order with one click'],
    ['📦', 'Track your order in real-time'],
    ['🎁', 'Earn loyalty points on every order'],
    ['👨‍🍳', 'Dedicated vendor portal to manage food and orders'],
    ['🎮', 'Play games while you wait!']].map(f => `<li class="login-panel-feature"><span>${f[0]}</span><span>${f[1]}</span></li>`).join('')}
        </ul>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="login-logo-mobile"><div class="icon">🍲</div><div class="brand">Ibhotwe</div></div>
        
        <div class="auth-tabs">
          <button class="auth-tab${state.loginTab === 'login' ? ' active' : ''}" onclick="setAuthTab('login')">Sign In</button>
          <button class="auth-tab${state.loginTab === 'register' ? ' active' : ''}" onclick="setAuthTab('register')">Register</button>
        </div>

        ${state.authError ? `<div class="auth-error">⚠ ${escHtml(state.authError)}</div>` : ''}

        ${state.loginTab === 'login' ? `
        <!-- Role confirmation question -->
        <div class="role-question-box">
          <div class="role-question-title">Are you signing in as a Student or a Vendor?</div>
          <div class="role-options">
            <div class="role-option ${!isVendorLogin ? 'active' : ''}" onclick="setLoginRole('student')">
              <span class="role-option-icon">🎒</span>
              <div>
                <div class="role-option-title">Student</div>
                <div class="role-option-sub">Order food</div>
              </div>
              ${!isVendorLogin ? '<span class="role-badge">✓</span>' : ''}
            </div>

            <div class="role-option ${isVendorLogin ? 'active' : ''}" onclick="setLoginRole('vendor')">
              <span class="role-option-icon">👨‍🍳</span>
              <div>
                <div class="role-option-title">Vendor</div>
                <div class="role-option-sub">Manage kitchen</div>
              </div>
              ${isVendorLogin ? '<span class="role-badge">✓</span>' : ''}
            </div>
          </div>
        </div>

        <div class="form-group mb-12">
          <label class="label">${isVendorLogin ? 'Vendor Email' : 'Student Email'}</label>
          <div class="input-wrap">
            <span class="icon">✉</span>
            <input class="input has-icon" id="lin-email" type="email" 
                   placeholder="${isVendorLogin ? 'vendor@ibhotwe.co.za' : 'student@ibhotwe.co.za'}" 
                   value="${escHtml(d.email)}"/>
          </div>
        </div>

        <div class="form-group mb-16">
          <label class="label">Password</label>
          <div class="input-wrap">
            <span class="icon">🔒</span>
            <input class="input has-icon has-icon-r" id="lin-pw" 
                   type="${state.showPw ? 'text' : 'password'}" 
                   placeholder="••••••••" 
                   value="${escHtml(d.password)}"/>
            <button class="field-icon-r" onclick="togglePw()">${state.showPw ? '🙈' : '👁'}</button>
          </div>
        </div>

        <button class="btn btn-primary-grad btn-full btn-lg" onclick="doLogin()">
          Sign In as ${isVendorLogin ? 'Vendor' : 'Student'}
        </button>

        <div class="demo-hint" style="margin-top:16px">
          <div><strong>Quick Demo Accounts:</strong></div>
          <div class="demo-buttons">
            <button type="button" class="demo-btn" onclick="quickFillDemo('student')">🎒 Fill Student Demo</button>
            <button type="button" class="demo-btn" onclick="quickFillDemo('vendor')">👨‍🍳 Fill Vendor Demo</button>
          </div>
        </div>
        ` : `
        <!-- Register role selection -->
        <div class="role-question-box">
          <div class="role-question-title">Register as a:</div>
          <div class="role-options">
            <div class="role-option ${!isVendorReg ? 'active' : ''}" onclick="setRegRole('student')">
              <span class="role-option-icon">🎒</span>
              <div>
                <div class="role-option-title">Student</div>
                <div class="role-option-sub">Order & earn points</div>
              </div>
              ${!isVendorReg ? '<span class="role-badge">✓</span>' : ''}
            </div>

            <div class="role-option ${isVendorReg ? 'active' : ''}" onclick="setRegRole('vendor')">
              <span class="role-option-icon">👨‍🍳</span>
              <div>
                <div class="role-option-title">Vendor</div>
                <div class="role-option-sub">Sell food on campus</div>
              </div>
              ${isVendorReg ? '<span class="role-badge">✓</span>' : ''}
            </div>
          </div>
        </div>

        <div class="form-group mb-12">
          <label class="label">${isVendorReg ? 'Owner / Manager Name *' : 'Full Name *'}</label>
          <input class="input" id="reg-name" type="text" placeholder="e.g. Thabo Mokoena" value="${escHtml(r.name)}"/>
        </div>

        <div class="form-group mb-12">
          <label class="label">${isVendorReg ? 'Business / Contact Email *' : 'Student Email *'}</label>
          <input class="input" id="reg-email" type="email" placeholder="name@domain.ac.za" value="${escHtml(r.email)}"/>
        </div>

        <div class="form-row mb-12">
          <div class="form-group">
            <label class="label">${isVendorReg ? 'Vendor / Stall Code' : 'Student Number'}</label>
            <input class="input" id="reg-stnum" placeholder="${isVendorReg ? 'VND-001' : 'STU20240012'}" value="${escHtml(r.studentNumber)}"/>
          </div>
          <div class="form-group">
            <label class="label">Campus</label>
            <select class="select" id="reg-campus">
              ${['Main Campus', 'Science & Engineering', 'Medical Campus', 'Arts & Design', 'Off-Campus Res'].map(c => `<option${r.campus === c ? ' selected' : ''}>${c}</option>`).join('')}
            </select>
          </div>
        </div>

        <div class="form-group mb-16">
          <label class="label">Password *</label>
          <input class="input" id="reg-pw" type="${state.showPw ? 'text' : 'password'}" placeholder="At least 6 characters"/>
        </div>

        <p class="auth-agree">By registering you agree to the terms and campus policy. New student accounts receive 50 loyalty points.</p>
        <button class="btn btn-primary-grad btn-full btn-lg" onclick="doRegister()">
          Create ${isVendorReg ? 'Vendor' : 'Student'} Account
        </button>
        `}
      </div>
    </div>
  </div>`;
}

function bindLogin() {
  document.getElementById('lin-email')?.addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
  document.getElementById('lin-pw')?.addEventListener('keydown', e => { if (e.key === 'Enter') doLogin(); });
  document.getElementById('reg-pw')?.addEventListener('keydown', e => { if (e.key === 'Enter') doRegister(); });
}

function setAuthTab(t) {
  state.loginTab = t;
  state.authError = '';
  refreshLogin();
}

function setLoginRole(role) {
  state.loginRole = role;
  state.authError = '';
  refreshLogin();
}

function setRegRole(role) {
  state.regRole = role;
  state.authError = '';
  refreshLogin();
}

function togglePw() {
  state.showPw = !state.showPw;
  refreshLogin();
}

function quickFillDemo(role) {
  state.loginRole = role;
  if (role === 'vendor') {
    state.loginData = { email: 'vendor@ibhotwe.co.za', password: 'Vendor123!' };
  } else {
    state.loginData = { email: 'student@ibhotwe.co.za', password: 'Student123!' };
  }
  state.authError = '';
  refreshLogin();
}

async function doLogin() {
  const email = document.getElementById('lin-email')?.value.trim() || '';
  const pw = document.getElementById('lin-pw')?.value || '';
  const role = state.loginRole || 'student';

  state.loginData.email = email;
  state.loginData.password = pw;

  if (!email || !pw) {
    state.authError = 'Please fill in both email and password';
    refreshLogin();
    return;
  }

  try {
    const data = await api('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password: pw, role })
    });
    state.user = data.user;
    window.location.href = homePageFor(data.user.role);
  } catch (e) {
    state.authError = e.message;
    refreshLogin();
  }
}

async function doRegister() {
  const name = document.getElementById('reg-name')?.value.trim() || '';
  const email = document.getElementById('reg-email')?.value.trim() || '';
  const pw = document.getElementById('reg-pw')?.value || '';
  const studentNumber = document.getElementById('reg-stnum')?.value.trim() || '';
  const campus = document.getElementById('reg-campus')?.value || 'Main Campus';
  const role = state.regRole || 'student';

  if (!name || !email || !pw) {
    state.authError = 'Please fill in all required fields';
    refreshLogin();
    return;
  }

  try {
    const data = await api('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password: pw, student_number: studentNumber, campus, role })
    });
    state.user = data.user;
    window.location.href = homePageFor(data.user.role);
  } catch (e) {
    state.authError = e.message;
    refreshLogin();
  }
}

async function handleLogout() {
  try { await api('/api/auth/logout', { method: 'POST' }); } catch (_) { }
  state.user = null;
  localStorage.removeItem('ibhotwe_cart');
  sessionStorage.clear();
  window.location.href = 'login.html';
}

function refreshLogin() {
  const el = document.getElementById('login-page');
  if (el) {
    el.innerHTML = renderLogin();
    bindLogin();
  }
}
