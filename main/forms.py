from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent',
        'placeholder': 'example@mail.ru'
    }))
    
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent',
            'placeholder': 'Придумайте пароль'
        }),
        strip=False,
        help_text="",   # убираем подсказку
        validators=[]   # пустой список валидаторов — отключает все проверки
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent',
            'placeholder': 'Повторите пароль'
        }),
        strip=False,
        help_text=""
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Задаём классы для всех полей (чтобы не дублировать в каждом)
        base_attrs = {
            'class': 'w-full px-4 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent',
        }
        # Для username
        self.fields['username'].widget.attrs.update(base_attrs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        # Для password1
        self.fields['password1'].widget.attrs.update(base_attrs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        # Для password2
        self.fields['password2'].widget.attrs.update(base_attrs)
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        # Для email (уже задали выше, но можно переопределить)
        self.fields['email'].widget.attrs.update(base_attrs)
        
        
        
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_attrs = {
            'class': 'w-full px-4 py-2 border border-zinc-300 rounded-lg focus:ring-2 focus:ring-zinc-500 focus:border-transparent',
        }
        self.fields['username'].widget.attrs.update(base_attrs)
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['password'].widget.attrs.update(base_attrs)
        self.fields['password'].widget.attrs['placeholder'] = 'Пароль'