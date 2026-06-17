from django.urls import path

from .views import (
    create_task,
    task_list,
    update_task,
    delete_task
)

urlpatterns = [
    path(
        "create/",
        create_task,
        name="create-task"
    ),

    path(
        "",
        task_list,
        name="task-list"
    ),

    path(
        "<int:task_id>/",
        update_task,
        name="update-task"
    ),

    path(
        "<int:task_id>/delete/",
        delete_task,
        name="delete-task"
    ),
]