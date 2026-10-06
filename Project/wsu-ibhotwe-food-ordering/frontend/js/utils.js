function discountedPrice(food){
  return food.discount ? food.price*(1-food.discount/100) : food.price;
}
function cartTotal(){
  return state.cart.reduce((s,i)=>s+discountedPrice(i)*i.qty,0);
}
function cartCount(){
  return state.cart.reduce((s,i)=>s+i.qty,0);
}
function promoDiscount(){
  return state.activePromo ? cartTotal()*(state.activePromo.discount/100) : 0;
}
function finalTotal(){
  const t = cartTotal()-promoDiscount();
  const delivery = t>100?0:10;
  return t+delivery;
}
function deliveryFee(){
  const t = cartTotal()-promoDiscount();
  return t>100?0:10;
}
function formatTime(date){
  return date.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
}
function formatDate(date){
  return date.toLocaleDateString();
}
function stars(rating,size=14){
  return `<span style="color:#f59e0b;font-size:${size}px">★</span> ${rating}`;
}
function getVendorName(vid){
  const v=VENDORS.find(v=>v.id===vid);
  return v?v.name:'Unknown';
}
function escHtml(s){
  if(!s) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
let _toastTimer=null;
function showToast(msg){
  let el=document.getElementById('ibhotwe-toast');
  if(!el){
    el=document.createElement('div');
    el.id='ibhotwe-toast';
    el.className='ibhotwe-toast';
    document.body.appendChild(el);
  }
  el.textContent=msg;
  el.classList.remove('show');
  void el.offsetWidth;
  el.classList.add('show');
  clearTimeout(_toastTimer);
  _toastTimer=setTimeout(()=>el.classList.remove('show'),1800);
}

