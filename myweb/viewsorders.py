from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from myweb.models import Types,Goods,Users,Orders,Detail
from django.core.urlresolvers import reverse
import time,json

#===========购物车模块================
#公共信息加载函数
def loadinfo(request):
    context={}
    context['type0list'] = Types.objects.filter(pid=0)
    return context
#购物车
def shopcart(request):
    context = loadinfo(request)
    if 'shoplist' not in request.session:
        request.session['shoplist'] = {}
    return render(request,"myweb/shopcart.html")

# 添加购物车
def shopcartadd(request,sid):
    #获取要放入购物车中的商品信息
    goods = Goods.objects.get(id=sid)
    shop = goods.toDict();
    shop['m'] = int(request.POST['m'])
    #从session获取购物车信息
    if 'shoplist' in request.session:
        shoplist = request.session['shoplist']
    else:
        shoplist = {}
    #判断此商品是否在购物车中
    if sid in shoplist:
        #商品数量加一
        shoplist[sid]['m'] += shop['m']#若购物车中已包含要购买的商品，就将购买量加1，
    else:
        #新商品添加
        shoplist[sid] = shop
    #将购物车信息放回到session中
    request.session['shoplist'] = shoplist
    return redirect(reverse('shopcart'))

def shopcartdel(request,sid):
    shoplist = request.session['shoplist']
    del shoplist[sid]
    request.session['shoplist'] = shoplist
    return redirect(reverse('shopcart')) #重定向

def shopcartclear(request):
    context = loadinfo(request)
    request.session['shoplist'] = {}
    return render(request,"myweb/shopcart.html",context)

def shopcartchange(request):
    context = loadinfo(request)
    shoplist = request.session['shoplist']
    #获取信息
    shopid = request.GET['sid']
    num = int(request.GET['num'])
    if num <1:
        num = 1
    shoplist[shopid]['m'] = num #更改商品数量
    request.session['shoplist'] = shoplist
    return redirect(reverse('shopcart'))
    # return render(request,"myweb/shopcart.html",context)
    
#=============订单管理=====================   
#订单管理
def ordersform(request):
    # #获取要结账的商品id信息
    ids = request.GET.get('gids','')
    if ids == '':
        return HttpResponse("请选择要结账的商品")
    gids = ids.split(',')
    #获取购物车中的商品信息
    shoplist = request.session['shoplist']
    #封装要结账的商品信息 以及累计总金额
    orderlist = {}
    total = 0
    for sid in gids:
        orderlist[sid] = shoplist[sid]
        total += shoplist[sid]['price'] * shoplist[sid]['m']#累计总金额
    request.session['orderlist'] = orderlist
    request.session['total'] = total
    return render(request,"myweb/ordersform.html")

#订单确认页
def ordersconfirm(request):
    return render(request,'myweb/ordersconfirm.html')

#执行订单添加
def ordersinsert(request):
    #封装订单信息,并执行添加
    orders = Orders()
    orders.uid = request.session['vipuser']['id']
    orders.linkman = request.POST['linkman']
    orders.address = request.POST['address']
    orders.code = request.POST['code']
    orders.phone = request.POST['phone']
    orders.addtime = time.time()
    orders.total = request.session['total']
    orders.status = 0
    orders.save()
    #获取订单详情
    orderlist = request.session['orderlist']
    shoplist = request.session['shoplist']
    #遍历购物信息,并添加订单详情信息
    for shop in orderlist.values():
        del shoplist[str(shop['id'])]
        detail = Detail()
        detail.orderid = orders.id
        detail.goodsid = shop['id']
        detail.name = shop['goods']
        detail.price = shop['price']
        detail.num = shop['m']
        detail.save()

    del request.session['orderlist']
    del request.session['total']
    request.session['shoplist'] = shoplist
    return HttpResponse("订单成功:订单id号:"+str(orders.id))

#提示信息
def ordersinfo(request):
    pass

#订单操作
#我的订单
def order(request):
    context = {}
    #从session中获得登陆者的id,并从订单表orders中所有当前用户所有订单
    orders = Orders.objects.filter(uid = request.session['vipuser']['id'])
    #遍历当前用户的所有订单信息,并获取每个订单对应的订单详细信息,并以detallist属性放置
    for order in orders:
        dlist = Detail.objects.filter(orderid = order.id)
        order.detaillist = dlist
        for detail in dlist:
            goods = Goods.objects.get(id = detail.goodsid)
            detail.picname = goods.picname
    context['orders'] = orders
    return render(request,'myweb/order.html',context)






