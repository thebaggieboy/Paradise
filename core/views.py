from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from .models import Order, OrderProduct,  Product


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "core/Products/product_list.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class IndexView(TemplateView):
    template_name = 'core/index.html'

class MenuView(TemplateView):
    template_name = 'core/menu.html'

class ProductCreateView(CreateView, LoginRequiredMixin):
    template_name = 'core/Products/product_create.html'
    fields = ('name', 'picture', 'price', 'size', 'color', 'details')
    model = models.Product

class ProductListView(ListView):
    template_name = 'core/Products/product_list.html'
    model = models.Product
    context_object_name = 'products'

class ProductUpdateView(UpdateView, LoginRequiredMixin):
    fields = ('name', 'picture', 'price', 'size')
    template_name = 'core/Products/product_edit.html'
    model = models.Product

class ProductDeleteView(DeleteView, LoginRequiredMixin):
    template_name = 'core/Products/product_delete.html'
    model = models.Product
    success_url = reverse_lazy('paradise:detail')

class ProductDetailView(DetailView):
    template_name = 'core/Products/product_detail.html'
    model = models.Product

@login_required
def add_to_cart(request, slug):
    # get product
    product = get_object_or_404(Product, slug=slug)
    # get or create product order
    product_order, created = OrderProduct.objects.get_or_create(
        product=product,
        #user=request.user,
        ordered=False
        )
    # Query through Orders that have not been completed yet
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)

    # for Orders that has not been completed yet and exists
    if order_qs.exists():
        # get order
        order = order_qs[0]
        # check if the product order is in the order
        if order.products.filter(product__slug=product.slug).exists():
            # if product order is in order add to quantity of the product order
            product_order.quantity += 1
            # save the product order
            product_order.save()
            messages.info(request, f'{product_order.quantity} pcs of {product.name} is in your cart ', extra_tags='alert')
        else:
            messages.success(request, f'{product.name} was added to your cart', extra_tags='alert')
            order.products.add(product_order)

    else:
        messages.warning(request, 'You do not have an active order! ', extra_tags='alert')
        # create a new order 
        order_date = timezone.now()
        order = models.Order.objects.create(user=request.user, order_date=order_date)
        # add products to order
        order.products.add(product_order)
    return redirect('core:detail', slug=slug)

@login_required 
def remove_from_cart (request, slug):
    # get product
    product = get_object_or_404(models.Product, slug=slug)
 
    # Query through Orders that have not been completed yet
    order_qs = models.Order.objects.filter(
        user=request.user,
        ordered=False)

    # for Orders that has not been completed yet and exists
    if order_qs.exists():
        # get order
        order = order_qs[0]
        # check if the product order is in the order
        if order.products.filter(product__slug=product.slug).exists():
            product_order = models.OrderProduct.objects.filter(
                product=product,
                #user=request.user,
                ordered=False

            )[0]
            order.products.remove(product_order)
            messages.warning(request, f'{product.name} was removed from your cart')
        else:
            return redirect('core:remove-from-cart', slug=slug)

    else:
        messages.warning(request, 'You do not have an active order! ')
        return redirect('core:remove-from-cart', slug=slug)
    return redirect('core:detail', slug=slug)




class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = models.Order.objects.get(user=self.request.user, ordered=False)
            context = {'object':order}
            return render(self.request, 'core/Orders/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/') 


class CheckOut(CreateView):
    model = models.BillingAddress
    fields = ['street_address', 'city', 'state', 'zip', 'country']
    template_name = 'core/checkout.html'


def product_review(request, slug):
    return render(request, 'core/Products/product_detail.html')

class ProductReview(CreateView):
    model = models.Review
    fields = ['review']
    template_name = 'core/Products/product_detail.html'

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(models.Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False                                                   
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderProduct.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.warning(request, f"Product was updated ({order_item.quantity})")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")
