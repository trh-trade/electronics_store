from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.db.models import Q
from .models import Product, Category
from .forms import OrderForm, ContactForm
import random

def index(request):
    # Получаем параметры из запроса
    search_query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    # Получаем все корневые категории (для меню)
    root_categories = Category.objects.filter(parent__isnull=True)
    
    # Начальный набор товаров
    products = Product.objects.all()
    
    # Фильтрация по категории (включая подкатегории)
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            # Получаем все подкатегории (включая текущую)
            categories = category.get_descendants(include_self=True)
            products = products.filter(category__in=categories)
        except Category.DoesNotExist:
            pass
    
    # Поиск по нескольким полям
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    context = {
        'root_categories': root_categories,
        'products': products,
        'search_query': search_query,
        'current_category_id': category_id,
    }
    return render(request, 'main/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            message = (
                f"Новый заказ: {product.name}\n"
                f"Имя: {form.cleaned_data['name']}\n"
                f"Телефон: {form.cleaned_data['phone']}\n"
                f"Email: {form.cleaned_data['email']}\n"
                f"Цена товара: {product.price} $\n"
                f"ID товара: {product.id}"
            )

            send_mail(
                subject=f"Новый заказ: {product.name}",
                message=message,
                from_email='trhtrade18@gmail.com',
                recipient_list=['trhtrade18@gmail.com'],
                fail_silently=False,
            )
    
    return render(request, 'main/product_detail.html', {
        'product': product,
        'form': form
    })

def about(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = (
                f"Новое сообщение от клиента\n"
                f"Имя: {form.cleaned_data['name2']}\n"
                f"Email: {form.cleaned_data['email2']}\n"
                f"Сообщение: {form.cleaned_data['message2']}\n"
            )

            send_mail(
                subject="Новое сообщение от клиента",
                message=message,
                from_email='trhtrade18@gmail.com',
                recipient_list=['trhtrade18@gmail.com'],
                fail_silently=False,
            )

            # Редирект с флагом
            return redirect('/about/?success=1')

    return render(request, 'main/about.html', {'form': form})



def product_list(request):
    query = request.GET.get('q')  # <-- правильный параметр
    category_id = request.GET.get('category')

    if query:
        # поиск — возвращаем все подходящие товары
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    elif category_id:
        # фильтрация по категории
        products = Product.objects.filter(category_id=category_id)
    else:
        # ни поиска, ни фильтра — 8 случайных товаров
        all_products = list(Product.objects.all())
        products = random.sample(all_products, min(len(all_products), 8))

    root_categories = Category.objects.filter(parent__isnull=True)

    return render(request, 'main/index.html', {
        'products': products,
        'search_query': query or '',
        'root_categories': root_categories,
    })


