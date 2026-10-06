function renderOrders(){
  const activeOrders=state.orders.filter(o=>o.status!=='completed'&&o.status!=='cancelled');
  let filtered=state.orders;
  if(state.orderFilter==='active') filtered=state.orders.filter(o=>o.status!=='completed'&&o.status!=='cancelled');
  if(state.orderFilter==='completed') filtered=state.orders.filter(o=>o.status==='completed'||o.status==='cancelled');
  return `
  <div class="container">
    <div class="orders-wrap">
      <div class="orders-header">
        <h1>My Orders</h1>
        <p>${activeOrders.length>0?activeOrders.length+' active order'+(activeOrders.length!==1?'s':''):'No active orders right now'}</p>
      </div>
      ${activeOrders.length>0?`
      <a class="game-banner" href="#" onclick="navigate('game');return false">
        <div class="game-banner-icon">🎮</div>
        <div>
          <h3>Play while you wait!</h3>
          <p>Challenge yourself to a game of Tic-Tac-Toe</p>
        </div>
        <div class="game-banner-arr">→</div>
      </a>`:''}
      <div class="order-tabs">
        ${[{id:'all',l:'All Orders'},{id:'active',l:'Active'},{id:'completed',l:'Completed'}].map(t=>`
        <button class="order-tab${state.orderFilter===t.id?' active':''}" onclick="setOrderFilter('${t.id}')">${t.l}</button>`).join('')}
      </div>
      ${filtered.length===0?`
      <div class="empty-orders">
        <div style="font-size:64px;margin-bottom:14px">📦</div>
        <h3 style="font-size:18px;font-weight:700;color:var(--gray-700);margin-bottom:8px">No orders yet</h3>
        <p style="color:var(--gray-400);margin-bottom:20px">Place your first order and track it right here</p>
        <button class="btn btn-primary" onclick="navigate('browse')">Browse Food</button>
      </div>`:`
      <div>
        ${filtered.map(o=>{
          const cfg=statusConfig(o.status);
          const expanded=!!state.expandedOrders[o.id];
          return `
          <div class="order-card" id="ocard-${o.id}">
            <div class="order-card-header">
              <div class="order-card-header-top">
                <div>
                  <div class="order-id">#${o.id} <span class="badge" style="background:${cfg.bg};color:${cfg.color};margin-left:4px">${cfg.icon} ${cfg.label}</span></div>
                  <div class="order-meta">${escHtml(o.vendorName)} · ${formatTime(o.placedAt instanceof Date?o.placedAt:new Date(o.placedAt))} · ${formatDate(o.placedAt instanceof Date?o.placedAt:new Date(o.placedAt))}</div>
                </div>
                <div>
                  <div class="order-total">R${o.total}</div>
                  <div class="order-payment">${o.payment}</div>
                </div>
              </div>
              ${o.status!=='completed'&&o.status!=='cancelled'?orderProgressHTML(o.status):''}
            </div>
            <div class="order-card-body">
              <div class="order-items-row">
                <div class="order-items-list">${o.items.map(i=>`<span class="order-item-chip">${i.qty}× ${escHtml(i.name)}</span>`).join('')}</div>
                ${o.status!=='completed'&&o.status!=='cancelled'?`<div class="order-est">⏱ ${o.est}</div>`:''}
              </div>
              <span class="order-details-toggle" onclick="toggleOrderExpand('${o.id}')">${expanded?'Show less ↑':'Show details ↓'}</span>
              ${expanded?`
              <div class="order-details-body">
                ${o.items.map(i=>`<div class="order-detail-line"><span>${i.qty}× ${escHtml(i.name)}</span><span>R${(discountedPrice(i)*i.qty).toFixed(0)}</span></div>`).join('')}
                <div class="order-detail-total"><span>Total</span><span>R${o.total}</span></div>
              </div>`:''}
              ${o.status==='completed'?`
              <div class="rate-prompt">
                <div class="rate-prompt-text"><p>How was your meal?</p><p>Rate your experience</p></div>
                <div class="stars" id="stars-${o.id}">
                  ${[1,2,3,4,5].map(s=>`<span class="star" data-oid="${o.id}" data-star="${s}" onclick="rateStar('${o.id}',${s})">★</span>`).join('')}
                </div>
              </div>`:''}
            </div>
          </div>`;
        }).join('')}
      </div>`}
      ${state.user?`
      <div class="loyalty-banner">
        <div>
          <div class="loyalty-pts">${state.user.loyaltyPoints} pts</div>
          <div class="loyalty-label">Loyalty Points Balance</div>
          <div class="loyalty-hint">Earn 10 pts per order · Redeem for discounts</div>
        </div>
        <div class="loyalty-bg">⭐</div>
      </div>`:''}
    </div>
  </div>`;
}

function bindOrders(){}
function setOrderFilter(f){state.orderFilter=f;refreshOrders();}
function toggleOrderExpand(id){state.expandedOrders[id]=!state.expandedOrders[id];refreshOrders();}
function rateStar(oid,s){
  const cont=document.getElementById('stars-'+oid);
  if(!cont) return;
  cont.querySelectorAll('.star').forEach((el,i)=>{
    el.classList.toggle('lit',i<s);
  });
}
function refreshOrders(){
  const el=document.getElementById('orders-page');
  el.innerHTML=renderOrders();bindOrders();
}

