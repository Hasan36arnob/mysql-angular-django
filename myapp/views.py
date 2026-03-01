from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, Avg
import json
from .models import Category, Product, CartItem, Order, OrderItem, Review

def index(request):
    return render(request, 'index.html')

# --- AUTH ---
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            login(request, user)
            return JsonResponse({'id': user.id, 'username': user.username})
        return JsonResponse({'error': 'Invalid username or password. Please try again.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during login.'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)
            
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'id': user.id, 'username': user.username})
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during registration.'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'ok': True})

def me_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'id': request.user.id, 'username': request.user.username})
    return JsonResponse({'error': 'Not logged in'}, status=401)

# --- STOREFRONT ---
def product_list(request):
    query = request.GET.get('q', '')
    cat_slug = request.GET.get('category', '')
    products = Product.objects.all()
    
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if cat_slug:
        products = products.filter(category__slug=cat_slug)
        
    data = [{
        'id': p.id,
        'name': p.name,
        'slug': p.slug,
        'price': str(p.price),
        'image_url': p.image_url,
        'category': p.category.name,
        'avg_rating': p.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    } for p in products]
    return JsonResponse(data, safe=False)

def product_detail(request, slug):
    p = get_object_or_404(Product, slug=slug)
    reviews = [{
        'user': r.user.username,
        'rating': r.rating,
        'comment': r.comment,
        'created_at': r.created_at.isoformat()
    } for r in p.reviews.all()]
    
    return JsonResponse({
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': str(p.price),
        'stock': p.stock,
        'image_url': p.image_url,
        'category': p.category.name,
        'reviews': reviews
    })

def category_list(request):
    categories = Category.objects.all()
    data = [{'name': c.name, 'slug': c.slug} for c in categories]
    return JsonResponse(data, safe=False)

# --- CART ---
@csrf_exempt
@require_http_methods(["GET", "POST"])
def cart_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Auth required'}, status=401)
        
    if request.method == "POST":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))
        qty = int(data.get('quantity', 1))
        
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if created:
            item.quantity = qty
        else:
            item.quantity += qty
        item.save()
        return JsonResponse({'ok': True})
        
    items = CartItem.objects.filter(user=request.user)
    data = [{
        'id': i.id,
        'product_id': i.product.id,
        'product_name': i.product.name,
        'price': str(i.product.price),
        'quantity': i.quantity,
        'image_url': i.product.image_url
    } for i in items]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["DELETE"])
def cart_remove(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Auth required'}, status=401)
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return JsonResponse({'ok': True})

@csrf_exempt
@require_http_methods(["PUT"])
def cart_update(request, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Auth required'}, status=401)
    
    data = json.loads(request.body)
    new_quantity = int(data.get('quantity', 1))
    
    if new_quantity <= 0:
        return JsonResponse({'error': 'Quantity must be positive'}, status=400)
        
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity = new_quantity
    item.save()
    
    return JsonResponse({'ok': True})

# --- ORDERS ---
@csrf_exempt
@require_http_methods(["POST"])
def checkout(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Auth required'}, status=401)
        
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return JsonResponse({'error': 'Cart is empty'}, status=400)
        
    total = sum(i.product.price * i.quantity for i in cart_items)
    order = Order.objects.create(user=request.user, total_price=total)
    
    for i in cart_items:
        OrderItem.objects.create(
            order=order,
            product=i.product,
            price=i.product.price,
            quantity=i.quantity
        )
        # Reduce stock
        i.product.stock -= i.quantity
        i.product.save()
        
    cart_items.delete()
    return JsonResponse({'order_id': order.id, 'total': str(total)})

def my_orders(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Auth required'}, status=401)
    orders = Order.objects.filter(user=request.user)
    data = [{
        'id': o.id,
        'total_price': str(o.total_price),
        'status': o.status,
        'created_at': o.created_at.isoformat(),
        'items': [{
            'name': i.product.name,
            'quantity': i.quantity,
            'price': str(i.price)
        } for i in o.items.all()]
    } for o in orders]
    return JsonResponse(data, safe=False)
