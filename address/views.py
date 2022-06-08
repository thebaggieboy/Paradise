from django.shortcuts import render
from core.forms import CheckOutForm
from core.models import Order
from .models import BillingAddress
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class CheckOutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form':form
         }
        return render(self.request, 'paradise/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        context = {
            'form':form
         }
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                print('Form is valid')
                return redirect('paradise:checkout')
            else:
                print('form is invalid')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('paradise:checkout') 
        return render(self.request, 'paradise/checkout.html', context)