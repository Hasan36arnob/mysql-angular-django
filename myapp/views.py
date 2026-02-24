from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json
from .models import Item

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["GET"])
def item_list(request):
    items = Item.objects.all()
    data = [{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'created_at': item.created_at.isoformat()
    } for item in items]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def create_item(request):
    try:
        data = json.loads(request.body)
        item = Item.objects.create(
            name=data['name'],
            description=data['description']
        )
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'created_at': item.created_at.isoformat()
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)