from django.shortcuts import render
from .models import Food, Consume
# Create your views here.


def index(request):
    user = request.user

    if request.method == 'POST':
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()

    user_nutrition = get_user_nutrition(user)

    consumed_food = Consume.objects.filter(user=request.user)
    return render(request, 'foodapp/index.html', {"foods":foods, 'consumed_food':consumed_food,'total_protein':user_nutrition['proteins'], 'total_carbs':user_nutrition['carbs'], 'total_fats':user_nutrition['fats'],
                                                   'total_calories':user_nutrition['calories'], 'progress_percentage':user_nutrition['progress_percentage']})
def get_user_nutrition(user):
    consumed_foods = Consume.objects.filter(user=user)

    proteins = sum(food.food_consumed.protein for food in consumed_foods)
    carbs = sum(food.food_consumed.carbs for food in consumed_foods)
    fats = sum(food.food_consumed.fats for food in consumed_foods)
    calories = sum(food.food_consumed.calories for food in consumed_foods)

    progress_percentage = (calories / 2000) * 100

    return {
        "proteins": proteins,
        "carbs": carbs,
        "fats": fats,
        "calories": calories,
        "progress_percentage":progress_percentage,
    }
