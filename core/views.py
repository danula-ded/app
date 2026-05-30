from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .exam_config import APP_TEXT, PRODUCT_RELATIONS, PRODUCT_SEARCH_FIELDS, PRODUCT_SORTS
from .forms import OrderForm, ProductForm
from .models import Order, Product, Supplier
from .permissions import is_admin, is_manager_or_admin


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "login"

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, APP_TEXT["admin_only"])
            return redirect("product_list")

        return super().handle_no_permission()


class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "login"

    def test_func(self):
        return is_manager_or_admin(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, APP_TEXT["orders_forbidden"])
            return redirect("product_list")

        return super().handle_no_permission()


class UserLoginView(LoginView):
    template_name = "core/login.html"


class ProductListView(ListView):
    model = Product
    template_name = "core/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        products = Product.objects.select_related(*PRODUCT_RELATIONS)

        if not is_manager_or_admin(self.request.user):
            return products.order_by("id")

        query = self.request.GET.get("q", "").strip()
        supplier_id = self.request.GET.get("supplier", "")
        sort = self.request.GET.get("sort", "")

        if query:
            search_filter = Q()

            for field in PRODUCT_SEARCH_FIELDS:
                search_filter |= Q(**{f"{field}__icontains": query})

            products = products.filter(search_filter)

        if supplier_id.isdigit():
            products = products.filter(supplier_id=supplier_id)

        if sort in PRODUCT_SORTS:
            return products.order_by(*PRODUCT_SORTS[sort])

        return products.order_by("id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["suppliers"] = Supplier.objects.order_by("name")
        context["can_use_product_tools"] = is_manager_or_admin(self.request.user)
        context["can_manage_products"] = is_admin(self.request.user)
        context["can_view_orders"] = is_manager_or_admin(self.request.user)
        context["selected_supplier"] = self.request.GET.get("supplier", "")
        context["selected_sort"] = self.request.GET.get("sort", "")
        context["query"] = self.request.GET.get("q", "")
        return context


class ProductCreateView(AdminRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "core/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        messages.success(self.request, APP_TEXT["item_added"])
        return super().form_valid(form)


class ProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "core/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        messages.success(self.request, APP_TEXT["item_updated"])
        return super().form_valid(form)


class ProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "core/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, APP_TEXT["item_delete_blocked"])
            return redirect("product_list")

        messages.success(self.request, APP_TEXT["item_deleted"])
        return response


class OrderListView(ManagerRequiredMixin, ListView):
    model = Order
    template_name = "core/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.select_related("status", "pickup_point", "user")
            .prefetch_related("items__product")
            .order_by("-id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage_orders"] = is_admin(self.request.user)
        return context


class OrderCreateView(AdminRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "core/order_form.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form):
        messages.success(self.request, APP_TEXT["order_added"])
        return super().form_valid(form)


class OrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "core/order_form.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form):
        messages.success(self.request, APP_TEXT["order_updated"])
        return super().form_valid(form)


class OrderDeleteView(AdminRequiredMixin, DeleteView):
    model = Order
    template_name = "core/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")

    def form_valid(self, form):
        messages.success(self.request, APP_TEXT["order_deleted"])
        return super().form_valid(form)
