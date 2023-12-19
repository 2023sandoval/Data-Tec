from .forms import ContactoForm
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

#def get_form_kwargs 12-15 y def get_success_url  17-20 comentar si dan problemas
class ContactoUsuario(CreateView):
    template_name = 'contacto/contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('apps.contacto:contacto')

    # def get_form_kwargs(self):
    #   kwargs = super().get_form_kwargs()
    #   kwargs['request'] = self.request
    #   return kwargs

    def get_success_url(self):
        success_url = super().get_success_url()
        success_url += f'?id={self.object.id}'
        return success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['request'] = self.request
        return context

    def form_valid(self, form):
        self.object = form.save()
        self.form_send_email()
        messages.success(self.request, 'Consulta enviada.')
        return super().form_valid(form)

    def form_send_email(self):

        pass                                       

