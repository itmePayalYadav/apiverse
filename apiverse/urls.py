from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    
    path("api/v1/todos/", include(("todos.urls", "todos"), namespace="todos")),
    path("api/v1/accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("api/v1/social-media/", include(("socials.urls", "socials"), namespace="socials")),
    path("api/v1/kitchen-sink/", include(("apis.urls", "kitchen_sink"), namespace="kitchen_sink")),
]
