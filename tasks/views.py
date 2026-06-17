import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Task


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