from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib import messages
from django.db.models import Q, F

from django.contrib.auth.decorators import login_required

from .models import Flight, Order, Ticket

from .filters import FlightFilter
from .forms import FlightForm, MyForm
from .decorators import unauthenticated_user


# Create your views here.


# from .forms import OrderForm, CreateUserForm
# from .filters import OrderFilter

@unauthenticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was create for ' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username OR password is incorrect')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        print('Hello')
        return redirect('manage')
    context = {}
    flight = Flight.objects.all()
    myFilter = FlightFilter(request.GET, queryset=flight)
    flight = myFilter.qs
    context['flight'] = flight
    context['myFilter'] = myFilter
    # 加载航班信息

    return render(request, 'accounts/index.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def buy(request, cid, fid):
    if cid != request.user.id:
        return redirect('error')
    flight = Flight.objects.get(id=fid)
    purchased = flight.purchased
    user = User.objects.get(id=cid)
    order = Order.objects.filter(flight=flight).filter(customer=user)
    print(order)
    if request.method == "POST":
        # todo: 添加一条订单消息
        # 查询该用户是否购买该航班
        order = Order(customer=user, flight=flight, status='未支付')
        flight.purchased = purchased + 1
        flight.save()
        order.save()
        return redirect('home')

    context = {'flight': flight, 'order': order}
    return render(request, 'accounts/buy.html', context)


def orders(request, cid):
    if cid != request.user.id:
        return redirect('error')
    user = User.objects.get(id=cid)
    orders = Order.objects.filter(customer=user)

    context = {'orders': orders}
    return render(request, 'accounts/orders.html', context)


def cancel(request, cid, oid):
    if cid != request.user.id:
        return redirect('error')
    order = Order.objects.get(id=oid)
    flight = Flight.objects.get(id=order.flight.id)
    purchased = flight.purchased
    context = {'order': order}
    if request.method == 'POST':
        # 删除订单  航班购买-1
        flight.purchased = purchased - 1
        flight.save()
        order.delete()
        return redirect('orders', cid=cid)
    return render(request, 'accounts/cancel.html', context)


def pay(request, cid, oid):
    if cid != request.user.id:
        return redirect('error')
    order = Order.objects.get(id=oid)
    context = {'order': order}
    if request.method == 'POST':
        # 支付 修改订单状态然后保存
        order.status = '已支付'
        order.save()
        return redirect('orders', cid=cid)
    return render(request, 'accounts/pay.html', context)


def collectticket(request, cid, oid):
    if cid != request.user.id:
        return redirect('error')
    order = Order.objects.get(id=oid)
    if order.status != '已支付':
        return redirect('orders', cid=cid)
    user = User.objects.get(id=cid)
    flight = Flight.objects.get(id=order.flight.id)
    rows = [i + 1 for i in range(flight.rownum)]
    columns = [i + 1 for i in range(flight.columnnum)]
    if request.method == 'POST':
        row = request.POST.get('row')
        column = request.POST.get('column')
        ticket = Ticket.objects.filter(flight=flight).filter(seatcolumn=column).filter(seatrow=row)
        if ticket:
            print("该座位被使用")
            messages.error(request, '该座位被使用')
        else:
            order.status = '已取票'
            order.save()
            # todo 将添加机票让数据库的触发器实现
            ticket = Ticket(customer=user, flight=flight, seatrow=row, seatcolumn=column)
            ticket.save()
            return redirect('orders', cid=cid)

    context = {'order': order, 'rows': rows, 'columns': columns}
    return render(request, 'accounts/collectticket.html', context)


def tickets(request, cid):
    if cid != request.user.id:
        return redirect('error')
    user = User.objects.get(id=cid)
    tickets = Ticket.objects.filter(customer=user)
    context = {'tickets': tickets}
    return render(request, 'accounts/tickets.html', context)


def error(request):
    return render(request, 'accounts/error.html')


# 管理员的主页
def manage(request):
    # todo
    #  1. 添加对航班信息的插入  完成
    #  2. 添加所有订单情况的查看
    #  3. 添加所有航班信息的查看 完成
    #     航班的销售情况  ---  基本信息 + 满座率 + 总金额

    #  get all flights
    flights = Flight.objects.all()
    flightnum = flights.count()
    ordernum = Order.objects.count()

    form = FlightForm()
    context = {'form': form, 'flights': flights, 'flightnum': flightnum, 'ordernum': ordernum}
    return render(request, 'accounts/manage.html', context)


# 航班管理
def manageflight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)

        if form.is_valid():
            print('OK')
            print(form.cleaned_data)
            form.save()
        else:
            print('not ok')
    else:
        form = FlightForm()
    flights = Flight.objects.all()
    context = {'flights': flights, 'form': form}
    return render(request, 'accounts/manageflight.html', context)


def deleteflight(request, fid):
    flight = Flight.objects.get(id=fid)
    if request.method == 'POST':
        print('delete flight')
        flight.delete()
        return redirect('manageflight')
    context = {'flight': flight}
    return render(request, 'accounts/deleteflight.html', context)


def modifyflight(request, fid):
    flight = Flight.objects.get(id=fid)
    form = FlightForm(instance=flight)

    if request.method=='POST':
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect('manageflight')
    context = {'form':form}
    return render(request, 'accounts/modifyflight.html',context)

def checkorders(request):
    # 查看所有的订单
    orders = Order.objects.all()
    ordernum = orders.count()
    weizhifunum = orders.filter(status='未支付').count()
    yizhifunum = orders.filter(status='已支付').count()
    yiqupiaonum = orders.filter(status='已取票').count()


    context = {'orders': orders,
               'ordernum':ordernum,
               'weizhifunum':weizhifunum,
               'yizhifunum':yizhifunum,
               'yiqupiaonum':yiqupiaonum
               }
    return render(request,'accounts/checkorders.html',context)
