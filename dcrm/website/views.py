from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddRecordForm
from .models import Record

# 🔒 Secure Home View with Login Protection
@csrf_protect
def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both fields are required')
            return redirect('home')

        # 🔐 Prevent username enumeration attacks
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('home')

    return render(request, 'home.html', {'records': records})

# 🔒 Logout User Securely
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

# 🔒 Secure User Registration
@csrf_protect
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed. Please check your details.')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

# 🔒 Secure Customer Record Retrieval
@login_required
def customer_record(request, pk):
    customer_record = get_object_or_404(Record, id=pk)
    return render(request, 'record.html', {'customer_record': customer_record})

# 🔒 Secure Record Deletion
@login_required
def delete_record(request, pk):
    delete_it = get_object_or_404(Record, id=pk)
    
    if request.method == "POST":  # Ensure only POST requests can delete records
        delete_it.delete()
        messages.success(request, 'Record deleted successfully')
    else:
        messages.warning(request, 'Invalid request method')

    return redirect('home')

# 🔒 Secure Add Record Function
@login_required
@csrf_protect
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Record added")
            return redirect('home')
        else:
            messages.error(request, "Invalid data provided")

    return render(request, 'add_record.html', {'form': form})

# 🔒 Secure Update Record Function
@login_required
@csrf_protect
def update_record(request, pk):
    current_record = get_object_or_404(Record, id=pk)
    form = AddRecordForm(request.POST or None, instance=current_record)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Record has been updated")
        return redirect('home')

    return render(request, 'update_record.html', {'form': form})
