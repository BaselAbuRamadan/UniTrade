from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from .models import Order
from item.models import Item
from django.db.models import Q


def order():
    return 0

@login_required
def order_create(request): #create a new order here | 在这里创建订单
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Item.objects.get(id=product_id, status='active')

            #check if is yours order
            if product.seller == request.user:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You cannot order yourself'
                })

            #创建订单
            #create
            order = Order.objects.create(
                buyer=request.user,
                seller=product.seller,
                product=product,
                price=product.price,
                status='paid',
                paid_at=timezone.now()
            )

            #更新状态为已售出
            #update status to 'sold'
            product.status = 'sold'
            product.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Purchase successful',
                'redirect_url': reverse('order:order_detail', args=[order.id])
            })

        except Item.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Item does not exist or has been sold'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })

def order_cancel():
    return 0

def order_status():
    return 0

def order_delete():
    return 0

@login_required
def order_list(request): #obtain all orders from both buyers and sellers of the user | 获取用户买卖双方的所有订单
    orders = Order.objects.filter(
        Q(buyer=request.user) | Q(seller=request.user)
    ).select_related('buyer', 'seller', 'product')

    return render(request, 'order/order_list.html', {
        'orders': orders
    })

def order_search():
    return 0

@login_required
def order_detail(request, order_id): #view order details here | 在这里查看订单详情
    order = get_object_or_404(Order, id=order_id)

    #检查权限
    #check permissions
    if order.customer != request.user and order.seller != request.user:
        return redirect('order:order_list')

    return render(request, 'order/order_detail.html', {
        'order': order
    })
