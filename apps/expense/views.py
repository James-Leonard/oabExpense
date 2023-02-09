from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from apps.userpreferences.models import UserPreference


@login_required(login_url="/login/")
def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expensez = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expensez.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="/login/")
def expense(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency 
    except UserPreference.DoesNotExist:
        currency = None 

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expense/expense.html', context)


@login_required(login_url="/login/")
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expense/add_expense.html',  context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expense/add_expense.html',  context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expense/add_expense.html',  context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expense/add_expense.html',  context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expense')


@login_required(login_url="/login/")
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expense/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expense/edit-expense.html',  context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expense/edit-expense.html',  context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expense/edit-expense.html',  context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expense')


@login_required(login_url="/login/")
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Removed ')
    return redirect('expense')
