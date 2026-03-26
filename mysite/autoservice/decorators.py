from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Informacija bus pasiekiama po prisijungimo.")
        return login_required(view_func)(request, *args, **kwargs)
    return wrapper
