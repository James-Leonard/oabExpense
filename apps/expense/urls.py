from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.expense, name="expense"),
    path('add_expense', views.add_expense, name="add_expense"),
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    path('search-expense/', csrf_exempt(views.search_expense),
         name="search_expense"),

]
