from .models import Todo
from core.utils import api_response
from .serializers import TodoSerializer
from rest_framework import generics, status, permissions
from django.shortcuts import get_object_or_404

# ----------------------
# List all todos / Create todo
# ----------------------
class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Todo.objects.all()
    
    def list(self, request, *args, **kwargs):
        todos = self.get_queryset()
        serializer = self.get_serializer(todos, many=True)
        return api_response(
            success=True,
            message="Todos retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Todo created successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED
        )
    
# ----------------------
# Retrieve / Update / Delete a todo
# ----------------------
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Todo.objects.all()
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        todo = self.get_object()
        serializer = self.get_serializer(todo)
        return api_response(
            success=True,
            message="Todo retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        todo = self.get_object()
        serializer = self.get_serializer(todo, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return api_response(
            success=True,
            message="Todo updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        todo = self.get_object()
        todo.delete()
        return api_response(
            success=True,
            message="Todo deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT
        )
        
# ----------------------
# Toggle Todo completion
# ----------------------
class TodoToggleStatusView(generics.GenericAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, id):
        todo = get_object_or_404(Todo, id=id)
        todo.completed = not todo.completed
        todo.save()
        serializer = self.get_serializer(todo)
        return api_response(
            success=True,
            message="Todo status toggled successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
        
        