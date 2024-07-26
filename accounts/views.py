from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from ac.decorators import superuser_required
from .models import CustomUser
from .forms import UserForm
from django.utils.decorators import method_decorator





@method_decorator(superuser_required, name='dispatch')
class AddUserView(CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'accounts/add-user.html'
    success_url = reverse_lazy('home')
