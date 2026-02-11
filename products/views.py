from django.views import generic
from django.shortcuts import get_object_or_404, reverse, render, redirect
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.contrib import messages


from .models import Product, Comment
from .forms import CommentForm


class ProductListView(generic.ListView):
    # model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    # def get_queryset(self):
    #

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


def comment_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        body = request.POST.get('body')
        stars = request.POST.get('stars')
        
        if body and stars:
            Comment.objects.create(
                product=product,
                author=request.user,
                body=body,
                stars=stars
            )
            messages.success(request, 'نظر شما با موفقیت ثبت شد')
        else:
            messages.error(request, 'لطفاً همه فیلدها را پر کنید')
    
    return redirect('product_detail', pk=product_id)