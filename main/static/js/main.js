// main/static/js/main.js

// Слайды для Hero
const heroSlides = [
    { image: 'https://images.unsplash.com/photo-1771573391561-ab2bfc7e27a7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1920', title: 'Профессиональная резьба по камню', subtitle: 'Услуги от мастеров своего дела', url: '/services/', text_button: 'Смотреть услуги' },
    { image: 'https://images.unsplash.com/photo-1426927308491-6380b6a9936f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1920', title: 'Широкий выбор инструментов', subtitle: 'От ручных до электроинструментов', url: '/catalog/', text_button: 'Смотреть каталог' },
    { image: 'https://images.unsplash.com/photo-1759059228251-273b42bbcaf1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=1920', title: 'Работа с любыми материалами', subtitle: 'Гранит, мрамор, песчаник и другие', url: '/works_and_products/', text_button: 'Работы и изделия из камня' }
];


// Слайдер
let currentSlide = 0;
let slideInterval;
function initHeroSlider() {
    const container = document.getElementById('heroSlider');
    if (!container) return;
    function renderSlide(index) {
        const slide = heroSlides[index];
        container.innerHTML = `
            <div class="absolute inset-0 transition-opacity duration-1000 opacity-100">
                <img src="${slide.image}" class="w-full h-full object-cover opacity-60" alt="">
                <div class="absolute inset-0 bg-gradient-to-r from-black/80 to-transparent">
                    <div class="max-w-7xl mx-auto px-4 h-full flex items-center">
                        <div class="max-w-2xl">
                            <h1 class="text-5xl md:text-6xl font-bold text-white mb-4">${slide.title}</h1>
                            <p class="text-xl md:text-2xl text-zinc-200 mb-8">${slide.subtitle}</p>
                            <a href="${slide.url}" 
                                <button  class="bg-white text-zinc-900 px-8 py-4 rounded-lg font-semibold hover:bg-zinc-100 transition">${slide.text_button}</button>
                            </a >
                        </div>
                    </div>
                </div>
            </div>
            <div class="absolute left-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 text-white p-3 rounded-full backdrop-blur-sm cursor-pointer" id="prevSlide">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
            </div>
            <div class="absolute right-4 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/30 text-white p-3 rounded-full backdrop-blur-sm cursor-pointer" id="nextSlide">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </div>
            <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex space-x-2" id="dotsContainer"></div>
        `;
        // Точки (dots)
        const dotsDiv = document.getElementById('dotsContainer');
        dotsDiv.innerHTML = heroSlides.map((_, i) => `<button class="w-3 h-3 rounded-full ${i===index ? 'bg-white' : 'bg-white/50'} transition-colors" data-dot="${i}"></button>`).join('');
        // События
        document.getElementById('prevSlide')?.addEventListener('click', () => changeSlide(-1));
        document.getElementById('nextSlide')?.addEventListener('click', () => changeSlide(1));
        document.querySelectorAll('[data-dot]').forEach(btn => btn.addEventListener('click', (e) => changeSlide(parseInt(e.currentTarget.dataset.dot) - currentSlide)));
    }
    function changeSlide(delta) {
        currentSlide = (currentSlide + delta + heroSlides.length) % heroSlides.length;
        renderSlide(currentSlide);
        resetInterval();
    }
    function resetInterval() {
        if (slideInterval) clearInterval(slideInterval);
        slideInterval = setInterval(() => changeSlide(1), 5000);
    }
    renderSlide(0);
    resetInterval();
}



// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initHeroSlider();
    

    
    // Мобильное меню
    const mobileBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    }
    
    



    
});




// Обработка кликов по специальным ссылкам для навигации
document.addEventListener('DOMContentLoaded', () => {
    const userAgent = navigator.userAgent.toLowerCase();
    const isAndroid = /android/i.test(userAgent);
    const isIOS = /iphone|ipad|ipod/i.test(userAgent);

    const navLinks = document.querySelectorAll('a[data-device-ios][data-device-android]');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            let url = null;
            if (isAndroid) {
                url = link.getAttribute('data-device-android');
            } else if (isIOS) {
                url = link.getAttribute('data-device-ios');
            }

            if (url) {
                event.preventDefault(); // Отменяем стандартный переход по href
                window.location.href = url; // Перенаправляем на нужную схему
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            // Каждый раз заново получаем все карточки, которые сейчас на странице
            const currentCards = document.querySelectorAll('.product-card');
            currentCards.forEach(card => {
                const link = card.closest('a');
                const name = card.dataset.name || '';
                if (name.includes(query)) {
                    link.classList.remove('hidden');   // показываем ссылку
                    card.style.display = 'block';      // показываем карточку (можно оставить)
                } else {
                    link.classList.add('hidden');      // скрываем ссылку целиком
                    card.style.display = 'none';       // и карточку для надёжности
                }
            });
        });
    }
});




// каталог поисковый запрос
document.addEventListener('DOMContentLoaded', function() {
    // Элементы фильтров
    const applyBtn = document.getElementById('applyFilters');
    const categorySelect = document.getElementById('category');
    const priceMinInput = document.getElementById('priceMin');
    const priceMaxInput = document.getElementById('priceMax');
    const productGrid = document.getElementById('productGrid');

    // Функция для создания HTML-карточки товара
    function renderProductCard(p) {
        return `
            <a href="/product/${p.id}/" class="block">
                    <div class="product-card bg-white rounded-lg shadow-sm hover:shadow-lg transition overflow-hidden group" 
                        data-name="${p.name.toLowerCase()}" data-category="${p.category}">
                        <div class="aspect-square relative overflow-hidden bg-zinc-100">
                            <img src="${p.image}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-110 transition duration-300">
                            <div class="absolute top-4 right-4">
                                <span class="bg-white px-3 py-1 rounded-full text-sm font-semibold">${p.category}</span>
                            </div>
                        </div>
                        <div class="p-4">
                            <h3 class="font-semibold text-lg mb-2">${p.name}</h3>
                            <div class="flex items-center mb-3">
                                <span class="text-yellow-500">★</span>
                                <span class="ml-1 text-sm text-zinc-600">${p.rating}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-2xl font-bold">${p.price.toLocaleString()} ₽</span>
                                <button class="bg-zinc-900 hover:bg-zinc-800 text-white p-2 rounded-lg transition add-to-cart" data-id="${p.id}">
                                    <svg class="w-5 h-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <img src="/static/images/icons/shopping-cart-white.svg" alt="Корзина" class="w-6 h-6 text-zinc-700" />
                                    </svg>
                                </button>

                            </div>
                        </div>
                    </div>
                
            </a>

            
        `;
    }
    
    if (applyBtn) {
        applyBtn.addEventListener('click', function(e) {
            e.preventDefault();

            const category = categorySelect ? categorySelect.value : '';
            const priceMin = priceMinInput ? priceMinInput.value : '';
            const priceMax = priceMaxInput ? priceMaxInput.value : '';

            // Собираем URL с параметрами
            let url = '/catalog/filter/?';
            if (category) url += `category=${encodeURIComponent(category)}&`;
            if (priceMin) url += `price_min=${encodeURIComponent(priceMin)}&`;
            if (priceMax) url += `price_max=${encodeURIComponent(priceMax)}&`;

            // Отправляем AJAX-запрос
            fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(response => response.json())
            .then(data => {
                const products = data.products;
                if (products.length === 0) {
                    productGrid.innerHTML = '<p class="col-span-full text-center text-zinc-500">Товары не найдены</p>';
                } else {
                    let html = '';
                    products.forEach(p => {
                        html += renderProductCard(p);
                    });
                    productGrid.innerHTML = html;
                    if (searchInput) {
                        searchInput.dispatchEvent(new Event('input'));
                    }
                }
            })
            .catch(error => console.error('Ошибка при загрузке:', error));
        });
    }
});







// ---------- Lightbox (увеличенный просмотр) ----------
let lightboxImages = [];
let currentLightboxIndex = 0;

function openLightbox(images, index) {
    if (!images || images.length === 0) return;
    lightboxImages = images;
    currentLightboxIndex = index || 0;
    updateLightbox();
    document.getElementById('lightbox').classList.remove('hidden');
    document.body.style.overflow = 'hidden'; // отключаем прокрутку страницы
}

function closeLightbox(event) {
    // Закрываем только если клик на затемнение (или вызов без event)
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('lightbox').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function updateLightbox() {
    const img = document.getElementById('lightbox-img');
    img.src = lightboxImages[currentLightboxIndex] || '';
    // Обновляем точки
    const dotsContainer = document.getElementById('lightbox-dots');
    dotsContainer.innerHTML = lightboxImages.map((_, i) => 
        `<span class="w-3 h-3 rounded-full ${i === currentLightboxIndex ? 'bg-white' : 'bg-white/50'} transition-colors"></span>`
    ).join('');
    // Показываем/скрываем стрелки
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    if (lightboxImages.length > 1) {
        prevBtn.classList.remove('hidden');
        nextBtn.classList.remove('hidden');
    } else {
        prevBtn.classList.add('hidden');
        nextBtn.classList.add('hidden');
    }
}

function changeLightbox(delta) {
    if (lightboxImages.length === 0) return;
    currentLightboxIndex = (currentLightboxIndex + delta + lightboxImages.length) % lightboxImages.length;
    updateLightbox();
}

// Назначаем обработчики на стрелки (один раз)
document.addEventListener('DOMContentLoaded', function() {
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    if (prevBtn) prevBtn.addEventListener('click', function(e) { e.stopPropagation(); changeLightbox(-1); });
    if (nextBtn) nextBtn.addEventListener('click', function(e) { e.stopPropagation(); changeLightbox(1); });
});





// ========== Модальное окно заказа услуги ==========
(function() {
    // Функции открытия/закрытия (глобальные для вызова из onclick)
    window.openServiceModal = function() {
        const modal = document.getElementById('serviceOrderModal');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    };

    window.closeServiceModal = function(event) {
        if (event && event.target !== event.currentTarget) return;
        const modal = document.getElementById('serviceOrderModal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
            // Очищаем форму и скрытые поля
            const form = document.getElementById('serviceOrderForm');
            if (form) {
                form.reset();
                const hidden = form.querySelector('input[name="service_id"]');
                if (hidden) hidden.remove();
            }
        }
    };

    // Обработчик клика по кнопкам "Заказать услугу"
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.order-service-btn');
        if (btn) {
            e.preventDefault();
            const serviceId = btn.dataset.id;
            openServiceModal();
            // Добавляем скрытое поле с ID услуги в форму
            const form = document.getElementById('serviceOrderForm');
            if (form) {
                let hidden = form.querySelector('input[name="service_id"]');
                if (!hidden) {
                    hidden = document.createElement('input');
                    hidden.type = 'hidden';
                    hidden.name = 'service_id';
                    form.appendChild(hidden);
                }
                hidden.value = serviceId;
            }
        }
    });

    // Обработка отправки формы заказа услуги
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('serviceOrderForm');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                // Здесь можно отправить данные через AJAX, пока просто alert
                alert('Заявка отправлена! Мы свяжемся с вами.');
                closeServiceModal();
            });
        }
    });
})();







// ========== Вкладки на странице "Работы и изделия" ==========
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab-btn');
    const cards = document.querySelectorAll('.work-product-card');
    
    if (tabs.length && cards.length) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Убираем активный класс у всех вкладок
                tabs.forEach(t => t.classList.remove('active', 'bg-zinc-900', 'text-white'));
                tabs.forEach(t => t.classList.add('bg-zinc-200', 'text-zinc-700'));
                // Активируем текущую
                this.classList.add('active', 'bg-zinc-900', 'text-white');
                this.classList.remove('bg-zinc-200', 'text-zinc-700');

                const filter = this.dataset.tab;
                cards.forEach(card => {
                    if (filter === 'all') {
                        card.style.display = 'flex';
                    } else {
                        const type = card.dataset.type;
                        card.style.display = (type === filter) ? 'flex' : 'none';
                    }
                });
            });
        });
    }
});

// ========== Обработчик для кнопок "Заказать" на странице работ/изделий ==========
// У нас уже есть общий обработчик для .order-service-btn, который добавляет service_id и открывает модалку.
// Нужно только в этом обработчике также добавить data-type в скрытое поле.
// Модифицируем существующий обработчик (добавим проверку на наличие поля type).
// Поскольку мы уже объявили обработчик выше, лучше переопределить его, но для простоты добавим дополнительный код.

// Переопределяем обработчик, чтобы он работал и для этой страницы
document.addEventListener('click', function(e) {
    const btn = e.target.closest('.order-service-btn');
    if (btn) {
        e.preventDefault();
        const id = btn.dataset.id;
        const type = btn.dataset.type || 'service'; // если не указан, считаем услугой
        openServiceModal();
        const form = document.getElementById('serviceOrderForm');
        if (form) {
            // Удаляем старые скрытые поля
            form.querySelectorAll('input[name="item_id"], input[name="item_type"]').forEach(el => el.remove());
            // Добавляем новые
            const hiddenId = document.createElement('input');
            hiddenId.type = 'hidden';
            hiddenId.name = 'item_id';
            hiddenId.value = id;
            form.appendChild(hiddenId);

            const hiddenType = document.createElement('input');
            hiddenType.type = 'hidden';
            hiddenType.name = 'item_type';
            hiddenType.value = type;
            form.appendChild(hiddenType);
        }
    }
});

// Обработка отправки формы (уже есть, но обновим alert)
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('serviceOrderForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Собираем данные (можно будет потом отправить AJAX)
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            console.log('Заказ:', data);
            alert('Заявка отправлена! Мы свяжемся с вами.');
            closeServiceModal();
        });
    }
});









// ========== Модальное окно для статей ==========
(function() {
    // Глобальные функции для вызова из onclick
    window.openArticleModal = function(title, content, meta) {
        const modal = document.getElementById('articleModal');
        if (!modal) return;
        document.getElementById('articleModalTitle').innerHTML = title;
        document.getElementById('articleModalContent').innerHTML = content;
        document.getElementById('articleModalMeta').innerHTML = meta;
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    window.closeArticleModal = function(event) {
        if (event && event.target !== event.currentTarget) return;
        const modal = document.getElementById('articleModal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    };

    // Обработчик клика по кнопкам "Читать далее"
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.read-more-btn');
        if (btn) {
            e.preventDefault();
            const articleId = btn.dataset.id;
            // Находим карточку статьи по ID (можно использовать data-атрибут на самой карточке, но проще найти через data-id кнопки)
            // Ищем родительскую карточку
            const card = btn.closest('.article-card');
            if (!card) return;
            // Извлекаем данные из карточки
            const title = card.querySelector('h3') ? card.querySelector('h3').innerText : '';
            // Ищем краткое описание, но для полного текста нужен отдельный источник — либо из data-атрибута, либо отдельный запрос.
            // Поскольку у нас все данные уже есть в шаблоне, мы можем сохранить контент в data-атрибуте кнопки или скрытом блоке.
            // Чтобы не усложнять, добавим скрытый div с полным текстом внутри карточки.
            // Но для простоты можно передать данные через атрибуты data-content и data-author.
            // Внесём изменения в шаблон: добавим data-content и data-meta.
            // Поскольку мы уже написали шаблон без этого, давайте немного его подправим.
            // Сейчас мы переделаем: добавим data-content и data-meta к кнопке.
            // Перепишем шаблон ниже.
        }
    });
})();






// ========== Модальное окно для статей ==========
(function() {
    window.openArticleModal = function(title, content, meta) {
        const modal = document.getElementById('articleModal');
        if (!modal) return;
        document.getElementById('articleModalTitle').textContent = title;
        document.getElementById('articleModalContent').innerHTML = content;
        document.getElementById('articleModalMeta').textContent = meta;
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    };

    window.closeArticleModal = function(event) {
        if (event && event.target !== event.currentTarget) return;
        const modal = document.getElementById('articleModal');
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    };

    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.read-more-btn');
        if (btn) {
            e.preventDefault();
            const title = btn.dataset.title;
            const content = btn.dataset.content;
            const meta = btn.dataset.meta;
            openArticleModal(title, content, meta);
        }
    });
})();












// ========== Корзина (localStorage) ==========
// Структура: массив объектов { id: number, quantity: number }

function getCart() {
    try {
        const raw = localStorage.getItem('cart');
        if (!raw) return [];
        const parsed = JSON.parse(raw);
        // Если это массив чисел (старый формат) — конвертируем
        if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'number') {
            const newCart = parsed.map(id => ({ id, quantity: 1 }));
            setCart(newCart);
            return newCart;
        }
        // Если это массив объектов — возвращаем как есть
        if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object' && 'id' in parsed[0]) {
            return parsed;
        }
        return [];
    } catch {
        return [];
    }
}

function setCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(productId) {
    let cart = getCart();
    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id: productId, quantity: 1 });
    }
    setCart(cart);
    showNotification('Товар добавлен в корзину');
}

function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    setCart(cart);
    if (document.getElementById('cartItems')) {
        renderCart();
    }
}

function changeQuantity(productId, delta) {
    let cart = getCart();
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity <= 0) {
        cart = cart.filter(it => it.id !== productId);
    }
    setCart(cart);
    if (document.getElementById('cartItems')) {
        renderCart();
    }
}

function updateCartCount() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.querySelector('.cart-count');
    if (badge) {
        if (totalItems > 0) {
            badge.textContent = totalItems;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }
}

function renderCart() {
    const container = document.getElementById('cartItems');
    if (!container) return;

    const cart = getCart();
    const allProducts = window.allProducts || [];
    
    const cartItems = cart.map(cartItem => {
        const product = allProducts.find(p => p.id === cartItem.id);
        return { ...cartItem, product };
    }).filter(item => item.product !== undefined);

    if (cartItems.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8">
                <p class="text-zinc-500 text-lg">Ваша корзина пуста</p>
                <a href="/catalog/" class="inline-block mt-4 bg-zinc-900 text-white px-6 py-2 rounded-lg hover:bg-zinc-800 transition">Перейти в каталог</a>
            </div>
        `;
        document.getElementById('cartTotal').textContent = '0 ₽';
        return;
    }

    let html = '<ul class="divide-y divide-zinc-200">';
    let total = 0;
    cartItems.forEach(item => {
        const p = item.product;
        const subtotal = p.price * item.quantity;
        total += subtotal;
        html += `
            <li class="py-4 flex flex-wrap items-center justify-between gap-2">
                <div class="flex items-center gap-4">
                    <img src="${p.image}" alt="${p.name}" class="w-16 h-16 object-cover rounded">
                    <div>
                        <h4 class="font-semibold">${p.name}</h4>
                        <p class="text-sm text-zinc-500">${p.category}</p>
                    </div>
                </div>
                <div class="flex items-center gap-4 flex-wrap">
                    <div class="flex items-center border border-zinc-300 rounded-lg overflow-hidden">
                        <button class="qty-btn px-2 py-1 hover:bg-zinc-100" data-id="${p.id}" data-delta="-1">−</button>
                        <span class="px-3 py-1 min-w-[2rem] text-center">${item.quantity}</span>
                        <button class="qty-btn px-2 py-1 hover:bg-zinc-100" data-id="${p.id}" data-delta="1">+</button>
                    </div>
                    <span class="text-lg font-bold">${subtotal.toLocaleString()} ₽</span>
                    <button class="remove-from-cart text-red-600 hover:text-red-800" data-id="${p.id}">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                        </svg>
                    </button>
                </div>
            </li>
        `;
    });
    html += '</ul>';
    container.innerHTML = html;
    document.getElementById('cartTotal').textContent = total.toLocaleString() + ' ₽';

    // Обработчики для кнопок изменения количества
    document.querySelectorAll('.qty-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const id = parseInt(this.dataset.id);
            const delta = parseInt(this.dataset.delta);
            changeQuantity(id, delta);
        });
    });

    // Обработчики удаления
    document.querySelectorAll('.remove-from-cart').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = parseInt(this.dataset.id);
            removeFromCart(id);
        });
    });
}

// ========== Обработчики событий ==========

// Добавление в корзину со страниц каталога и детальной
document.addEventListener('click', function(e) {
    const btn = e.target.closest('.add-to-cart');
    if (btn) {
        e.preventDefault();
        const productId = parseInt(btn.dataset.id);
        if (!isNaN(productId)) {
            addToCart(productId);
        }
    }
});

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function() {
    updateCartCount();
    if (document.getElementById('cartItems')) {
        renderCart();
    }
});