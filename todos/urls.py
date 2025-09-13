from django.urls import path
from .views import (
    TodoListCreateView,
    TodoDetailView,
    TodoToggleStatusView,
)

app_name = "todos"

urlpatterns = [
    path("", TodoListCreateView.as_view(), name="list-create-todo"),
    path("<int:id>/", TodoDetailView.as_view(), name="todo-detail"),
    path("<int:id>/toggle/", TodoToggleStatusView.as_view(), name="todo-toggle-status"),
]