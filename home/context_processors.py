from django.conf import settings

def admin_check(request):
    return {
        'is_admin': request.user.is_authenticated and request.user.is_staff
    }