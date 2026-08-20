import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string




def send_order_to_telegram(order_data):
    """Отправляет детали заказа в Telegram"""
    text = (
        f"🛒 *Новый заказ PIETRA STORE!*\n"
        f"*Пользователь:* {order_data.get('username', 'Неизвестно')}\n"
        f"*Email:* {order_data.get('email', 'Не указан')}\n"
        f"*Телефон:* {order_data.get('phone', 'Не указан')}\n"
        f"\n*Товары:*\n"
    )
    total = 0
    for item in order_data.get('items', []):
        text += f"  • {item['name']} x {item['quantity']} = {item['subtotal']} ₽\n"
        total += item['subtotal']
    text += f"\n*Итого:* {total} ₽"
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': settings.TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False
    
    
    
    


def send_order_to_email(order_data):
    """
    Отправляет детали заказа на почту администратора (EMAIL_HOST_USER).
    """
    # Получаем данные
    username = order_data.get('username', 'Неизвестно')
    email_user = order_data.get('email', 'Не указан')
    phone = order_data.get('phone', 'Не указан')
    items = order_data.get('items', [])
    total = order_data.get('total', 0)

    # Тема письма
    subject = f"🛒 Новый заказ от {username}"

    # Формируем plain text (на случай, если почтовый клиент не поддерживает HTML)
    text_lines = [
        f"Новый заказ от {username}",
        f"Email: {email_user}",
        f"Телефон: {phone}",
        "",
        "Товары:",
    ]
    for item in items:
        text_lines.append(f"  • {item['name']} x {item['quantity']} = {item['subtotal']} ₽")
    text_lines.append("")
    text_lines.append(f"Итого: {total} ₽")
    text_message = "\n".join(text_lines)

    html_message = render_to_string('order_email.html', {
        'username': username,
        'email': email_user,
        'phone': phone,
        'items': items,
        'total': total,
    })

    # Отправляем письмо
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.EMAIL_HOST_USER,  # отправитель (ваш ящик)
        to=[settings.EMAIL_HOST_USER, 'Lanskorot@yandex.ru'],       
    )
    email.attach_alternative(html_message, "text/html")

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False