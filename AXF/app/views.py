from django.shortcuts import render

# Create your views here.
from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtypes, Goods


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


# def market(request,categoryid=104749):
def market(request,childid='0',sortid='0'):
    foodtypes=Foodtypes.objects.all()


    # 商品信息
    # goods_list=Goods.objects.all()[0:5]
    # 默认打开页面（热销榜)
    #点击左侧分类，即显示对应商品信息 [傳參數categoryid]
    # goods_list=Goods.objects.filter(categoryid=categoryid)


    #客户端需要记录  点击的分类下表 ·[cookies,会自动携带]

    index=int(request.COOKIES.get('index','0'))

    # 根据index 获取 对应的 分类ID

    categoryid=foodtypes[index].typeid
    #根据分类id 获取对应分类信息
    # goods_list = Goods.objects.filter(categoryid=categoryid)
    #子类
    if childid=='0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(childcid=childid)
    #获取子类信息
    if sortid=='1':
        goods_list=goods_list.order_by('-productnum')
    elif sortid=='2':
        goods_list=goods_list.order_by('price')
    elif sortid=='3':
        goods_list = goods_list.order_by('-price')

    childtypenames = foodtypes[index].childtypenames

    childtype_list=[]

    for item in  childtypenames.split('#'):
        # item >> 全部分类：0

        item_arr = item.split(':')

        # print(item_arr)
        temp_dir={
            'name':item_arr[0],
            'id':item_arr[1]
        }

        childtype_list.append(temp_dir)
        # print(childtype_list)
    response_dir={
        'foodtypes':foodtypes,
        'goods_list':goods_list,
        'childtype_list':childtype_list,
        'childid':childid
    }

    return render(request,'market/market.html',context=response_dir)


def cart(request):
    return render(request,'cart/cart.html')


def mine(request):
    return render(request,'mine/mine.html')


def login(request):
    return None


def logout(request):
    return None


def register(request):
    return None