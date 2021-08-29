from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from accounts.forms import CustomerLoginRegisterForm, CustomerCodeConfirmForm, CustomerPasswordForm
from accounts.models import Customer
from accounts.utils import check_expire_time
from django.contrib.auth import authenticate, login


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class CustomerLoginRegisterView(FormView):
    form_class = CustomerLoginRegisterForm
    template_name = 'accounts/login_register.html'
    success_url = reverse_lazy('accounts:code-confirm')

    def form_valid(self, form):
        try:
            customer = Customer.objects.get(phone_number=form.changed_data['phone_number'])
        except Customer.DoesNotExist:
            pass
        else:
            if customer.password:
                self.success_url = reverse_lazy('accounts:password-confirm')

        return super().form_valid(form)


class CustomerPhoneNumberConfirmView(FormView):
    form_class = CustomerCodeConfirmForm
    template_name = 'accounts/phone_number_confirm.html'
    success_url = reverse_lazy('accounts:profile')

    def dispatch(self, request, *args, **kwargs):
        check_expire_time(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phone_number = '98' + self.request.session['phone_number']
        form_code = int(form.changed_data['code'])
        session_code = self.request.get('code', None)

        if session_code:
            if session_code == form_code:
                Customer.objects.get_or_create(phone_number=phone_number)
                self.delete_confirm_code()
                customer = authenticate(phone_number=phone_number)
                if customer:
                    login(self.request, customer)
                    messages.info(self.request, 'Login success', 'success')
                    return super().form_valid(form)
                else:
                    return super().form_valid(form)

            else:
                messages.info(self.request, 'The code is incorrect!', 'danger')
                return redirect('accounts:code-confirm')
        else:
            messages.info(self.request, 'The code is invalid! Enter your phone number again', 'danger')
            return redirect('accounts:login-register')

    def delete_confirm_code(self):
        del self.request.session['code']


class CustomerPasswordConfirmView(FormView):
    form_class = CustomerPasswordForm
    template_name = 'accounts/password_confirm.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        phone_number = self.request.session['phone_number']
        password = form.changed_data['password']
        customer = authenticate(phone_number=phone_number, password=password)

        if customer:
            login(self.request, customer)
            messages.info(self.request, 'Login success', 'success')
            super().form_valid(form)

        else:
            messages.info(self.request, 'Your password is incorrect!', 'danger')
            return redirect('accounts:password-confirm')
