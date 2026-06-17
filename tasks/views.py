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