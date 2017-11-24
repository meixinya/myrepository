from django.conf.urls import url

from . import views,viewsorders

urlpatterns = [
    #url(r'^$',views.index,name="index"),

    #===========商品展示==================
    url(r'^$', views.shopindex,name='shopindex'), #  商城首页
    url(r'^shoplist$', views.shoplist,name='shoplist'), #  商城列表页
    url(r'^shop/(?P<gid>[0-9]+)$', views.shop,name='shop'), #  商城详情页
    url(r'^person$', views.person,name='person'), #  个人中心

    
    #===========会员模块==================
    url(r'^shoplogin', views.shoplogin,name='shoplogin'), #  会员登录
    url(r'^shopregister', views.shopregister,name='shopregister'), #  会员注册
    url(r'^shopinsert$', views.shopinsert, name="shopinsert"),
    url(r'^shopdologin$', views.shopdologin, name="shopdologin"),#会员执行登录
    url(r'^shoplogout$', views.shoplogout, name="shoplogout"),#会员退出
    
    #===========购物车模块================
    url(r'^shopcart$', viewsorders.shopcart, name="shopcart"),#购物车
    url(r'^shopcartadd/(?P<sid>[0-9]+)$', viewsorders.shopcartadd, name="shopcartadd"),#添加购物车
    url(r'^shopcartdel/(?P<sid>[0-9]+)$', viewsorders.shopcartdel, name="shopcartdel"),#购物车
    url(r'^shopcartclear$', viewsorders.shopcartclear, name="shopcartclear"),#购物车
    url(r'^shopcartchange$', viewsorders.shopcartchange, name="shopcartchange"),#更改购物车中商品数量

    #===========订单模块==================
    url(r'^ordersform$', viewsorders.ordersform, name="ordersform"),#订单
    url(r'^ordersconfirm$', viewsorders.ordersconfirm, name="ordersconfirm"),#订单确认
    url(r'^ordersinsert$', viewsorders.ordersinsert, name="ordersinsert"),#执行订单添加
    url(r'^ordersinfo$', viewsorders.ordersinfo, name="ordersinfo"),#订单信息
    url(r'^order$', viewsorders.order, name="order"),#订单信息

    
]
