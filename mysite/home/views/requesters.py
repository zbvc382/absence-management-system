from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from ..decorators import requester_required
from ..forms import RequestForm
from ..models import Request, Requester


User = get_user_model()


@method_decorator([login_required, requester_required], name='dispatch')
class RequesterHomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        requester_requests = Request.objects.filter(user=self.request.user)
        pending_requests = requester_requests.filter(status='Pending')
        is_pending = False

        if pending_requests.__len__() > 0:
            is_pending = True

        # TODO: Might need exception handling
        assigned_authoriser = Requester.objects.get(user=self.request.user)\
            .assigned_authoriser.user.get_full_name
        array = ['pdf', 'jpg', 'txt', 'docx']

        context = {'user': user, 'requester_requests': requester_requests,
                   'assigned_authoriser': assigned_authoriser, 'array': array,
                   'pending_requests': pending_requests.__len__(),
                   'is_pending': is_pending}

        return context


@method_decorator([login_required, requester_required], name='dispatch')
class RequesterRequestView(CreateView):
    template_name = 'request.html'
    form_class = RequestForm

    def get_context_data(self, **kwargs):
        context = super(RequesterRequestView, self).get_context_data(**kwargs)
        assigned_authoriser = Requester.objects.get(user=self.request.user)\
            .assigned_authoriser.user.get_full_name
        context['authoriser'] = assigned_authoriser

        return context

    def form_valid(self, form):
        o = form.save(commit=False)
        o.user = self.request.user
        o.save()
        messages.success(self.request, 'Absence request submitted successfully!')

        return redirect(reverse('home:home'))


@method_decorator([login_required, requester_required], name='dispatch')
class RequesterCheckView(UpdateView):
    model = Request
    fields = ['status']
    template_name = 'check.html'
    success_url = reverse_lazy('home:home')

    def get_context_data(self, **kwargs):
        context = super(RequesterCheckView, self).get_context_data(**kwargs)
        assigned_authoriser = Requester.objects.get(user=self.request.user)\
            .assigned_authoriser.user.get_full_name
        array = ['pdf', 'jpg', 'txt', 'docx']
        request_object = self.get_object()
        attachment = request_object.__str__()
        extension = attachment.split('.').pop()
        context['array'] = array
        context['extension'] = extension
        context['authoriser'] = assigned_authoriser

        return context
