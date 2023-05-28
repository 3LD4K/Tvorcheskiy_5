from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views import View
from .models import Customer, Product, Installment
# на будущее если писать формы в html и утилиты
from .forms import InstallmentForm
from .utils import calculate_installments

class ProductListView(ListView):
    model = Product
    template_name = "myapp/product_list.html"
    context_object_name = "products"

class ProductDetailView(DetailView):
    model = Product
    template_name = "myapp/product_detail.html"
    context_object_name = "product"

class InstallmentView(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs["pk"])
        form = InstallmentForm()
        return render(request, "myapp/installment_form.html", {"product": product, "form": form})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs["pk"])
        form = InstallmentForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            term = form.cleaned_data["term"]


            customer, created = Customer.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )

            credit_amount = product.price * 0.75
            if credit_amount > 60000:
                return render(request, "myapp/credit_limit_error.html", {"product": product})

            # Calculate the installments
            installments = calculate_installments(credit_amount, term)

            # Create the installment payments
            for amount, due_date in installments:
                Installment.objects.create(
                    customer=customer,
                    product=product,
                    amount=amount,
                    due_date=due_date,
                )

            # Redirect to the success page
            return redirect("installment_success", pk=customer.pk)
        else:
            # Return the form with errors
            return render(request, "myapp/installment_form.html", {"product": product, "form": form})

class InstallmentSuccessView(DetailView):
    model = Customer
    template_name = "myapp/installment_success.html"
    context_object_name = "customer"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["installments"] = self.object.installment_set.all()
        return context
