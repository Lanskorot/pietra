# main/context_processors.py
from .views import categoriesData

def categories_processor(request):
    return {'categories_menu': categoriesData}