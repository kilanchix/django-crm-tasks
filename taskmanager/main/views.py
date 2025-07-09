from django.contrib.auth.decorators import login_required

# Профиль пользователя: история выполненных сделок только для клиента, связанного с этим пользователем
@login_required(login_url='/login/')
def profile(request):
    from .models import Deal, Client
    user = request.user
    # Поиск клиента по email пользователя (или доработать под вашу логику связи)
    client = Client.objects.filter(email=user.email).first()
    deals = []
    completed_count = 0
    if client:
        deals = Deal.objects.filter(client=client, status='closed').order_by('-created')
        completed_count = deals.count()
    return render(request, 'main/profile.html', {'client': client, 'deals': deals, 'completed_count': completed_count})

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Task, Client, Deal

# Авторизация (только логин)
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:index')
        else:
            return render(request, 'main/login.html', {"error": "Неверный логин или пароль"})
    return render(request, 'main/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('main:login')

# Задачи
@login_required
def index(request):
    tasks = Task.objects.all().order_by('-created')
    return render(request, 'main/index.html', {'tasks': tasks})

@login_required
@require_POST
def add_task(request):
    title = request.POST.get('title')
    if title:
        Task.objects.create(title=title)
    return redirect('main:index')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('main:index')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('main:index')

# Клиенты
@login_required
def clients(request):
    query = request.GET.get('q', '').strip()
    clients = Client.objects.all()
    if query:
        clients = clients.filter(name__icontains=query)
    clients = clients.order_by('-created')
    return render(request, 'main/clients.html', {'clients': clients, 'q': query})





@login_required
@require_http_methods(["POST"])
def delete_client(request, client_id):
    Client.objects.filter(id=client_id).delete()
    return redirect('main:clients')

# Сделки
@login_required
def deals(request):
    status = request.GET.get('status', '').strip()
    query = request.GET.get('q', '').strip()
    deals = Deal.objects.select_related('client').all()
    clients = Client.objects.all()
    if query:
        deals = deals.filter(title__icontains=query)
    if status:
        deals = deals.filter(status=status)
    deals = deals.order_by('-created')
    completed_count = deals.filter(status='closed').count()
    import json
    from django.utils.safestring import mark_safe
    clients_json = mark_safe(json.dumps(list(clients.values('id', 'name'))))
    return render(request, 'main/deals.html', {
        'deals': deals,
        'q': query,
        'status': status,
        'completed_count': completed_count,
        'clients': clients,
        'clients_json': clients_json
    })


# Добавление сделки (через обычную форму)
from django.views.decorators.csrf import csrf_protect
@login_required
@require_http_methods(["POST"])
@csrf_protect
def add_deal(request):
    title = request.POST.get('title')
    amount = request.POST.get('amount')
    status = request.POST.get('status')
    client_id = request.POST.get('client')
    currency = request.POST.get('currency', '₽')
    if title and client_id:
        try:
            client = Client.objects.get(id=client_id)
            # Сохраняем валюту в поле extra (если нет поля currency в модели)
            deal = Deal.objects.create(title=title, amount=amount or 0, status=status, client=client)
            if hasattr(deal, 'currency'):
                deal.currency = currency
                deal.save()
            else:
                # Если нет поля currency, можно добавить его в модель или игнорировать
                pass
        except Client.DoesNotExist:
            pass
    return redirect('main:deals')





@login_required
@require_http_methods(["POST"])
def delete_deal(request, deal_id):
    Deal.objects.filter(id=deal_id).delete()
    return redirect('main:deals')

# Редактирование сделки
@login_required
@require_http_methods(["POST"])
@csrf_protect
def edit_deal(request, deal_id):
    from .models import Deal, Client
    deal = get_object_or_404(Deal, id=deal_id)
    title = request.POST.get('title')
    amount = request.POST.get('amount')
    status = request.POST.get('status')
    client_id = request.POST.get('client')
    currency = request.POST.get('currency', '₽')
    if title and client_id:
        try:
            client = Client.objects.get(id=client_id)
            deal.title = title
            deal.amount = amount or 0
            deal.status = status
            deal.client = client
            deal.currency = currency
            deal.save()
        except Client.DoesNotExist:
            pass
    return redirect('main:deals')
