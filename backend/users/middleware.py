from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Get the last activity timestamp from the session
        last_activity_str = request.session.get('last_activity')

        if last_activity_str:
            # Convert the string back to a datetime object
            last_activity = now().fromisoformat(last_activity_str)

            # Calculate inactivity duration (in seconds)
            elapsed_time = (now() - last_activity).total_seconds()

            # Check if the elapsed time is greater than the timeout threshold (e.g., 600 seconds = 10 minutes)
            if elapsed_time > settings.AUTO_LOGOUT_TIME:
                logout(request)  # Automatically log the user out
                return redirect('reviews:home')  # Redirect to homepage after logout

        # Update the last activity timestamp (store as an ISO 8601 string)
        request.session['last_activity'] = now().isoformat()

        return self.get_response(request)
