from django.http import Http404
from django.shortcuts import render, redirect

from main.dummy_data import PRODUCTS

# Create your views here.

# Simulate database (in-memory list)
products_store = PRODUCTS.copy()
next_id = max(p['id'] for p in products_store) + 1

def products(request):
    return render(request, 'products.html', {'products': products_store})


def index(request):
    return render(request, 'index.html')


def create(request):
    global next_id
    if request.method == 'POST':
        new_product = {
            "id": next_id,
            "name": request.POST['name'],
            "price": request.POST['price'],
            "description": request.POST['description'],
            "image": request.POST['image']
        }
        products_store.append(new_product)
        next_id += 1
        return redirect('products')
    return render(request, 'create.html')

def update(request, product_id):
    product = next((p for p in products_store if p['id'] == product_id), None)
    if not product:
        raise Http404("Product not found")

    if request.method == 'POST':
        product['name'] = request.POST['name']
        product['price'] = request.POST['price']
        product['description'] = request.POST['description']
        product['image'] = request.POST['image']
        return redirect('products')

    return render(request, 'update.html', {'product': product})

def delete(request, product_id):
    global products_store
    products_store = [p for p in products_store if p['id'] != product_id]
    return redirect('products')