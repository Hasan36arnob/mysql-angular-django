from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
import json
from .models import Item, Project, Task, Comment, Membership, Tag

def index(request):
    return render(request, 'index.html')

def _user_json(u: User):
    return {'id': u.id, 'username': u.username, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email}

# ---------- Auth ----------
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body or "{}")
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is None:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        login(request, user)
        return JsonResponse({'ok': True, 'user': _user_json(user)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'ok': True})

@csrf_exempt
@require_http_methods(["GET"])
def me(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return JsonResponse({'user': None})
    return JsonResponse({'user': _user_json(user)})

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

@csrf_exempt
@require_http_methods(["GET"])
def projects(request):
    q = request.GET.get('q') or ''
    limit = int(request.GET.get('limit') or 20)
    offset = int(request.GET.get('offset') or 0)
    qs = Project.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    total = qs.count()
    data = [{
        'id': p.id, 'name': p.name, 'description': p.description,
        'created_at': p.created_at.isoformat(), 'updated_at': p.updated_at.isoformat(),
    } for p in qs.order_by('-created_at')[offset:offset+limit]]
    return JsonResponse({'results': data, 'total': total, 'offset': offset, 'limit': limit})

@csrf_exempt
@require_http_methods(["POST"])
def create_project(request):
    try:
        payload = json.loads(request.body or "{}")
        p = Project.objects.create(name=payload['name'], description=payload.get('description',''))
        return JsonResponse({'id': p.id, 'name': p.name, 'description': p.description,
                             'created_at': p.created_at.isoformat(), 'updated_at': p.updated_at.isoformat()}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def tasks(request, project_id):
    try:
        q = request.GET.get('q') or ''
        status = request.GET.get('status')
        priority = request.GET.get('priority')
        limit = int(request.GET.get('limit') or 20)
        offset = int(request.GET.get('offset') or 0)
        qs = Task.objects.filter(project_id=project_id)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if status:
            qs = qs.filter(status=status)
        if priority:
            qs = qs.filter(priority=priority)
        total = qs.count()
        data = [{
            'id': t.id, 'title': t.title, 'description': t.description, 'status': t.status,
            'priority': t.priority, 'due_date': t.due_date.isoformat() if t.due_date else None,
            'assignee_id': t.assignee_id, 'project_id': t.project_id,
            'tags': [tag.name for tag in t.tags.all()],
            'created_at': t.created_at.isoformat(), 'updated_at': t.updated_at.isoformat(),
        } for t in qs.order_by('-created_at')[offset:offset+limit]]
        return JsonResponse({'results': data, 'total': total, 'offset': offset, 'limit': limit})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_task(request, project_id):
    try:
        payload = json.loads(request.body or "{}")
        t = Task.objects.create(
            project_id=project_id,
            title=payload['title'],
            description=payload.get('description',''),
            status=payload.get('status','todo'),
            priority=payload.get('priority','medium'),
            due_date=payload.get('due_date') or None,
            assignee_id=payload.get('assignee_id') or None
        )
        names = payload.get('tags') or []
        if names:
            tags = [Tag.objects.get_or_create(name=n)[0] for n in names]
            t.tags.set(tags)
        return JsonResponse({'id': t.id}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_task(request, task_id):
    try:
        payload = json.loads(request.body or "{}")
        t = Task.objects.get(pk=task_id)
        for field in ['title','description','status','priority']:
            if field in payload:
                setattr(t, field, payload[field])
        if 'due_date' in payload:
            t.due_date = payload['due_date'] or None
        if 'assignee_id' in payload:
            t.assignee_id = payload['assignee_id'] or None
        t.save()
        if 'tags' in payload:
            names = payload.get('tags') or []
            tags = [Tag.objects.get_or_create(name=n)[0] for n in names]
            t.tags.set(tags)
        return JsonResponse({'ok': True})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_task(request, task_id):
    try:
        Task.objects.filter(pk=task_id).delete()
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def comments(request, task_id):
    try:
        qs = Comment.objects.filter(task_id=task_id).order_by('created_at')
        data = [{
            'id': c.id, 'author_id': c.author_id, 'body': c.body, 'created_at': c.created_at.isoformat()
        } for c in qs]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_comment(request, task_id):
    try:
        payload = json.loads(request.body or "{}")
        author_id = payload.get('author_id') or (request.user.id if request.user.is_authenticated else None)
        if not author_id:
            return JsonResponse({'error': 'author required'}, status=400)
        c = Comment.objects.create(task_id=task_id, author_id=author_id, body=payload['body'])
        return JsonResponse({'id': c.id, 'created_at': c.created_at.isoformat()}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
@require_http_methods(["PUT"])
def update_item(request, item_id):
    try:
        data = json.loads(request.body)
        item = Item.objects.get(pk=item_id)
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.save()
        return JsonResponse({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'created_at': item.created_at.isoformat()
        })
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_item(request, item_id):
    try:
        item = Item.objects.get(pk=item_id)
        item.delete()
        return JsonResponse({'ok': True})
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
