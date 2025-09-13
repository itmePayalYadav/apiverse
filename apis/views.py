import json
import os
import ipaddress
from django.conf import settings
from core.utils import api_response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import FileResponse, HttpResponseRedirect

# ----------------------
# Base methods
# ----------------------
class BaseAPIView(APIView):
    """
    Base API view with common methods like request payload extraction.
    """
    def get_request_payload(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
        payload = {
            "method": request.method,
            "headers": dict(request.headers),
            "origin": ip,
            "url": request.build_absolute_uri(),
        }
        if request.method != "GET":
            payload["body"] = request.data
        return payload
        
# ----------------------
# HTTP Methods
# ----------------------
class GetRequestView(BaseAPIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        payload = self.get_request_payload(request)
        return api_response(
            success=True,
            message="GET request received",
            data=payload,
            status_code=status.HTTP_200_OK
        )

class PostRequestView(BaseAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        payload = self.get_request_payload(request)
        return api_response(
            success=True,
            message="POST request received.",
            data=payload,
            status_code=status.HTTP_201_CREATED
        )

class PutRequestView(BaseAPIView):
    permission_classes = [permissions.AllowAny]
    def put(self, request):
        payload = self.get_request_payload(request)
        return api_response(
            success=True,
            message="PUT request received.",
            data=payload,
            status_code=status.HTTP_200_OK
        )
        
class PatchRequestView(BaseAPIView):
    permission_classes = [permissions.AllowAny]
    def patch(self, request):
        payload = self.get_request_payload(request)
        return api_response(
            success=True,
            message="PATCH request received.",
            data=payload,
            status_code=status.HTTP_200_OK
        )
    
class DeleteRequestView(BaseAPIView):
    permission_classes = [permissions.AllowAny]
    def delete(self, request):
        payload = self.get_request_payload(request)
        return api_response(
            success=True,
            message="DELETE request received.",
            data=payload,
            status_code=status.HTTP_200_OK
        )

# ----------------------
# Status Codes
# ----------------------
class GetAllStatusCodesView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'status-codes.json')
        try:
            with open(json_path, 'r') as f:
                status_codes = json.load(f)
        except FileNotFoundError:
            return api_response(
                success=False,
                message="Status codes file not found",
                status_code=status.HTTP_404_NOT_FOUND
            )   
        return api_response(
            success=True,
            message="Status codes fetched.",
            data=status_codes,
            status_code=status.HTTP_200_OK
        )

class GetStatusCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, status_code):
        try:
            status_code = int(status_code)
        except ValueError:
            return api_response(
                success=False,
                message="Invalid status code format",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        json_path = os.path.join(settings.BASE_DIR, 'data', 'status-codes.json')
        try:
            with open(json_path, 'r') as f:
                status_codes = json.load(f)
        except FileNotFoundError:
            return api_response(
                success=False,
                message="Status codes file not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        category = f"{str(status_code)[0]}xx"
        if category not in status_codes or str(status_code) not in status_codes[category]:
            return api_response(
                success=False,
                message="Invalid status code",
                status_code=status.HTTP_404_NOT_FOUND
            )

        payload = status_codes[category][str(status_code)]
        conflicting_codes = [100, 102, 103, 204, 205, 304]

        message = f"{status_code}: {payload['phrase']}"

        response_status = status.HTTP_200_OK if status_code in conflicting_codes else status_code

        return api_response(
            success=True,
            message=message,
            status_code=response_status,
            data={**payload, "statusCode": status_code, "category": category}  
        )
    
# ----------------------
# Request Information
# ----------------------
class GetRequestHeadersView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        headers = dict(request.headers)
        message = "Request headers returned"
        return api_response(
            success=True,
            message=message,
            status_code=status.HTTP_200_OK,
            data={"headers": headers}
        )
    
class GetClientIPView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        try:
            ip_version = "IPv4" if ipaddress.ip_address(ip).version == 4 else "IPv6"
        except ValueError:
            ip_version = "Unknown"

        return api_response(
            success=True,
            message="IP information returned",
            status_code=status.HTTP_200_OK,
            data={"ip": ip, "ipv": ip_version}
        )

class GetUserAgentView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        return api_response(
            success=True,
            message="User agent returned",
            status_code=status.HTTP_200_OK,
            data={"userAgent": user_agent}
        )

class GetPathVariableView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, path_variable):
        return api_response(
            success=True,
            message="Path variable returned",
            status_code=status.HTTP_200_OK,
            data={"pathVariable": path_variable}
        )

class GetQueryParametersView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query_params = dict(request.GET)
        return api_response(
            success=True,
            message="Query parameters returned",
            status_code=status.HTTP_200_OK,
            data={"query_params": query_params}
        )

# ----------------------
# Cookies
# ----------------------
class GetCookiesView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return api_response(
            success=True,
            message="Cookies returned",
            status_code=status.HTTP_200_OK,
            data={"cookies": request.COOKIES}
        )

class SetCookieView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        cookie_object = request.data  

        response = api_response(
            success=True,
            message="Cookies set",
            status_code=status.HTTP_200_OK,
            data={"cookies": {**request.COOKIES, **cookie_object}}
        )

        for key, value in cookie_object.items():
            response.set_cookie(key, value)

        return response

class RemoveCookieView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def delete(self, request):
        cookie_key = request.GET.get("cookieKey")

        if not cookie_key:
            return api_response(
                success=False,
                message="Cookie key required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        response = api_response(
            success=True,
            message="Cookie removed",
            status_code=status.HTTP_200_OK,
            data={"cookies": {cookie_key: None}}
        )

        response.delete_cookie(cookie_key)

        return response

# ----------------------
# Redirect
# ----------------------
class RedirectToUrlView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        url = request.GET.get("url")
        if url:
            return HttpResponseRedirect(url)

        return api_response(
            success=False,
            message="URL parameter is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

# ----------------------
# Images
# ----------------------
class BaseImageView(APIView):
    content_type = "image/jpeg"
    filename = ""
    
    def get(self, request):
        try:
            path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'images', self.filename)
            return FileResponse(open(path, 'rb'), content_type=self.content_type)
        except FileNotFoundError:
            return api_response(
            success=False,
            message="URL parameter is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

class SendJPEGImageView(BaseImageView):
    permission_classes = [permissions.AllowAny]
    
    filename = "image.jpeg"
    content_type = "image/jpeg"


class SendJPGImageView(BaseImageView):
    permission_classes = [permissions.AllowAny]
    
    filename = "image.jpg"
    content_type = "image/jpg"


class SendPNGImageView(BaseImageView):
    permission_classes = [permissions.AllowAny]
    
    filename = "image.png"
    content_type = "image/png"


class SendWEBPImageView(BaseImageView):
    permission_classes = [permissions.AllowAny]
    
    filename = "image.webp"
    content_type = "image/webp"


class SendSVGImageView(BaseImageView):
    permission_classes = [permissions.AllowAny]
    
    filename = "image.svg"
    content_type = "image/svg+xml"