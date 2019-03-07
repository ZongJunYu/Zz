from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtypes


def home(request):

    wheels=Wheel.objects.all()

    navs=Nav.objects.all()

    mastbuys=Mustbuy.objects.all()

    shops=Shop.objects.all()

    shop1=shops[0]
    shop2=shops[1:3]
    shop3=shops[3:7]
    shop4=shops[7:11]

    mainshows=Mainshow.objects.all()



    # print(mastbuys)

    response_dir={
        'wheels':wheels,
        'navs':navs,
        'mastbuys':mastbuys,
        'shop1':shop1,
        'shop2':shop2,
        'shop3':shop3,
        'shop4':shop4,
        'mainshows':mainshows
    }

    return render(request,'home/home.html',context=response_dir)


def market(request):
    foodtypes=Foodtypes.objects.all()

    response_dir={
        'foodtypes':foodtypes,
    }

    return render(request,'market/market.html',context=response_dir)


def cart(request):
    return render(request,'cart/cart.html')


def mine(request):
    return render(request,'mine/mine.html')