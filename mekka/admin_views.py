from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin import views as admin_views

admin_views.LoginView = csrf_exempt(staff_member_required(admin_views.LoginView))