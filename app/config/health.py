"""
Health check views for the Querido Diário Backend.
"""
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    """
    Health check endpoint for monitoring and load balancers.
    Returns 200 OK when the service is healthy.
    """
    
    def get(self, request, *args, **kwargs):
        """Handle GET requests to the health endpoint."""
        return JsonResponse({
            "status": "healthy",
            "service": "querido-diario-backend",
            "django_version": "4.0.3"
        })