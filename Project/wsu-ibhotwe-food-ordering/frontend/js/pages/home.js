function renderHome(){
  const popular = FOODS.filter(f=>f.popular).slice(0,6);
  const openCount = VENDORS.filter(v=>v.isOpen).length;
  const userName = state.user?state.user.name.split(' ')[0]:'';
  return `
  <!-- HERO -->
  <section class="hero">
    <div class="hero-blur1"></div><div class="hero-blur2"></div>
    <div class="container">
      <div class="hero-grid">
        <div>
          ${state.user?`<div class="hero-greeting">👋 Hey, ${escHtml(userName)}!</div>`:''}
          <h1>Campus food,<br><span>delivered fast</span></h1>
          <p>Order from your favourite campus vendors. Fresh meals from Mama's Kitchen, Campus Bites, and more — right to your spot.</p>
          <div class="hero-search">
            <div class="input-wrap" style="flex:1">
              <span class="icon">🔍</span>
              <input class="input has-icon" id="hero-search" placeholder="Search for food, vendors..." value="${escHtml(state.searchQuery)}"/>
            </div>
            <button class="btn btn-primary" onclick="doHeroSearch()">Search</button>
          </div>
          <div class="hero-stats">
            <div class="hero-stat"><p>${VENDORS.length}+</p><p>Vendors</p></div>
            <div class="hero-stat"><p>${FOODS.length}+</p><p>Meals</p></div>
            <div class="hero-stat"><p>15 min</p><p>Avg. wait</p></div>
          </div>
        </div>
        <div class="hero-imgs">
          <div class="hero-img-main"><img src="${FOODS[0].img}?w=600" alt="food" loading="lazy"/></div>
          <div class="hero-img-sm"><img src="${FOODS[3].img}?w=400" alt="food" loading="lazy"/></div>
          <div class="hero-img-sm"><img src="${FOODS[8].img}?w=400" alt="food" loading="lazy"/></div>
        </div>
      </div>
    </div>
  </section>

  <!-- CATEGORIES -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <div><div class="section-title">Browse by Category</div></div>
        <a class="section-link" href="#" onclick="navigate('browse');return false">View all →</a>
      </div>
      <div class="cats-scroll">
        ${CATEGORIES.map(c=>`
        <button class="cat-btn" onclick="goBrowseCat('${c.id}')">
          <span class="emoji">${c.icon}</span>
          <span>${c.label}</span>
        </button>`).join('')}
      </div>
    </div>
  </section>

  <!-- PROMOS -->
  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="promos-grid">
        ${PROMOS.map(p=>`
        <div class="promo-card">
          <div class="promo-icon">${p.icon}</div>
          <div class="promo-title">${escHtml(p.title)}</div>
          <div class="promo-desc">${escHtml(p.desc)}</div>
          <div class="promo-code">🎁 ${p.code}</div>
          <div class="promo-bg-emoji">🎁</div>
        </div>`).join('')}
      </div>
    </div>
  </section>

  <!-- VENDORS -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <div>
          <div class="section-title">Open Vendors</div>
          <div class="section-sub">${openCount} vendors available now</div>
        </div>
      </div>
      <div class="vendors-grid">
        ${VENDORS.map(v=>vendorCardHTML(v)).join('')}
      </div>
    </div>
  </section>

  <!-- POPULAR -->
  <section class="section">
    <div class="container">
      <div class="section-header">
        <div>
          <div class="section-title">🔥 Popular Right Now</div>
          <div class="section-sub">Most ordered by students today</div>
        </div>
        <a class="section-link" href="#" onclick="navigate('browse');return false">See all →</a>
      </div>
      <div class="popular-grid">
        ${popular.map(f=>foodCardHTML(f,true)).join('')}
      </div>
    </div>
  </section>

  <!-- FEATURES -->
  <section class="section">
    <div class="container">
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">⚡</div>
          <div><div class="feature-title">Fast & Fresh</div><div class="feature-desc">Average 15-min wait time on campus</div></div>
        </div>
        <div class="feature-card">
          <div class="feature-icon" style="background:var(--green-light)">🎁</div>
          <div><div class="feature-title">Student Deals</div><div class="feature-desc">Exclusive discounts for registered students</div></div>
        </div>
        <div class="feature-card">
          <div class="feature-icon" style="background:var(--purple-light)">👥</div>
          <div><div class="feature-title">Group Orders</div><div class="feature-desc">Share your cart with friends easily</div></div>
        </div>
      </div>
    </div>
  </section>

  <!-- GAME CTA -->
  <section class="section" style="padding-bottom:40px">
    <div class="container">
      <div class="game-cta">
        <div class="game-cta-bg">❌ ⭕</div>
        <div class="game-cta-icon">🎮</div>
        <h2>Waiting for your order?</h2>
        <p>Play a quick Tic-Tac-Toe game while your food is being prepared!</p>
        <button class="btn btn-primary btn-lg" onclick="navigate('game')">Play Now →</button>
      </div>
    </div>
  </section>`;
}

function bindHome(){
  const inp = document.getElementById('hero-search');
  if(inp) inp.addEventListener('keydown',e=>{if(e.key==='Enter') doHeroSearch();});
}
function doHeroSearch(){
  const v = document.getElementById('hero-search');
  if(v){state.searchQuery=v.value;navigate('browse');}
}
function goBrowseCat(cat){
  state.activeCategory=cat;
  navigate('browse');
}

