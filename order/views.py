from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def order():
    return 0

def order_create():
    return 0

def order_cancel():
    return 0

def order_status():
    return 0

def order_delete():
    return 0

def item_list():
    return 0

def item_search():
    return 0

@login_required
def my_order():
    return 0