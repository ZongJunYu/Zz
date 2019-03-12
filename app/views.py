import hashlib
import random
import time

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtypes, Goods, User, Cart, Order, OrderGoods


# Create your views here.
def home(request):
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shops = Shop.objects.all()
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass_list = shops[3:7]
    shopcommends = shops[7:11]

    # 商品列表
    mainshows = Mainshow.objects.all()

    response_dir = {
        'wheels':wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptabs': shoptabs,
        'shopclass_list': shopclass_list,
        'shopcommends': shopcommends,
        'mainshows': mainshows
    }

    return render(request, 'home/home.html', context=response_dir)



# def market(request, categoryid=104749):
def market(request, childid='0', sortid='0'):
    # 分类信息
    foodtypes = Foodtypes.objects.all()


    # 商品信息
    # goods_list = Goods.objects.all()[0:5]
    # 默认打开页面  热销榜
    # 点击左侧分类，即显示对应分类 商品信息  【传参数categoryid】
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 客户端 需要记录 点击的分类下标 【cookies， 会自动携带】
    index = int(request.COOKIES.get('index', '0'))
    # 根据index 获取 对应的 分类ID
    categoryid = foodtypes[index].typeid
    # 根据 分类ID 获取对应分类信息
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 子类
    if childid == '0':
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    # 排序
    # 0默认综合排序   1销量排序     2价格最低   3价格最高
    if sortid == '1':
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '2':
        goods_list = goods_list.order_by('price')
    elif sortid == '3':
        goods_list = goods_list.order_by('-price')

    # 获取子类信息
    childtypenames = foodtypes[index].childtypenames
    # 存储子类信息 列表
    childtype_list = []
    # 将对应的子类拆分出来
    for item in childtypenames.split('#'):
        # item  >> 全部分类:0
        # item  >> 子类名称: 子类ID
        item_arr = item.split(':')
        temp_dir = {
            'name': item_arr[0],
            'id': item_arr[1]
        }

        childtype_list.append(temp_dir)


    response_dir = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtype_list': childtype_list,
        'childid': childid,
    }


    # 获取购物车信息
    token = request.session.get('token')
    userid = cache.get(token)


    if userid:
        user = User.objects.get(pk=userid)
        carts = user.cart_set.all()
        response_dir['carts'] = carts


    return render(request, 'market/market.html', context=response_dir)


def cart(request):
    token = request.session.get('token')
    userid = cache.get(token)
    if userid:  # 有登录才显示
        user = User.objects.get(pk=userid)
        carts = user.cart_set.filter(number__gt=0)

        isall = True
        for cart in carts:
            if not cart.isselect:
                isall = False

        return render(request, 'cart/cart.html', context={'carts': carts, 'isall':isall})
    else:   # 未登录不显示
        return render(request, 'cart/no-login.html')



def mine(request):
    # 获取
    token = request.session.get('token')
    userid = cache.get(token)
    response_data={
     'user': None
    }
    if userid:
        user = User.objects.get(pk=userid)
        response_data['user'] = user
        orders=user.order_set.all()

        response_data['waitpay']=orders.filter(status=0).count()
        response_data['paydone']=orders.filter(status=1).count()
    return render(request, 'mine/mine.html', context=response_data)


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 重定向位置
        back = request.COOKIES.get('back')

        users = User.objects.filter(email=email)
        if users.exists():  # 存在
            user = users.first()
            if user.password == generate_password(password):    # 验证通过
                # 更新token
                token = generate_token()

                # 状态保持
                cache.set(token, user.id, 60*60*24*3)

                # 传递客户端
                request.session['token'] = token

                # 根据back
                if back == 'mine':
                    return redirect('axf:mine')
                else:
                    return redirect('axf:marketbase')
            else:   # 密码错误
                return render(request, 'mine/login.html', context={'ps_err': '密码错误'})
        else:   # 不存在
            return render(request, 'mine/login.html', context={'user_err':'用户不存在'})

def logout(request):
    request.session.flush()

    return redirect('axf:mine')


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def generate_token():
    temp = str(time.time()) + str(random.random())
    md5 = hashlib.md5()
    md5.update(temp.encode('utf-8'))
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
        # 获取数据
        email = request.POST.get('email')
        name = request.POST.get('name')
        passoword = generate_password(request.POST.get('password'))

        # 存入数据库
        user = User()
        user.email = email
        user.password = passoword
        user.name = name
        user.save()

        # 状态保持
        token = generate_token()
        # key-value  >>  token:userid
        cache.set(token, user.id, 60*60*24*3)

        request.session['token'] = token

        return redirect('axf:mine')


def checkemail(request):
    email = request.GET.get('email')

    # 去数据库中查找
    users = User.objects.filter(email=email)
    if users.exists():  # 账号被占用
        response_data = {
            'status': 0,  # 1可用， 0不可用
            'msg': '账号被占用!'
        }
    else:   # 账号可用
        response_data = {
            'status':1,  # 1可用， 0不可用
            'msg': '账号可用!'
        }

    # 返回JSON数据
    return JsonResponse(response_data)


def addcart(request):
    # 获取token
    token = request.session.get('token')

    # 响应数据
    response_data = {}

    # 缓存
    if token:
        userid = cache.get(token)

        if userid:  # 已经登录
            user = User.objects.get(pk=userid)
            goodsid = request.GET.get('goodsid')
            goods = Goods.objects.get(pk=goodsid)

            # 商品不存在: 添加新记录
            # 商品存在: 修改number
            carts = Cart.objects.filter(user=user).filter(goods=goods)
            if carts.exists():
                cart = carts.first()
                cart.number = cart.number + 1
                cart.save()
            else:
                cart = Cart()
                cart.user = user
                cart.goods = goods
                cart.number = 1
                cart.save()

            response_data['status'] = 1
            response_data['number'] = cart.number
            response_data['msg'] = '添加 {} 购物车成功: {}'.format(cart.goods.productlongname, cart.number)

            return JsonResponse(response_data)

    # 未登录
    # 因为是ajax操作，所以重定向是不可以的!
    # return redirect('axf:login')

    response_data['status'] = -1
    response_data['msg'] = '请登录后操作'

    return JsonResponse(response_data)


def subcart(request):
    # 商品
    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    # 用户
    token = request.session.get('token')
    userid = cache.get(token)
    user = User.objects.get(pk=userid)

    # 获取对应的购物车信息
    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number -1
    cart.save()

    response_data = {
        'msg': '删减商品成功',
        'status': 1,
        'number': cart.number
    }

    return JsonResponse(response_data)


def changecartselect(request):
    cartid = request.GET.get('cartid')

    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    response_data = {
        'msg': '状态修改成功',
        'status': 1,
        'isselect': cart.isselect
    }

    return JsonResponse(response_data)


def changecartall(request):

    isall=request.GET.get('isall')


    token=request.session.get('token')
    userid=cache.get(token)
    user=User.objects.get(pk=userid)
    carts=user.cart_set.all()

    if isall=='true':
        isall=True
    else:
        isall=False

    for cart in carts:
        cart.isselect=isall
        cart.save()

    response_data={
        'msg':'全选/取消全选 成功',
        'status':1
    }
    return JsonResponse(response_data)


def generate_identifier():
    temp=str(time.time())+str(random.randrange(1000,10000))
    return temp

def generateorder(request):
    token=request.session.get('token')
    userid=cache.get(token)
    user=User.objects.get(pk=userid)

    order=Order()
    order.user=user
    order.identifier=generate_identifier()
    order.save()

    carts=user.cart_set.filter(isselect=True)
    for cart in carts:
        orderGoods=OrderGoods()
        orderGoods.order=order
        orderGoods.goods=cart.goods
        orderGoods.number=cart.number
        orderGoods.save()

        cart.delete()

    return render(request,'order/orderdetail.html',context={'order':order})

def orderlist(request):
    token=request.session.get('token')
    userid=cache.get(token)
    user=User.objects.get(pk=userid)

    orders=user.order_set.all()

    return render(request,'order/orderlist.html',context={'orders':orders})

def orderdetail(request ,identifier):
    order=Order.objects.filter(identifier=identifier).first()

    return render(request,'order/orderdetail.html',context={'order':order})