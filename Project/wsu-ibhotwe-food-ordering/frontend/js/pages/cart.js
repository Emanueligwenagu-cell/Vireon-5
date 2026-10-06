function renderCart(){
  if(state.orderPlaced){
    const oid=state.orderPlaced;
    return `
    <div class="order-success">
      <div class="order-success-card success-card">
        <div class="success-icon">✓</div>
        <h2>Order Placed! 🎉</h2>
        <p>Your order <span class="success-id">${oid}</span> has been received.</p>
        <p style="font-size:13px;color:var(--gray-400)">Your food is being prepared. Estimated wait: 15–20 mins.</p>
        <div class="success-btns">
          <button class="btn btn-primary-grad btn-full btn-lg" onclick="navigate('orders')">📦 Track My Order</button>
          <button class="btn btn-secondary btn-full btn-lg" onclick="navigate('game')">🎮 Play While You Wait</button>
          <button class="btn" style="color:var(--orange)" onclick="navigate('browse')">Order more food</button>
        </div>
      </div>
    </div>`;
  }
  if(state.cart.length===0){
    return `
    <div class="empty-cart">
      <div class="icon">🛒</div>
      <h2>Your cart is empty</h2>
      <p>Add some delicious campus food to get started!</p>
      <button class="btn btn-primary-grad btn-lg" onclick="navigate('browse')">🍽️ Browse Food</button>
    </div>`;
  }
  const ct = cartTotal();
  const disc = promoDiscount();
  const dlv = deliveryFee();
  const fin = ct-disc+dlv;
  const payOpts=[
    {id:'card',label:'Card',sub:'Debit / Credit',icon:'💳'},
    {id:'mobile',label:'Mobile Pay',sub:'SnapScan / Zapper',icon:'📱'},
    {id:'cash',label:'Cash on Collect',sub:'Pay when you pick up',icon:'💵'},
  ];
  return `
  <div class="container">
    <div class="cart-layout">
      <div>
        <div class="cart-header">
          <button class="back-btn" onclick="navigate('browse')">←</button>
          <div>
            <div class="font-black" style="font-size:20px;color:var(--gray-900)">Your Cart</div>
            <div style="font-size:14px;color:var(--gray-500)">${cartCount()} item${cartCount()!==1?'s':''}</div>
          </div>
        </div>
        ${state.cart.map(item=>{
          const dp=(discountedPrice(item)*item.qty).toFixed(0);
          const each=discountedPrice(item).toFixed(0);
          return `
          <div class="cart-item">
            <div class="cart-item-img"><img src="${item.img}?w=160" alt="${escHtml(item.name)}" loading="lazy"/></div>
            <div class="cart-item-body">
              <div class="cart-item-top">
                <div class="cart-item-name">${escHtml(item.name)}</div>
                <div class="cart-item-del" onclick="removeFromCart('${item.id}')">🗑</div>
              </div>
              ${item.discount?`<div class="cart-item-discount">-${item.discount}% off</div>`:''}
              <div class="cart-item-bottom">
                <div class="qty-ctrl">
                  <div class="qty-btn minus" onclick="updateCartQty('${item.id}',${item.qty-1})">−</div>
                  <span class="qty-val">${item.qty}</span>
                  <div class="qty-btn plus" onclick="updateCartQty('${item.id}',${item.qty+1})">+</div>
                </div>
                <div class="cart-item-price">
                  <div class="total">R${dp}</div>
                  ${item.qty>1?`<div class="each">R${each} each</div>`:''}
                </div>
              </div>
            </div>
          </div>`;
        }).join('')}
      </div>
      <div>
        <!-- Promo -->
        <div class="summary-card">
          <h3>🏷 Promo Code</h3>
          ${state.activePromo?`
          <div class="promo-success">
            <div class="promo-success-info">
              <div class="code">${state.activePromo.code}</div>
              <div class="msg">-${state.activePromo.discount}% discount applied!</div>
            </div>
            <button onclick="removePromo()" style="color:var(--green-dark);font-size:18px;background:none;border:none;cursor:pointer">✕</button>
          </div>`:`
          <div class="promo-row">
            <input class="input" id="promo-inp" placeholder="Enter code" value="${escHtml(state.promoInput)}" oninput="state.promoInput=this.value.toUpperCase();this.value=state.promoInput" onkeydown="if(event.key==='Enter')applyPromo()" style="font-family:monospace"/>
            <button class="btn btn-primary" onclick="applyPromo()">Apply</button>
          </div>
          ${state.promoError?`<div class="promo-error">${escHtml(state.promoError)}</div>`:''}
          <div class="promo-hint">Try: MONDAY20, EXAMTIME, WELCOME15</div>`}
        </div>
        <!-- Summary -->
        <div class="summary-card">
          <h3>Order Summary</h3>
          <div class="summary-line"><span>Subtotal (${cartCount()} items)</span><span>R${ct.toFixed(0)}</span></div>
          ${state.activePromo?`<div class="summary-line green"><span>Promo (${state.activePromo.code})</span><span>-R${disc.toFixed(0)}</span></div>`:''}
          <div class="summary-line"><span>Delivery fee</span><span${dlv===0?' style="color:var(--green-dark);font-weight:600"':''}>${dlv===0?'Free':'R'+dlv}</span></div>
          <div class="summary-divider"></div>
          <div class="summary-total"><span>Total</span><span>R${fin.toFixed(0)}</span></div>
        </div>
        <!-- Payment -->
        <div class="summary-card">
          <h3>💳 Payment Method</h3>
          ${payOpts.map(p=>`
          <div class="pay-option${state.cartPayment===p.id?' selected':''}" onclick="setPayment('${p.id}')">
            <span class="pay-icon">${p.icon}</span>
            <div><div class="pay-label">${p.label}</div><div class="pay-sub">${p.sub}</div></div>
            <div class="pay-radio${state.cartPayment===p.id?' checked':''}"></div>
          </div>`).join('')}
        </div>
        <button class="btn btn-primary-grad btn-full btn-lg" onclick="placeOrder()">
          Place Order • R${fin.toFixed(0)}
        </button>
      </div>
    </div>
  </div>`;
}

function bindCart(){}

function setPayment(p){state.cartPayment=p;refreshCart();}
function applyPromo(){
  const code=state.promoInput.trim().toUpperCase();
  if(!code) return;
  const disc=PROMO_CODES[code];
  if(disc){
    state.activePromo={code,discount:disc};
    state.promoError='';
  } else {
    state.promoError='Invalid code. Try MONDAY20, EXAMTIME, or WELCOME15';
  }
  refreshCart();
}
function removePromo(){state.activePromo=null;refreshCart();}
async function placeOrder(){
  if(state.user?.role==='vendor'){ alert('Vendor accounts cannot place orders.'); return; }
  if(state.cart.length===0) return;
  try{
    const payload={items:state.cart.map(i=>({product_id:i.id,qty:i.qty})),payment:state.cartPayment,promo_code:state.activePromo?.code||null};
    const data=await api('/api/orders',{method:'POST',body:JSON.stringify(payload)});
    state.orders.unshift(data.order);
    state.cart=[]; persistCart(); state.activePromo=null; state.orderPlaced=data.order.id; state.promoInput='';
    updateNavCart(); refreshCart();
  }catch(e){ alert(e.message); }
}
function refreshCart(){
  const el=document.getElementById('cart-page');
  el.innerHTML=renderCart();bindCart();
}

