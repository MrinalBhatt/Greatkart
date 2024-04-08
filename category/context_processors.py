from category.models import Category

def get_categories(request):
    categoreies = Category.objects.all()
    return {'categories' : categoreies }