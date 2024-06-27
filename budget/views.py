from django.shortcuts import render,redirect, get_object_or_404
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .form import CustomUserCreationForm, CustomAuthenticationForm,IncomeForm
from .models import Income
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from .form import TransactionForm
from collections import defaultdict
from django.utils import timezone
import base64
# Create your views here.

@login_required
def index(request):
    
    transactions = Transaction.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    
    # Add a 'type' attribute to distinguish transactions and incomes
    transactions = [{'id': t.id ,'type': 'transaction', 'category': t.category, 'amount': t.amount, 'description': t.description, 'date': t.date} for t in transactions]
    ft = "PT5aaWFkQktM"
    inc = "TWFkZSBCeSBTYWxhaA=="
    incomes = [{'id': i.id ,'type': 'income', 'category': i.category, 'amount': i.amount, 'description': i.description, 'date': i.date} for i in incomes]
    try:
        ft = base64.b64decode(ft).decode('utf-8')
        inc = base64.b64decode(inc).decode('utf-8')



    except Exception as e:
        ft = "Salah"
        inc = "=> ZiadBKL"
    combined_list = sorted(transactions + incomes, key=lambda x: x['date'], reverse=True)
    
    context = {
        'combined_list': combined_list,
        'ft': ft,
        'inc':inc,
    }
    return render(request, 'home.html', context)


@login_required
def chart_view(request):
    return render(request, 'chart.html')  

def chart_data(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        # Fetch all transactions and incomes for the user
        transactions = Transaction.objects.filter(user=request.user).order_by('date')
        incomes = Income.objects.filter(user=request.user).order_by('date')

        # Aggregate transaction totals by month
        transaction_totals = defaultdict(float)
        for transaction in transactions:
            month_year = transaction.date.strftime('%Y-%m')
            transaction_totals[month_year] += float(transaction.amount)

        # Aggregate income totals by month
        income_totals = defaultdict(float)
        for income in incomes:
            month_year = income.date.strftime('%Y-%m')
            income_totals[month_year] += float(income.amount)

        # Prepare data for chart
        labels = sorted(set(transaction_totals.keys()).union(set(income_totals.keys())))
        transaction_data = [transaction_totals[label] for label in labels]
        income_data = [income_totals[label] for label in labels]

        # Prepare data to be sent as JSON response
        data = {
            'labels': labels,
            'transaction_totals': transaction_data,
            'income_totals': income_data,
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            user =request.user
            transaction = form.save(commit=False)
            transaction.user = user
            transaction.date = timezone.now()
            user.balance -= transaction.amount
            request.user.save()
            transaction.save()    
            return redirect('homepage')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.date = timezone.now()
            request.user.balance += income.amount
            request.user.save()
            income.save()
            return redirect('homepage')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})


def delete_item(request, item_id, item_type):
    try:
        if not request.user.is_authenticated:
            return redirect('login')
        if item_type == 'transaction':
            item = get_object_or_404(Transaction, pk=item_id, user=request.user)
            request.user.balance += item.amount
        elif item_type == 'income':
            item = get_object_or_404(Income, pk=item_id, user=request.user)
            request.user.balance -= item.amount 
        else:
            raise ValueError("Invalid item type")
        request.user.save()
        item.delete()

    except Exception as e:
        print(f'Error deleting item: {str(e)}')

    return redirect('homepage')