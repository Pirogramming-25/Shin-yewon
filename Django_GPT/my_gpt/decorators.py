from urllib.parse import urlencode

from django.shortcuts import redirect


def model_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            query = urlencode({"next": request.path, "required": "1"})
            return redirect(f"/accounts/login/?{query}")
        return view_func(request, *args, **kwargs)
    return wrapper