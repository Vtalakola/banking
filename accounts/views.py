from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Transaction

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')

@login_required
def dashboard(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        account = Account.objects.create(user=request.user, balance=0)
    
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'accounts/dashboard.html', {'account': account, 'transactions': transactions})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        account = Account.objects.get(user=request.user)
        account.balance += float(amount)
        account.save()
        Transaction.objects.create(account=account, description='Deposit', amount=amount)
        return redirect('dashboard')
    return render(request, 'accounts/deposit.html')

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        account = Account.objects.get(user=request.user)
        if account.balance >= float(amount):
            account.balance -= float(amount)
            account.save()
            Transaction.objects.create(account=account, description='Withdraw', amount=amount)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/withdraw.html', {'error': 'Insufficient balance'})
    return render(request, 'accounts/withdraw.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user, balance=0)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

