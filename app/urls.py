from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),  # 首页

    url(r'^market/$', views.market, name='marketbase'), # 闪购超市
    url(r'^market/(?P<childid>\d+)/(?P<sortid>\d+)/$', views.market, name='market'), # 闪购超市

    # url(r'^market/$', views.market, name='market'),

    url(r'^cart/$', views.cart, name='cart'),   # 购物车
    url(r'^mine/$', views.mine, name='mine'),   # 我的

    url(r'^login/$', views.login, name='login'),    # 登录
    url(r'^logout/$', views.logout, name='logout'),    # 退出
    url(r'^register/$', views.register, name='register'),    # 登录
    url(r'^checkemail/$', views.checkemail, name='checkemail'), # 账号验证


    url(r'^addcart/$', views.addcart, name='addcart'),  # 添加到购物车
    url(r'^subcart/$', views.subcart, name='subcart'),  # 删减购物车
    url(r'^changecartselect/$', views.changecartselect, name='changecartselect'),   # 购物车商品选中状态
    url(r'^changecartall/$',views.changecartall,name='changecartall'),


url(r'^generateorder/$', views.generateorder, name='generateorder'),    # 生成订单
    url(r'orderlist/$', views.orderlist, name='orderlist'), # 订单列表
    url(r'^orderdetail/(?P<identifier>[\d.]+)/$', views.orderdetail, name='orderdetail'),
]