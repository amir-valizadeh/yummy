from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView, DetailView, DeleteView, ListView

from accounts.utils import IsServiceProvider
from item.forms import ItemCreateForm, ItemUpdateForm
from item.models import Item, ItemLine
from service.models import Service, ServiceCategory


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ItemCreateView(IsServiceProvider, FormView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/create_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs['service'] = get_object_or_404(Service, id=self.kwargs['service_pk'])
        self.kwargs['category'] = get_object_or_404(ServiceCategory, id=self.kwargs['category_pk'])

    def form_valid(self, form):
        item = form.save(commit=False)
        item.service = self.kwargs['service']
        item.category = self.kwargs['category']
        ItemLine.objects.create(item=item, quantity=form.cleaned_data['quantity'])
        item.save()
        return super().form_valid(form)

    def test_func(self):
        result = super().test_func()
        service_check = self.kwargs['service'].service_provider == self.request.user
        category_check = self.kwargs['category'].service == self.kwargs['service']
        return result and service_check and category_check


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ItemUpdateView(IsServiceProvider, UpdateView):
    model = Item
    template_name = 'item/update_form.html'
    form_class = ItemUpdateForm

    def get_initial(self):
        initial = super().get_initial()
        initial['quantity'] = self.get_object().stock
        return initial

    def get_form_class(self):
        form = super().get_form_class()
        queryset = form.base_fields['category'].queryset
        form.base_fields['category'].queryset = queryset.filter(service=self.get_object().service)
        return form

    def form_valid(self, form):
        item = form.save(commit=False)
        item.line.quantity = form.cleaned_data['quantity']
        item.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def test_func(self):
        result = super().test_func()
        return result and self.get_object().service.service_provider == self.request.user


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item/detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return Item.objects.available()


@method_decorator(login_required(login_url=reverse_lazy('accounts:service-provider-login')), name='dispatch')
class ItemDeleteView(IsServiceProvider, DeleteView):
    model = Item
    template_name = 'item/delete.html'
    success_url = reverse_lazy('accounts:service-provider-profile')

    def test_func(self):
        result = super().test_func()
        return result and self.get_object().service.service_provider == self.request.user


class BaseItemListView(ListView):
    model = Item
    context_object_name = 'items'


class ServiceItemListView(BaseItemListView):
    template_name = 'item/service_item_list.html'

    def get_queryset(self):
        return Item.objects.available().filter(service_id=self.kwargs['pk'])
