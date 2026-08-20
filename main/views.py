# main/views.py
import json

from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from .forms import RegistrationForm
from .utils import send_order_to_telegram, send_order_to_email


categoriesData = [
    { 'name': 'Химия', 'icon': 'images/icons/flask-conical.svg', 'image': 'https://images.unsplash.com/photo-1583912267550-d974311a9a6e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fEx1YnJpY2FudHMlMjBjaGVtaXN0cnl8ZW58MHx8MHx8fDA%3D' },
    { 'name': 'Алмазный инструмент', 'icon': 'images/icons/gem.svg', 'image': 'https://images.unsplash.com/photo-1576115081906-b15927fb959e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGRpYW1vbmQlMjB0b29sfGVufDB8fDB8fHww' },
    { 'name': 'Абразивный инструмент', 'icon': 'images/icons/gavel.svg', 'image': 'https://plus.unsplash.com/premium_photo-1663127162791-ef922fd1ab89?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8dGhlJTIwYWJyYXNpdmUlMjB0b29sfGVufDB8fDB8fHww' },
    { 'name': 'Твердосплавный инструмент', 'icon': 'images/icons/hammer.svg', 'image': 'https://images.unsplash.com/photo-1759059228251-273b42bbcaf1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600' },
    { 'name': 'Вспомогательный инструмент', 'icon': 'images/icons/wrench.svg', 'image': 'https://images.unsplash.com/photo-1679240219409-51901fb6d2db?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=600' },
    { 'name': 'Электроинструмент', 'icon': 'images/icons/drill.svg', 'image': 'https://images.unsplash.com/photo-1518709414768-a88981a4515d?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fEVsZWN0b3JhbCUyMHRvb2xzfGVufDB8fDB8fHww' }
]


allProducts = [
    { 'id': 1, 'name': 'Набор резцов по камню', 'price': 4500, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1679240219409-51901fb6d2db?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Химия' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'},
    { 'id': 2, 'name': 'Профессиональный молоток', 'price': 2800, 'rating': 4.9, 'image': 'https://images.unsplash.com/reserve/oIpwxeeSPy1cnwYpqJ1w_Dufer%20Collateral%20test.jpg?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Алмазный инструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.' },
    { 'id': 3, 'name': 'Угловая шлифмашина', 'price': 8900, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1518709414768-a88981a4515d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Абразивный инструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'},
    { 'id': 4, 'name': 'Набор буров по камню', 'price': 3200, 'rating': 4.6, 'image': 'https://images.unsplash.com/photo-1606676539940-12768ce0e762?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Твердосплавный инструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'},
    { 'id': 5, 'name': 'Стамески для резьбы', 'price': 5500, 'rating': 4.9, 'image': 'https://images.unsplash.com/photo-1722836723721-917eb3ba14d7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Вспомогательный инструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'},
    { 'id': 6, 'name': 'Гранитный блок', 'price': 12000, 'rating': 4.5, 'image': 'https://images.unsplash.com/photo-1759059228251-273b42bbcaf1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Электроинструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'},
    { 'id': 7, 'name': 'Мраморная плита', 'price': 15000, 'rating': 4.8, 'image': 'https://images.unsplash.com/photo-1551554781-c46200ea959d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Электроинструмент',
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.' },
    { 'id': 8, 'name': 'Набор для полировки', 'price': 6700, 'rating': 4.7, 'image': 'https://images.unsplash.com/photo-1426927308491-6380b6a9936f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&w=400', 'category': 'Электроинструмент' ,
        'description': 'Набор высококачественных резцов для ручной обработки природного и искусственного камня. Подходит для гравировки, контурной резьбы и создания мелких деталей. Твёрдосплавные наконечники обеспечивают долгий срок службы.'}
]






# Услуги (для страницы услуг)
servicesData = [
    {
        'id': 1,
        'name': 'Художественная резьба по камню',
        'description': 'Ручная резьба по мрамору, граниту и песчанику. Создание барельефов, скульптур, архитектурных деталей любой сложности.',
        'price': 5000,          # цена за кв. метр или за час работы
        'image': 'https://media.istockphoto.com/id/491295408/photo/crafts.webp?a=1&b=1&s=612x612&w=0&k=20&c=1kpPPNBugEgB_iHE9zcJwLXRtnciB3N_uY4ZAGxfHv8=',
        'category': 'Резьба',
        'rating': 4.9
    },
    {
        'id': 2,
        'name': 'Полировка и шлифовка поверхности',
        'description': 'Восстановление и полировка каменных поверхностей до зеркального блеска. Удаление царапин, сколов, потёртостей.',
        'price': 2500,
        'image': 'https://media.istockphoto.com/id/1396150916/photo/master-grinds-and-polished-granite.webp?a=1&b=1&s=612x612&w=0&k=20&c=PsvDWFdaW2wh_ijxZGmzk_c9oFKVOHnBQC7IipSZl-g=',
        'category': 'Обработка',
        'rating': 4.7
    },
    {
        'id': 3,
        'name': 'Гравировка на камне (лазерная и ручная)',
        'description': 'Нанесение надписей, логотипов, портретов и орнаментов. Подходит для памятников, сувениров, интерьерных панно.',
        'price': 3000,
        'image': 'https://images.unsplash.com/photo-1558607433-8749229ef272?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8JUQwJTkzJUQxJTgwJUQwJUIwJUQwJUIyJUQwJUI4JUQxJTgwJUQwJUJFJUQwJUIyJUQwJUJBJUQwJUIwJTIwJUQwJUJEJUQwJUIwJTIwJUQwJUJBJUQwJUIwJUQwJUJDJUQwJUJEJUQwJUI1JTIwKCVEMCVCQiVEMCVCMCVEMCVCNyVEMCVCNSVEMSU4MCVEMCVCRCVEMCVCMCVEMSU4RiUyMCVEMCVCOCUyMCVEMSU4MCVEMSU4MyVEMSU4NyVEMCVCRCVEMCVCMCVEMSU4Ril8ZW58MHx8MHx8fDA%3D',
        'category': 'Гравировка',
        'rating': 4.8
    },
    {
        'id': 4,
        'name': 'Изготовление столешниц и подоконников',
        'description': 'Индивидуальное изготовление столешниц из натурального и искусственного камня по вашим размерам. Раскрой, обработка кромки, монтаж.',
        'price': 12000,
        'image': 'https://plus.unsplash.com/premium_photo-1674815329718-e1967af880f3?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8JUQwJTk4JUQwJUI3JUQwJUIzJUQwJUJFJUQxJTgyJUQwJUJFJUQwJUIyJUQwJUJCJUQwJUI1JUQwJUJEJUQwJUI4JUQwJUI1JTIwJUQxJTgxJUQxJTgyJUQwJUJFJUQwJUJCJUQwJUI1JUQxJTg4JUQwJUJEJUQwJUI4JUQxJTg2JTIwJUQwJUI4JTIwJUQwJUJGJUQwJUJFJUQwJUI0JUQwJUJFJUQwJUJBJUQwJUJFJUQwJUJEJUQwJUJEJUQwJUI4JUQwJUJBJUQwJUJFJUQwJUIyJTIwJUQwJUI4JUQwJUI3JTIwJUQwJUJBJUQwJUIwJUQwJUJDJUQwJUJEJUQxJThGfGVufDB8fDB8fHww',
        'category': 'Изделия',
        'rating': 4.6
    },
    {
        'id': 5,
        'name': 'Реставрация каменных изделий',
        'description': 'Восстановление старых памятников, колонн, лестниц. Заполнение сколов, склеивание трещин, тонировка под цвет камня.',
        'price': 7000,
        'image': 'https://plus.unsplash.com/premium_photo-1672287579489-4e92e57de92a?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8JUQwJUEwJUQwJUI1JUQxJTgxJUQxJTgyJUQwJUIwJUQwJUIyJUQxJTgwJUQwJUIwJUQxJTg2JUQwJUI4JUQxJThGJTIwJUQwJUJBJUQwJUIwJUQwJUJDJUQwJUI1JUQwJUJEJUQwJUJEJUQxJThCJUQxJTg1JTIwJUQwJUI4JUQwJUI3JUQwJUI0JUQwJUI1JUQwJUJCJUQwJUI4JUQwJUI5fGVufDB8fDB8fHww',
        'category': 'Реставрация',
        'rating': 4.9
    },
    {
        'id': 6,
        'name': 'Алмазное бурение отверстий',
        'description': 'Бурение отверстий любого диаметра в граните, мраморе, бетоне без сколов и трещин. Для коммуникаций, анкеров, декора.',
        'price': 1500,
        'image': 'https://media.istockphoto.com/id/1392217602/photo/drilling-holes-in-concrete-floor-or-ceiling-with-drill-rig-and-drill-bit.webp?a=1&b=1&s=612x612&w=0&k=20&c=Do-Nwxsvh-rEJ_ufBhWjNfv-9hL-gtVvTa1EFuffsRY=',
        'category': 'Бурение',
        'rating': 4.5
    },
    {
        'id': 7,
        'name': 'Химическая защита камня (гидрофобизация)',
        'description': 'Нанесение защитных составов для отталкивания влаги, грязи и масел. Увеличивает срок службы и облегчает уход.',
        'price': 4000,
        'image': 'https://images.unsplash.com/photo-1677003644492-8b056076cfcf?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8JUQwJUE1JUQwJUI4JUQwJUJDJUQwJUI4JUQxJTg3JUQwJUI1JUQxJTgxJUQwJUJBJUQwJUIwJUQxJThGJTIwJUQwJUI3JUQwJUIwJUQxJTg5JUQwJUI4JUQxJTgyJUQwJUIwJTIwJUQwJUJBJUQwJUIwJUQwJUJDJUQwJUJEJUQxJThGJTIwKCVEMCVCMyVEMCVCOCVEMCVCNCVEMSU4MCVEMCVCRSVEMSU4NCVEMCVCRSVEMCVCMSVEMCVCOCVEMCVCNyVEMCVCMCVEMSU4NiVEMCVCOCVEMSU4Ril8ZW58MHx8MHx8fDA%3D',
        'category': 'Защита',
        'rating': 4.7
    },
    {
        'id': 8,
        'name': 'Консультация и замеры на объекте',
        'description': 'Выезд специалиста для замеров, оценки состояния камня, подбора технологии и материалов. Бесплатно при заказе услуги.',
        'price': 0,             # бесплатно
        'image': 'https://media.istockphoto.com/id/2258227067/photo/building-inspectors-checking-water-softener-digital-display-in-unfinished-residential-basement.webp?a=1&b=1&s=612x612&w=0&k=20&c=0C4DTdI0WU13O1kiuwhSe-AMBwx5GbMfaHeM1JNmhbE=',
        'category': 'Консультация',
        'rating': 5.0
    }
]



# Работы и изделия из камня
works_products_data = [
    {
        'id': 1,
        'name': 'Мраморная столешница с фаской',
        'description': 'Изготовление столешницы из натурального мрамора с фаской и полировкой. Размеры под заказ. Отличное решение для кухни или ванной.',
        'price': 25000,
        'image': 'https://media.istockphoto.com/id/2197624461/photo/fragment-of-a-polished-marble-window-sill.webp?a=1&b=1&s=612x612&w=0&k=20&c=dCRPT7Xgtsln1d1Yxm3dcz2VXHS_VW5snHtiWa6avC4=',
        'category': 'Изделия',
        'rating': 4.9,
        'is_product': True,  # флаг, что это изделие
    },
    {
        'id': 2,
        'name': 'Реставрация мраморной колонны',
        'description': 'Восстановление исторической колонны из мрамора: заполнение трещин, шлифовка, полировка, тонировка. Работа выполнена в срок.',
        'price': 18000,
        'image': 'https://plus.unsplash.com/premium_photo-1668032803389-3a05947140a8?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8JUQwJUEwJUQwJUI1JUQxJTgxJUQxJTgyJUQwJUIwJUQwJUIyJUQxJTgwJUQwJUIwJUQxJTg2JUQwJUI4JUQxJThGJTIwJUQwJUJDJUQxJTgwJUQwJUIwJUQwJUJDJUQwJUJFJUQxJTgwJUQwJUJEJUQwJUJFJUQwJUI5JTIwJUQwJUJBJUQwJUJFJUQwJUJCJUQwJUJFJUQwJUJEJUQwJUJEJUQxJThCfGVufDB8fDB8fHww',
        'category': 'Реставрация',
        'rating': 4.8,
        'is_product': False,
    },
    {
        'id': 3,
        'name': 'Гранитный памятник с портретом',
        'description': 'Изготовление памятника из гранита с лазерной гравировкой портрета. Размер 120x80 см, полировка, цоколь.',
        'price': 35000,
        'image': 'https://plus.unsplash.com/premium_photo-1742457641093-bdc52d3a1169?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8JUQwJTkzJUQxJTgwJUQwJUIwJUQwJUJEJUQwJUI4JUQxJTgyJUQwJUJEJUQxJThCJUQwJUI5JTIwJUQwJUJGJUQwJUIwJUQwJUJDJUQxJThGJUQxJTgyJUQwJUJEJUQwJUI4JUQwJUJBJTIwJUQxJTgxJTIwJUQwJUJGJUQwJUJFJUQxJTgwJUQxJTgyJUQxJTgwJUQwJUI1JUQxJTgyJUQwJUJFJUQwJUJDfGVufDB8fDB8fHww',
        'category': 'Изделия',
        'rating': 4.7,
        'is_product': True,
    },
    {
        'id': 4,
        'name': 'Художественная резьба на песчанике',
        'description': 'Ручная резьба по песчанику: создание барельефа с растительным орнаментом для фасада здания. Работа выполнена мастером-камнерезом.',
        'price': 12000,
        'image': 'https://media.istockphoto.com/id/1320987915/photo/scene-of-archaeological-remains-from-the-arab-period-preserved-in-a-glass-urn-hand-carved.webp?a=1&b=1&s=612x612&w=0&k=20&c=pbjofTTbnl_FpwTia4CO7V2-bJKVDGz1HjmogxfB_Os=',
        'category': 'Резьба',
        'rating': 4.9,
        'is_product': False,
    },
    {
        'id': 5,
        'name': 'Подоконник из искусственного камня',
        'description': 'Изготовление подоконника из композитного материала с имитацией мрамора. Выдерживает перепады температур, не боится влаги.',
        'price': 8500,
        'image': 'https://media.istockphoto.com/id/2216888323/photo/this-elegant-marble-window-sill-features-natural-patterns-that-enhance-its-appeal.webp?a=1&b=1&s=612x612&w=0&k=20&c=_H-iHz2gdIrjc25Y2e91_-iBU8HoziouGYwhlRSm0jg=',
        'category': 'Изделия',
        'rating': 4.6,
        'is_product': True,
    },
    {
        'id': 6,
        'name': 'Алмазное бурение под коммуникации',
        'description': 'Выполнение отверстий в гранитной плите для прокладки труб и кабелей. Диаметр 50 мм, глубина до 200 мм.',
        'price': 5000,
        'image': 'https://media.istockphoto.com/id/512405186/photo/diamond-drilling-machine.webp?a=1&b=1&s=612x612&w=0&k=20&c=fBmAZiBCWxKMcYTD-5PFia-raINUBJpvxmjWgr2mDjM=',
        'category': 'Работы',
        'rating': 4.5,
        'is_product': False,
    },
    {
        'id': 7,
        'name': 'Скульптура "Лев" из мрамора',
        'description': 'Изготовление декоративной скульптуры льва из мрамора для парка. Высота 150 см, ручная обработка, полировка до зеркального блеска.',
        'price': 45000,
        'image': 'https://media.istockphoto.com/id/1332231607/photo/white-lion-statue.webp?a=1&b=1&s=612x612&w=0&k=20&c=ZyHtzrS586B13_viJqczO-nQY8wEiGFrHHikDuCQ83o=',
        'category': 'Изделия',
        'rating': 4.9,
        'is_product': True,
    },
    {
        'id': 8,
        'name': 'Гидрофобизация мраморного пола',
        'description': 'Нанесение защитного состава на мраморный пол в вестибюле. Защита от пятен, облегчение уборки, сохранение цвета.',
        'price': 7000,
        'image': 'https://images.unsplash.com/photo-1588606805498-5c212783a722?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8JUQwJTkzJUQwJUI4JUQwJUI0JUQxJTgwJUQwJUJFJUQxJTg0JUQwJUJFJUQwJUIxJUQwJUI4JUQwJUI3JUQwJUIwJUQxJTg2JUQwJUI4JUQxJThGJTIwJUQwJUJDJUQxJTgwJUQwJUIwJUQwJUJDJUQwJUJFJUQxJTgwJUQwJUJEJUQwJUJFJUQwJUIzJUQwJUJFJTIwJUQwJUJGJUQwJUJFJUQwJUJCJUQwJUIwfGVufDB8fDB8fHww',
        'category': 'Защита',
        'rating': 4.7,
        'is_product': False,
    }
]



# Статьи (с полным текстом)
articles_data = [
    {
        'id': 1,
        'title': 'Как выбрать алмазный инструмент для гранита',
        'short_description': 'Подробный гид по выбору алмазных дисков, фрез и канатов для обработки гранита. Советы по зернистости, связке и режимам работы.',
        'content': """
            <p>Выбор правильного алмазного инструмента для обработки гранита — ключевой фактор для достижения высокой производительности и качества поверхности. В этой статье мы разберем основные параметры, на которые стоит обратить внимание.</p>
            <p>Первое, что нужно учесть — тип связки. Для гранита лучше всего подходят инструменты с металлической связкой, которая обеспечивает высокую износостойкость. Также важна зернистость: для черновой обработки используют более крупное зерно (30-50), для чистовой — мелкое (100-200).</p>
            <p>Не забывайте о режиме охлаждения: при работе с гранитом обязательно используйте водяное охлаждение, чтобы предотвратить перегрев и выкрашивание.</p>
            <p>В итоге, правильный выбор инструмента значительно увеличит срок его службы и улучшит качество обработки. Рекомендуем консультироваться с нашими специалистами.</p>
        """,
        'image': 'https://images.unsplash.com/photo-1576115081906-b15927fb959e?w=600&auto=format&fit=crop&q=60',
        'date': '2026-06-20',
        'category': 'Советы',
        'author': 'Алексей Петров',
        'views': 1250,
        'is_featured': True,
    },
    {
        'id': 2,
        'title': 'Технология полировки мрамора до зеркального блеска',
        'short_description': 'Пошаговая инструкция по полировке мраморных поверхностей. Используемые материалы, инструменты и секреты профессионалов.',
        'content': """
            <p>Полировка мрамора — это процесс, требующий терпения и правильного подхода. В этой статье мы расскажем, как добиться зеркального блеска в домашних условиях.</p>
            <p>Сначала необходимо выполнить шлифовку с использованием абразивных кругов разной зернистости — от 50 до 3000. Затем переходим к полировке с применением специальных паст и войлочных кругов.</p>
            <p>Важно помнить, что мрамор — мягкий камень, поэтому не стоит сильно давить на инструмент. Лучше делать несколько проходов с малой нагрузкой.</p>
            <p>Завершающий этап — нанесение защитного воска или гидрофобизатора для сохранения блеска на долгое время.</p>
        """,
        'image': 'https://media.istockphoto.com/id/1164586291/photo/carpenter-polishes-the-surface-of-the-facade-before-assembling-furniture-on-a-blurred.webp?a=1&b=1&s=612x612&w=0&k=20&c=qi46k4k4gwBUnMl7mSLxD0Gq147cBzZCwauhXC0xd-E=',
        'date': '2026-06-15',
        'category': 'Технологии',
        'author': 'Иван Смирнов',
        'views': 890,
        'is_featured': False,
    },
    {
        'id': 3,
        'title': 'Реставрация старых каменных памятников: методы и материалы',
        'short_description': 'Обзор современных методов реставрации: заполнение трещин, укрепление структуры, тонировка и защита от выветривания.',
        'content': """
            <p>Реставрация старых памятников — сложная задача, требующая знаний химии, материаловедения и истории. В этой статье мы рассмотрим основные этапы и материалы.</p>
            <p>Первый шаг — очистка поверхности от загрязнений, мхов и солей. Используются специальные растворы и мягкие щётки. Затем проводится укрепление структуры с помощью инъекций.</p>
            <p>Заключительный этап — тонировка и нанесение защитного гидрофобного слоя. Важно подобрать состав, максимально приближенный к оригинальному цвету.</p>
            <p>Реставрация памятников — это не только работа, но и сохранение истории. Доверяйте её только профессионалам.</p>
        """,
        'image': 'https://media.istockphoto.com/id/1189995887/photo/restorer-and-framer-laboratory-craftswomen-restoring-antique-religious-painting-canvas.webp?a=1&b=1&s=612x612&w=0&k=20&c=JmNqIJ-23yps_5XDtLnF5wB1NxeY1rw5kWr7w-KDCS0=',
        'date': '2026-06-10',
        'category': 'Реставрация',
        'author': 'Мария Кузнецова',
        'views': 1560,
        'is_featured': False,
    }
]

def home(request):
    return render(request, 'main/index.html', {'active_menu': 'home',
                                               'categories': categoriesData,
                                               'popular_product': allProducts[:4]})


def filter_products(request):
    category = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    filtered = allProducts[:]  # копируем список

    if category:
        filtered = [p for p in filtered if p['category'] == category]

    if price_min:
        try:
            price_min = int(price_min)
            filtered = [p for p in filtered if p['price'] >= price_min]
        except (ValueError, TypeError):
            pass

    if price_max:
        try:
            price_max = int(price_max)
            filtered = [p for p in filtered if p['price'] <= price_max]
        except (ValueError, TypeError):
            pass

    return JsonResponse({'products': filtered})


def about(request):
    return render(request, 'main/about_us.html')

def catalog(request):
    category = request.GET.get('category')
    products = allProducts[:]          # копия всех товаров
    selected_category = None
    if category:
        products = [p for p in products if p['category'] == category]
        selected_category = category
    return render(request, 'main/catalog.html', {
        'product': products,
        'categories': categoriesData,
        'selected_category': selected_category, 
    })

def contact(request):
    return render(request, 'main/contact.html')


def stone_works_and_products(request):
    # Используем данные, объявленные выше (works_products_data)
    return render(request, 'main/stone_works_and_products.html', {
        'works_products': works_products_data,
    })



def articles(request):
    return render(request, 'main/articles.html', {
        'articles': articles_data,
    })



class ProductDetailView(DetailView):
    template_name = 'main/product_detail.html'
    context_object_name = 'product'   # чтобы в шаблоне была переменная product
    

    def get_object(self, queryset=None):
        # Получаем id из URL
        product_id = self.kwargs.get('pk')
        # Ищем товар в списке (позже здесь будет запрос к БД)
        product = next((p for p in allProducts if p['id'] == product_id), None)
        if product is None:
            raise Http404("Товар не найден")
        return product
    
    
def services(request):
    return render(request, 'main/services.html', {
        'services': servicesData
    })
    
    
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:profile')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})




@login_required
def profile(request):
    return render(request, 'main/profile.html', {
        'all_products': allProducts,
    })
    
    
    
@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            products_data = data.get('products', [])
            order_items = []
            total_price = 0
            for item in products_data:
                pid = item.get('id')
                qty = item.get('quantity', 1)
                product = next((p for p in allProducts if p['id'] == pid), None)
                if product:
                    subtotal = product['price'] * qty
                    order_items.append({
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['price'],
                        'quantity': qty,
                        'subtotal': subtotal
                    })
                    total_price += subtotal
            # Сохраняем заказ в сессию до получения телефона
            request.session['order_data'] = {
                'username': request.user.username,
                'email': request.user.email,
                'items': order_items,
                'total': total_price,
            }
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)

# @login_required
# def update_order_phone(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             phone = data.get('phone', '')
#             order_data = request.session.get('order_data')
#             if not order_data:
#                 return JsonResponse({'status': 'error', 'message': 'Нет данных заказа'}, status=400)
#             order_data['phone'] = phone
#             # Отправляем в Telegram
#             success = send_order_to_telegram(order_data)
#             success_email = send_order_to_email(order_data)
#             request.session.pop('order_data', None)
#             if success or success_email:
#                 return JsonResponse({'status': 'ok'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Не удалось отправить в Telegram'}, status=500)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)




import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def update_order_phone(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Метод не разрешён'}, status=405)

    try:
        body = request.body.decode('utf-8')
        data = json.loads(body)
        phone = data.get('phone', '')

        order_data = request.session.get('order_data')
        send_order_to_telegram(order_data)
        if not order_data:
            logger.error("order_data not found in session")
            return JsonResponse({'status': 'error', 'message': 'Нет данных заказа'}, status=400)

        order_data['phone'] = phone

        # Формируем текст письма
        subject = f"Новый заказ от PIETRA"
        text_message = f"""
Пользователь: {order_data['username']}
Email: {order_data['email']}
Телефон: {phone}
Список товаров:
"""
        total = 0
        for item in order_data['items']:
            text_message += f"  {item['name']} x {item['quantity']} = {item['subtotal']} ₽\n"
            total += item['subtotal']
        text_message += f"\nИтого: {total} ₽"

        # --- Отправка через SMTP с STARTTLS (порт 587) ---
        try:
            from_email = settings.EMAIL_HOST_USER
            recipients = list(set([settings.EMAIL_HOST_USER, settings.MY_EMAIL]))
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            msg.attach(MIMEText(text_message, 'plain', 'utf-8'))

            # Подключаемся к серверу
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)  # 587
            server.starttls()  # включаем шифрование
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_email, recipients, msg.as_string())
            server.quit()

            print("Письмо успешно отправлено через SMTP+STARTTLS")

        except Exception as email_error:
            logger.error(f"Ошибка при отправке письма: {email_error}")
            return JsonResponse({'status': 'error', 'message': f'Ошибка отправки письма: {str(email_error)}'}, status=400)

        # Очищаем сессию
        request.session.pop('order_data', None)
        return JsonResponse({'status': 'ok'})

    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return JsonResponse({'status': 'error', 'message': 'Неверный формат JSON'}, status=400)
    except Exception as e:
        logger.error(f"Общая ошибка в update_order_phone: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)