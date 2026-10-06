function renderVendor(){
  const v=VENDORS[0];
  const totalRev=state.orders.filter(o=>o.status==='completed').reduce((s,o)=>s+o.total,0);
  const pendingCnt=state.orders.filter(o=>o.status==='pending'||o.status==='preparing').length;
  const completedCnt=state.orders.filter(o=>o.status==='completed').length;
  const avgR=(state.vendorMenuItems.reduce((s,i)=>s+i.rating,0)/state.vendorMenuItems.length).toFixed(1);
  return `
  <div class="container" style="padding-top:24px;padding-bottom:40px">
    <!-- Vendor header -->
    <div class="vendor-header-card">
      <div class="vendor-header-img">
        <img src="${v.img}" alt="${escHtml(v.name)}"/>
        <div class="vendor-header-overlay"></div>
        <div class="vendor-header-bottom">
          <div>
            <div class="vendor-dash-name">${escHtml(v.name)}</div>
            <div class="vendor-dash-campus">${escHtml(v.campus)}</div>
          </div>
          <button class="toggle-btn ${state.vendorOpen?'open':'closed'}" onclick="toggleVendorOpen()">
            ${state.vendorOpen?'✅ Open':'🔴 Closed'}
          </button>
        </div>
      </div>
      <div class="vendor-header-meta">
        <span>★ ${v.rating} rating</span> <span>·</span>
        <span>${v.reviews} reviews</span> <span>·</span>
        <span>${state.vendorMenuItems.length} menu items</span>
      </div>
    </div>
    <!-- Tabs -->
    <div class="vendor-dash-tabs">
      <button class="vendor-tab${state.vendorTab==='overview'?' active':''}" onclick="setVendorTab('overview')">📊 Overview</button>
      <button class="vendor-tab${state.vendorTab==='menu'?' active':''}" onclick="setVendorTab('menu')">👨‍🍳 Menu</button>
      <button class="vendor-tab${state.vendorTab==='orders'?' active':''}" onclick="setVendorTab('orders')">
        📦 Orders ${pendingCnt>0?`<span class="notif-dot">${pendingCnt}</span>`:''}
      </button>
    </div>

    ${state.vendorTab==='overview'?`
    <!-- OVERVIEW -->
    <div class="stats-grid">
      ${[
        {label:"Today's Revenue",val:`R${totalRev}`,icon:'💰',bg:'background:var(--green-light);color:var(--green-dark)'},
        {label:'Active Orders',val:pendingCnt,icon:'⏳',bg:'background:var(--blue-light);color:var(--blue)'},
        {label:'Completed Today',val:completedCnt,icon:'✅',bg:'background:var(--orange-light);color:var(--orange)'},
        {label:'Avg Rating',val:avgR,icon:'⭐',bg:'background:#fef9c3;color:#ca8a04'},
      ].map(s=>`
      <div class="stat-card">
        <div class="stat-icon" style="${s.bg}">${s.icon}</div>
        <div class="stat-val">${s.val}</div>
        <div class="stat-label">${s.label}</div>
      </div>`).join('')}
    </div>
    <div class="popular-list">
      <h3 style="font-weight:800;margin-bottom:14px;font-size:16px">🔥 Most Popular Items</h3>
      ${state.vendorMenuItems.sort((a,b)=>b.reviews-a.reviews).slice(0,5).map((item,i)=>`
      <div class="popular-item">
        <span class="popular-rank">#${i+1}</span>
        <div class="popular-img"><img src="${item.img}?w=80" alt="${escHtml(item.name)}" loading="lazy"/></div>
        <div class="popular-info">
          <div class="popular-name">${escHtml(item.name)}</div>
          <div class="popular-orders">${item.reviews} orders</div>
        </div>
        <div class="popular-right">
          <div class="popular-price">R${item.price}</div>
          <div class="popular-rating">★ ${item.rating}</div>
        </div>
      </div>`).join('')}
    </div>`:

    state.vendorTab==='menu'?`
    <!-- MENU -->
    <div class="menu-header">
      <span class="menu-count">Menu Items (${state.vendorMenuItems.length})</span>
      <button class="btn btn-primary btn-sm" onclick="openAddModal()">+ Add Item</button>
    </div>
    ${state.vendorMenuItems.map(item=>`
    <div class="menu-item" id="mitem-${item.id}">
      <div class="menu-item-img"><img src="${item.img}?w=120" alt="${escHtml(item.name)}" loading="lazy"/></div>
      <div class="menu-item-body">
        <div class="menu-item-name-row">
          <span class="menu-item-name">${escHtml(item.name)}</span>
          ${item.popular?'<span class="badge badge-orange" style="font-size:10px">Popular</span>':''}
        </div>
        <div class="menu-item-desc">${escHtml(item.desc)}</div>
        <div class="menu-item-meta">
          <span style="font-weight:700;color:var(--gray-900)">R${item.price}</span>
          <span>★ ${item.rating}</span>
          <span>⏱ ${item.prep}min</span>
        </div>
      </div>
      <div class="menu-item-actions">
        <button class="icon-btn edit" title="Edit">✏</button>
        <button class="icon-btn del" title="Delete" onclick="deleteMenuItem('${item.id}')">🗑</button>
      </div>
    </div>`).join('')}`:

    `<!-- ORDERS -->
    <h2 style="font-weight:800;font-size:16px;margin-bottom:14px">Incoming Orders</h2>
    ${state.orders.length===0?`<div style="text-align:center;padding:60px 0;color:var(--gray-400)">No orders yet</div>`:`
    ${state.orders.map(o=>{
      const cfg=statusConfig(o.status);
      return `
      <div class="order-mgmt-item">
        <div class="order-mgmt-header">
          <div>
            <span style="font-weight:900;font-size:14px">#${o.id}</span>
            <span class="badge" style="background:${cfg.bg};color:${cfg.color};margin-left:8px">${cfg.icon} ${cfg.label}</span>
          </div>
          <span style="font-weight:700;font-size:15px">R${o.total}</span>
        </div>
        <div class="order-mgmt-chips">${o.items.map(i=>`<span class="order-item-chip">${i.qty}× ${escHtml(i.name)}</span>`).join('')}</div>
        ${o.status!=='completed'&&o.status!=='cancelled'?`
        <div class="order-mgmt-actions">
          ${o.status==='pending'?`<button class="btn btn-blue btn-sm btn-full" onclick="vendorUpdateOrder('${o.id}','preparing')">Accept & Prepare</button>`:''}
          ${o.status==='preparing'?`<button class="btn btn-green btn-sm btn-full" onclick="vendorUpdateOrder('${o.id}','ready')">Mark Ready ✓</button>`:''}
          ${o.status==='ready'?`<button class="btn btn-primary btn-sm btn-full" onclick="vendorUpdateOrder('${o.id}','completed')">Complete Order</button>`:''}
          <button class="btn btn-red-outline btn-sm" onclick="vendorUpdateOrder('${o.id}','cancelled')">Cancel</button>
        </div>`:''}
      </div>`;
    }).join('')}`}
    `}
  </div>`;
}

function bindVendor(){}
function setVendorTab(t){state.vendorTab=t;refreshVendor();}
function toggleVendorOpen(){state.vendorOpen=!state.vendorOpen;refreshVendor();}
async function deleteMenuItem(id){
  try{await api('/api/vendor/menu/'+id,{method:'DELETE'}); state.vendorMenuItems=state.vendorMenuItems.filter(i=>i.id!==id);refreshVendor();}
  catch(e){alert(e.message)}
}
async function vendorUpdateOrder(oid,status){
  try{const data=await api('/api/vendor/orders/'+oid,{method:'PATCH',body:JSON.stringify({status})});
    const o=state.orders.find(o=>o.id===oid); if(o) Object.assign(o,data.order); refreshVendor();
  }catch(e){alert(e.message)}
}
function refreshVendor(){
  const el=document.getElementById('vendor-page');
  el.innerHTML=renderVendor();bindVendor();
}
function openAddModal(){
  document.getElementById('add-item-modal').classList.add('open');
}
function closeAddModal(){
  document.getElementById('add-item-modal').classList.remove('open');
  document.getElementById('new-item-name').value='';
  document.getElementById('new-item-desc').value='';
  document.getElementById('new-item-price').value='';
  document.getElementById('new-item-prep').value='';
}
async function confirmAddItem(){
  const name=document.getElementById('new-item-name').value.trim();
  const price=document.getElementById('new-item-price').value;
  if(!name||!price) return;
  try{
    const data=await api('/api/vendor/menu',{method:'POST',body:JSON.stringify({name,description:document.getElementById('new-item-desc').value,price:Number(price),category:document.getElementById('new-item-cat').value,prep:Number(document.getElementById('new-item-prep').value)||15})});
    state.vendorMenuItems.push({...data.item, desc:data.item.description||'', cat:data.item.category, img:data.item.image, vid:data.item.vendor_id}); closeAddModal();refreshVendor();
  }catch(e){alert(e.message)}
}

