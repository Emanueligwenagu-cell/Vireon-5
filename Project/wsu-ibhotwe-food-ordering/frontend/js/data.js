const IMGS = {
  campus: 'https://images.unsplash.com/photo-1758432370137-bda5e8a097b0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  burger: 'https://images.unsplash.com/photo-1654987581885-a05493f5dc67?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  bowl: 'https://images.unsplash.com/photo-1644704170910-a0cdf183649b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  wings: 'https://images.unsplash.com/photo-1766589221522-d5beae155124?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  pizza: 'https://images.unsplash.com/photo-1688966601042-a7a794a2cdac?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  stew: 'https://images.unsplash.com/photo-1763048443535-1243379234e2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  samosa: 'https://images.unsplash.com/photo-1772729996007-40bad08b3c40?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
  smoothie: 'https://images.unsplash.com/photo-1697642452436-9c40773cbcbb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600',
};

const VENDORS = [
  {id:'v1',name:"Mama's Kitchen",desc:'Authentic South African home-style cooking. From pap to bunny chow, taste the culture.',campus:'Main Campus – Block C',img:IMGS.campus,rating:4.8,reviews:312,delivery:'15–25 min',isOpen:true,minOrder:30},
  {id:'v2',name:'Campus Bites',desc:'Quick, affordable, and delicious. Burgers, wings, and rolls made fresh every day.',campus:'Student Union – Ground Floor',img:IMGS.burger,rating:4.5,reviews:218,delivery:'10–20 min',isOpen:true,minOrder:25},
  {id:'v3',name:'The Green Bowl',desc:'Nutritious and delicious meals for health-conscious students. Fresh ingredients daily.',campus:'Science Block – Cafeteria',img:IMGS.bowl,rating:4.6,reviews:145,delivery:'15–20 min',isOpen:true,minOrder:40},
  {id:'v4',name:'Samoosa Palace',desc:'The best samoosas, spring rolls, and street snacks on campus. Spicy or mild – your choice!',campus:'Arts Block – Kiosk 7',img:IMGS.samosa,rating:4.7,reviews:289,delivery:'5–15 min',isOpen:true,minOrder:20},
  {id:'v5',name:'Slice & Dice',desc:'Campus-favourite pizza with generous toppings. Great for group orders.',campus:'Res Area – Common Room',img:IMGS.pizza,rating:4.4,reviews:176,delivery:'20–35 min',isOpen:false,minOrder:50},
];

const FOODS = [
  {id:'f1',vid:'v1',name:'Bunny Chow',desc:'A hollowed-out loaf of white bread filled with spicy curry. Classic Durban street food.',price:45,cat:'traditional',img:IMGS.stew,rating:4.9,reviews:204,prep:15,popular:true,discount:10,tags:['spicy','filling','veg-option']},
  {id:'f2',vid:'v1',name:'Pap & Wors',desc:'Creamy maize pap served with flame-grilled boerewors sausage and chakalaka.',price:55,cat:'traditional',img:IMGS.stew,rating:4.7,reviews:156,prep:20,popular:true,tags:['hearty','local-favourite']},
  {id:'f3',vid:'v1',name:'Boerewors Roll',desc:'A juicy boerewors sausage in a fresh roll with tomato sauce and mustard.',price:35,cat:'traditional',img:IMGS.stew,rating:4.6,reviews:98,prep:10,popular:false,tags:['quick','budget-friendly']},
  {id:'f4',vid:'v2',name:'Classic Cheeseburger',desc:'Juicy beef patty with cheddar, lettuce, tomato, and secret sauce on a toasted bun.',price:65,cat:'fast-food',img:IMGS.burger,rating:4.5,reviews:187,prep:12,popular:true,discount:15,tags:["students-favourite","filling"]},
  {id:'f5',vid:'v2',name:'Chicken Wings x6',desc:'Crispy fried chicken wings tossed in your choice of peri-peri, BBQ, or lemon herb sauce.',price:60,cat:'fast-food',img:IMGS.wings,rating:4.7,reviews:143,prep:18,popular:true,tags:['shareable','spicy-option']},
  {id:'f6',vid:'v2',name:'Gatsby Roll',desc:'A massive sub loaded with chips, sausage, atchar and sauce. Uniquely Cape Town.',price:70,cat:'fast-food',img:IMGS.burger,rating:4.4,reviews:89,prep:15,popular:false,tags:['sharing','huge']},
  {id:'f7',vid:'v3',name:'Avo Grain Bowl',desc:'Quinoa and brown rice base with avocado, roasted chickpeas, and lemon tahini dressing.',price:75,cat:'healthy',img:IMGS.bowl,rating:4.8,reviews:112,prep:10,popular:true,tags:['vegan','gluten-free-option']},
  {id:'f8',vid:'v3',name:'Chicken Rice Bowl',desc:'Grilled chicken strips over brown rice with roasted veggies and peri-peri drizzle.',price:70,cat:'healthy',img:IMGS.bowl,rating:4.6,reviews:95,prep:12,popular:false,discount:5,tags:['high-protein','meal-prep']},
  {id:'f9',vid:'v4',name:'Samoosas x3',desc:'Golden fried pastry triangles filled with spiced mince or vegetable curry.',price:25,cat:'snacks',img:IMGS.samosa,rating:4.9,reviews:278,prep:5,popular:true,tags:['veg-option','snack','affordable']},
  {id:'f10',vid:'v4',name:'Spring Rolls x4',desc:'Crispy vegetable spring rolls served with sweet chilli dipping sauce.',price:30,cat:'snacks',img:IMGS.samosa,rating:4.5,reviews:134,prep:8,popular:false,tags:['vegan','snack']},
  {id:'f11',vid:'v5',name:'Margarita Pizza',desc:'Classic tomato base, fresh mozzarella, and basil on a hand-tossed crust.',price:85,cat:'pizza',img:IMGS.pizza,rating:4.4,reviews:121,prep:25,popular:false,discount:20,tags:['vegetarian','classic']},
  {id:'f12',vid:'v5',name:'Chicken Supreme Pizza',desc:'Loaded with grilled chicken, peppers, onions, mushrooms, and cream sauce.',price:95,cat:'pizza',img:IMGS.pizza,rating:4.6,reviews:98,prep:30,popular:true,tags:['group-meal','hearty']},
  {id:'f13',vid:'v3',name:'Tropical Smoothie',desc:'Blended mango, pineapple, banana, and coconut water. Refreshing and nutritious.',price:40,cat:'drinks',img:IMGS.smoothie,rating:4.7,reviews:167,prep:5,popular:true,tags:['vegan','refreshing','cold']},
  {id:'f14',vid:'v3',name:'Green Detox Juice',desc:'Spinach, cucumber, ginger, apple, and lemon. Your daily green boost.',price:45,cat:'drinks',img:IMGS.smoothie,rating:4.5,reviews:88,prep:5,popular:false,tags:['detox','healthy']},
];

const CATEGORIES = [
  {id:'all',label:'All',icon:'🍽️'},
  {id:'fast-food',label:'Fast Food',icon:'🍔'},
  {id:'traditional',label:'Traditional',icon:'🍲'},
  {id:'healthy',label:'Healthy',icon:'🥗'},
  {id:'snacks',label:'Snacks',icon:'🥟'},
  {id:'pizza',label:'Pizza',icon:'🍕'},
  {id:'drinks',label:'Drinks',icon:'🥤'},
];

const PROMOS = [
  {id:'p1',title:'Student Monday Deal',desc:'20% off all Traditional meals every Monday',code:'MONDAY20',discount:20,icon:'🎓'},
  {id:'p2',title:'Exam Season Bundle',desc:'Buy any meal + drink, get snacks 50% off',code:'EXAMTIME',discount:50,icon:'📚'},
  {id:'p3',title:'First Order Special',desc:'15% off your first order on Ibhotwe',code:'WELCOME15',discount:15,icon:'🎉'},
];

const PROMO_CODES = {MONDAY20:20,EXAMTIME:50,WELCOME15:15};

