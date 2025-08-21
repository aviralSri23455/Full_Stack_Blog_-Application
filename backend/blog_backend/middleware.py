"""
Performance monitoring middleware for better debugging
"""
import time
import logging

logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Start timing
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calculate response time
        process_time = time.time() - start_time
        
        # Log slow requests (over 1 second)
        if process_time > 1.0:
            logger.warning(f"Slow request: {request.path} took {process_time:.2f}s")
        
        # Add response time header for debugging
        response['X-Process-Time'] = str(process_time)
        
        return response
