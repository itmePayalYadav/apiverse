from django.urls import path
from . import views

app_name = "kitchen_sink"

urlpatterns = [
    # ----------------------
    # HTTP Methods
    # ----------------------
    path('http-methods/get/', views.GetRequestView.as_view(), name='get-request'),
    path('http-methods/post/', views.PostRequestView.as_view(), name='post-request'),
    path('http-methods/put/', views.PutRequestView.as_view(), name='put-request'),
    path('http-methods/patch/', views.PatchRequestView.as_view(), name='patch-request'),
    path('http-methods/delete/', views.DeleteRequestView.as_view(), name='delete-request'),

    # ----------------------
    # Status Codes
    # ----------------------
    path('status-codes/', views.GetAllStatusCodesView.as_view(), name='get-all-status-codes'),
    path('status-codes/<int:status_code>/', views.GetStatusCodeView.as_view(), name='get-status-code'),

    # ----------------------
    # Request Information
    # ----------------------
    path('request/headers/', views.GetRequestHeadersView.as_view(), name='get-request-headers'),
    path('request/ip/', views.GetClientIPView.as_view(), name='get-client-ip'),
    path('request/user-agent/', views.GetUserAgentView.as_view(), name='get-user-agent'),
    path('request/path-variable/<str:path_variable>/', views.GetPathVariableView.as_view(), name='get-path-variable'),
    path('request/query-parameter/', views.GetQueryParametersView.as_view(), name='get-query-parameters'),

    # ----------------------
    # Cookies
    # ----------------------
    path('cookies/get/', views.GetCookiesView.as_view(), name='get-cookies'),
    path('cookies/set/', views.SetCookieView.as_view(), name='set-cookie'),
    path('cookies/remove/', views.RemoveCookieView.as_view(), name='remove-cookie'),

    # ----------------------
    # Redirect
    # ----------------------
    path('redirect/to/', views.RedirectToUrlView.as_view(), name='redirect'),

    # ----------------------
    # Images
    # ----------------------
    path('images/jpeg/', views.SendJPEGImageView.as_view(), name='send-jpeg-image'),
    path('images/jpg/', views.SendJPGImageView.as_view(), name='send-jpg-image'),
    path('images/png/', views.SendPNGImageView.as_view(), name='send-png-image'),
    path('images/webp/', views.SendWEBPImageView.as_view(), name='send-webp-image'),
    path('images/svg/', views.SendSVGImageView.as_view(), name='send-svg-image')
]
