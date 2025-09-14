from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404
from .models import Todo
from .serializers import TodoSerializer
from core.utils import api_response

# ----------------------
# List Todos
# ----------------------
class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(deleted_at__isnull=True).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        todos = self.get_queryset()
        serializer = self.get_serializer(todos, many=True)
        return api_response(
            success=True,
            message="Todos retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Create Todo
# ----------------------
class TodoCreateView(generics.CreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            success=True,
            message="Todo created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )


# ----------------------
# Retrieve Todo
# ----------------------
class TodoRetrieveView(generics.RetrieveAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(deleted_at__isnull=True)

    def retrieve(self, request, *args, **kwargs):
        todo = get_object_or_404(self.get_queryset(), pk=kwargs["id"])
        return api_response(
            success=True,
            message="Todo retrieved successfully",
            data=self.get_serializer(todo).data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Update Todo
# ----------------------
class TodoUpdateView(generics.UpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(deleted_at__isnull=True)

    def update(self, request, *args, **kwargs):
        todo = get_object_or_404(self.get_queryset(), pk=kwargs["id"])
        serializer = self.get_serializer(todo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Todo updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Delete Todo (Soft Delete)
# ----------------------
class TodoDeleteView(generics.DestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(deleted_at__isnull=True)

    def destroy(self, request, *args, **kwargs):
        todo = get_object_or_404(self.get_queryset(), pk=kwargs["id"])
        todo.soft_delete()
        return api_response(
            success=True,
            message="Todo deleted successfully",
            status_code=status.HTTP_200_OK
        )


# ----------------------
# Toggle status
# ----------------------
class TodoToggleStatusView(generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, id=kwargs["id"], deleted_at__isnull=True)
        todo.completed = not todo.completed
        todo.save(update_fields=["completed"])
        response = {"id": todo.id, "completed": todo.completed}
        return api_response(
            success=True,
            message="Todo status toggled",
            data=response,
            status_code=status.HTTP_200_OK
        )
