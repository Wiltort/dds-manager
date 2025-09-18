from django.http import JsonResponse
from .models import SubCategory


def get_subcategories(request):
    """Получение подкатегорий для выбранной категории"""

    category_id = request.GET.get("category_id")
    print(category_id)
    if category_id:
        subcategories = SubCategory.objects.filter(category_id=category_id)
        data = [{"id": sub.id, "name": sub.name} for sub in subcategories]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
