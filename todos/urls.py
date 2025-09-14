from django.urls import path
from .views import (
    TodoListView,
    TodoCreateView,
    TodoRetrieveView,
    TodoUpdateView,
    TodoDeleteView,
    TodoToggleStatusView,
)

app_name = "todos"

urlpatterns = [
    path("", TodoListView.as_view(), name="todo-list"),
    path("create/", TodoCreateView.as_view(), name="todo-create"),
    path("<uuid:id>/", TodoRetrieveView.as_view(), name="todo-retrieve"),
    path("<uuid:id>/update/", TodoUpdateView.as_view(), name="todo-update"),
    path("<uuid:id>/delete/", TodoDeleteView.as_view(), name="todo-delete"),
    path("<uuid:id>/toggle/", TodoToggleStatusView.as_view(), name="todo-toggle"),
]