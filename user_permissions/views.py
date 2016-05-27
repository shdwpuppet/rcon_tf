from django.shortcuts import render
from django.views.generic import TemplateView
from server_controller.views import dashboard

# Create your views here.
def homepage(request):
    if request.user.is_authenticated():
        return dashboard(request)
    else:
        return render(request, template_name='login.html')
