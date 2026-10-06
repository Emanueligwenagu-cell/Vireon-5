function getFilteredFoods(){
  let items = [...FOODS];
  if(state.activeCategory!=='all') items=items.filter(f=>f.cat===state.activeCategory);
  if(state.searchQuery){
    const q=state.searchQuery.toLowerCase();
    items=items.filter(f=>f.name.toLowerCase().includes(q)||f.desc.toLowerCase().includes(q)||f.tags.some(t=>t.toLowerCase().includes(q)));
  }
  items=items.filter(f=>f.price<=state.priceMax);
  if(state.minRating>0) items=items.filter(f=>f.rating>=state.minRating);
  switch(state.sortBy){
    case 'price-asc': items.sort((a,b)=>a.price-b.price); break;
    case 'price-desc': items.sort((a,b)=>b.price-a.price); break;
    case 'rating': items.sort((a,b)=>b.rating-a.rating); break;
    case 'prepTime': items.sort((a,b)=>a.prep-b.prep); break;
    default: items.sort((a,b)=>(b.popular?1:0)-(a.popular?1:0));
  }
  return items;
}

function renderBrowse(){
  const filtered = getFilteredFoods();
  const hasFilters = state.activeCategory!=='all'||state.searchQuery||state.minRating>0;
  return `
  <div class="browse-sticky">
    <div class="container">
      <div class="browse-search-row">
        <div class="input-wrap" style="flex:1">
          <span class="icon">🔍</span>
          <input class="input has-icon" id="browse-search" placeholder="Search meals, ingredients, vendors..." value="${escHtml(state.searchQuery)}"/>
          ${state.searchQuery?`<button onclick="clearBrowseSearch()" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);color:var(--gray-400);font-size:16px;border:none;background:none;cursor:pointer">✕</button>`:''}
        </div>
        <select class="select" id="sort-sel" style="width:140px" onchange="browseSortChange(this.value)">
          <option value="popular"${state.sortBy==='popular'?' selected':''}>Popular</option>
          <option value="price-asc"${state.sortBy==='price-asc'?' selected':''}>Price: Low</option>
          <option value="price-desc"${state.sortBy==='price-desc'?' selected':''}>Price: High</option>
          <option value="rating"${state.sortBy==='rating'?' selected':''}>Top Rated</option>
          <option value="prepTime"${state.sortBy==='prepTime'?' selected':''}>Fastest</option>
        </select>
        <button class="btn${state.filtersOpen?' btn-primary':' btn-outline'}" onclick="toggleBrowseFilters()">
          ⚙ Filters
        </button>
      </div>
      <div class="browse-filters${state.filtersOpen?' open':''}" id="browse-filter-panel">
        <div>
          <label class="label">Price Range: R0 – R${state.priceMax}</label>
          <input type="range" min="20" max="200" value="${state.priceMax}" oninput="updatePriceRange(this.value)" style="width:100%;accent-color:var(--orange)"/>
        </div>
        <div>
          <label class="label">Min Rating: ${state.minRating>0?state.minRating+'+':'Any'}</label>
          <div class="rating-btns">
            ${[0,4,4.5,4.8].map(r=>`<button class="rating-btn${state.minRating===r?' active':''}" onclick="setMinRating(${r})">${r===0?'Any':'★ '+r+'+'}</button>`).join('')}
          </div>
        </div>
      </div>
      <div class="cat-pills">
        ${CATEGORIES.map(c=>`<button class="cat-pill${state.activeCategory===c.id?' active':''}" onclick="setBrowseCat('${c.id}')">${c.icon} ${c.label}</button>`).join('')}
      </div>
    </div>
  </div>
  <div class="container">
    <div class="results-bar">
      <div class="results-count">
        <strong>${filtered.length}</strong> results
        ${state.searchQuery?` for "<em>${escHtml(state.searchQuery)}</em>"` : ''}
      </div>
      ${hasFilters?`<button class="clear-btn" onclick="clearAllFilters()">✕ Clear filters</button>`:''}
    </div>
    ${filtered.length===0?`
    <div class="no-results">
      <div class="icon">🔍</div>
      <h3>No results found</h3>
      <p>Try adjusting your search or filters</p>
    </div>`:`
    <div class="food-grid">
      ${filtered.map(f=>{
        const vname = getVendorName(f.vid);
        return `<div>${foodCardHTML(f)}<div class="food-vendor-label">📍 ${escHtml(vname)}</div></div>`;
      }).join('')}
    </div>`}
  </div>`;
}

function bindBrowse(){
  const s = document.getElementById('browse-search');
  if(s){
    s.addEventListener('input',e=>{state.searchQuery=e.target.value; refreshBrowse();});
    s.addEventListener('keydown',e=>{if(e.key==='Escape'){state.searchQuery='';refreshBrowse();}});
  }
}
function refreshBrowse(){
  const el=document.getElementById('browse-page');
  el.innerHTML=renderBrowse(); bindBrowse();
}
function clearBrowseSearch(){state.searchQuery='';refreshBrowse();}
function browseSortChange(v){state.sortBy=v;refreshBrowse();}
function toggleBrowseFilters(){state.filtersOpen=!state.filtersOpen;refreshBrowse();}
function setBrowseCat(c){state.activeCategory=c;refreshBrowse();}
function updatePriceRange(v){state.priceMax=Number(v);refreshBrowse();}
function setMinRating(r){state.minRating=r;refreshBrowse();}
function clearAllFilters(){
  state.activeCategory='all';state.searchQuery='';state.minRating=0;state.priceMax=200;
  refreshBrowse();
}

