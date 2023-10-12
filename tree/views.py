from django.shortcuts import render
from .models import Menu

def menu(request):
    menu_items = Menu.objects.all()
    current_url = request.path
    
    context = {
        'menu_items': menu_items,
        'current_url': current_url
    }
    return render(request, 'menu.html', context)

#  делаем запрос к модели Menu, получаем все элементы меню с помощью Menu.objects.all(). 
# Затем объявляем переменные menu_items и current_url, которые передаем в menu.html
# ну и рендерим все