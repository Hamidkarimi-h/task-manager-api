import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


@csrf_exempt
@login_required
def create_task(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    data = json.loads(request.body)

    task = Task.objects.create(
        user=request.user,
        title=data.get("title"),
        description=data.get("description")
    )

    return JsonResponse(
        {
            "id": task.id,
            "message": "Task created successfully"
        },
        status=201
    )

@login_required
def task_list(request):

    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    tasks = Task.objects.filter(
        user=request.user
    )

    data = []

    for task in tasks:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        })

    return JsonResponse(
        data,
        safe=False
    )
    
@csrf_exempt
@login_required
def update_task(request, task_id):

    if request.method != "PUT":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        task = Task.objects.get(
            id=task_id,
            user=request.user
        )
    except Task.DoesNotExist:
        return JsonResponse(
            {"error": "Task not found"},
            status=404
        )

    data = json.loads(request.body)

    task.title = data.get(
        "title",
        task.title
    )

    task.description = data.get(
        "description",
        task.description
    )

    task.is_done = data.get(
        "is_done",
        task.is_done
    )

    task.save()

    return JsonResponse(
        {"message": "Task updated"}
    )
    
@csrf_exempt
@login_required
def delete_task(request, task_id):

    if request.method != "DELETE":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    try:
        task = Task.objects.get(
            id=task_id,
            user=request.user
        )
    except Task.DoesNotExist:
        return JsonResponse(
            {"error": "Task not found"},
            status=404
        )

    task.delete()

    return JsonResponse(
        {"message": "Task deleted"}
    )
    
@csrf_exempt
def register(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405
        )

    data = json.loads(request.body)

    user = User.objects.create_user(
        username=data["username"],
        password=data["password"]
    )

    return JsonResponse(
        {
            "id": user.id,
            "message": "User created"
        },
        status=201
    )
    
@csrf_exempt
def user_login(request):

    data = json.loads(request.body)

    user = authenticate(
        username=data["username"],
        password=data["password"]
    )

    if not user:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=400
        )

    login(request, user)

    return JsonResponse(
        {"message": "Logged in"}
    )