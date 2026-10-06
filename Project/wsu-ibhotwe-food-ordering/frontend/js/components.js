function foodCardHTML(food, compact=false){
  const dp = discountedPrice(food).toFixed(0);
  const inCart = state.cart.find(c=>c.id===food.id);
  const tagsHtml = food.tags.slice(0,2).map(t=>`<span class="tag">${t}</span>`).join('');
  return `
  <div class="food-card" data-fid="${food.id}">
    <div class="food-card-img">
      <img src="${food.img}?w=400" alt="${escHtml(food.name)}" loading="lazy"/>
      <div class="food-card-badges">
        ${food.popular?'<span class="badge badge-orange">🔥 Popular</span>':''}
        ${food.discount?`<span class="badge badge-green">-${food.discount}%</span>`:''}
      </div>
      <div class="food-card-add" onclick="quickAddFood('${food.id}')">+</div>
    </div>
    <div class="food-card-body">
      <div class="food-card-name">${escHtml(food.name)}</div>
      ${!compact?`<div class="food-card-desc">${escHtml(food.desc)}</div>`:''}
      ${!compact&&food.tags.length?`<div class="food-card-tags">${tagsHtml}</div>`:''}
      <div class="food-card-meta">
        <span><span class="star-icon">★</span>${food.rating}</span>
        <span>⏱ ${food.prep}min</span>
      </div>
      <div class="food-card-footer">
        <div>
          <span class="price">R${dp}</span>
          ${food.discount?`<span class="price-old">R${food.price}</span>`:''}
        </div>
        <button class="add-btn${inCart?' in-cart':''}" onclick="quickAddFood('${food.id}')">
          + ${inCart?`(${inCart.qty})`:'Add'}
        </button>
      </div>
    </div>
  </div>`;
}

function vendorCardHTML(v){
  return `
  <div class="vendor-card${!v.isOpen?' closed':''}" onclick="navigate('browse')">
    <div class="vendor-img">
      <img src="${v.img}" alt="${escHtml(v.name)}" loading="lazy"/>
      <div class="vendor-img-overlay"></div>
      <div class="vendor-img-bottom">
        <span class="vendor-name">${escHtml(v.name)}</span>
        <span class="vendor-status ${v.isOpen?'open':'closed'}">${v.isOpen?'Open':'Closed'}</span>
      </div>
    </div>
    <div class="vendor-body">
      <div class="vendor-campus">📍 ${escHtml(v.campus)}</div>
      <div class="vendor-meta">
        <span>${stars(v.rating)} (${v.reviews})</span>
        <span>⏱ ${v.delivery}</span>
        <span style="color:var(--orange);font-weight:600">Min R${v.minOrder}</span>
      </div>
    </div>
  </div>`;
}

function statusConfig(status){
  const map = {
    pending:{label:'Order Received',color:'#ca8a04',bg:'#fefce8',icon:'⏳',step:1},
    preparing:{label:'Being Prepared',color:'#2563eb',bg:'#eff6ff',icon:'👨‍🍳',step:2},
    ready:{label:'Ready for Pickup',color:'#16a34a',bg:'#f0fdf4',icon:'📦',step:3},
    completed:{label:'Completed',color:'#4b5563',bg:'#f9fafb',icon:'✅',step:4},
    cancelled:{label:'Cancelled',color:'#dc2626',bg:'#fef2f2',icon:'❌',step:0},
  };
  return map[status]||map.pending;
}

function orderProgressHTML(status){
  if(status==='cancelled') return '';
  const steps = ['pending','preparing','ready','completed'];
  const curStep = statusConfig(status).step;
  let html = '<div class="order-progress">';
  steps.forEach((s,i)=>{
    const cfg = statusConfig(s);
    const done = curStep>=cfg.step;
    const active = curStep===cfg.step;
    if(i>0) html+=`<div class="progress-line${done?' done-line':''}"></div>`;
    html+=`<div class="progress-step">
      <div class="progress-dot${done?' done':active?' active-dot':' pending-dot'}">${cfg.icon}</div>
      <div class="progress-label${done?' done-label':''}">${cfg.label.split(' ')[0]}</div>
    </div>`;
  });
  html+='</div>';
  return html;
}

function quickAddFood(fid){
  if(state.user?.role==='vendor'){ showToast('Vendor accounts cannot order food.'); return; }
  const food=FOODS.find(f=>String(f.id)===String(fid));
  if(!food) return;
  const existing=state.cart.find(c=>String(c.id)===String(fid));
  if(existing) existing.qty++;
  else state.cart.push({...food,qty:1});
  persistCart(); updateNavCart();
  refreshCurrentPage();
  showToast(`✓ Added ${food.name} to cart`);
}

function removeFromCart(id){
  state.cart=state.cart.filter(c=>String(c.id)!==String(id));
  persistCart(); updateNavCart();refreshCart();
}

function updateCartQty(id,qty){
  if(qty<=0){removeFromCart(id);return;}
  const item=state.cart.find(c=>String(c.id)===String(id));
  if(item) item.qty=qty;
  persistCart(); updateNavCart();refreshCart();
}

