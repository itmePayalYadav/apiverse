from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/todos/", include(("todos.urls", "todos"), namespace="todos")),
    path("api/v1/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/v1/social-media/", include(("socials.urls", "socials"), namespace="socials")),
    path("api/v1/kitchen-sink/", include(("apis.urls", "kitchen_sink"), namespace="kitchen_sink")),
]
