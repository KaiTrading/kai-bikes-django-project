from django.shortcuts import render
from home.models import Foot1_Nav, Slider, Site_Profile, Banner, Top_Nav
from order.models import ShopCart
from products.models import Category, Comment, Images, Product, Variants,Color,BlogModel
from django.http import  JsonResponse
from django.template.loader import render_to_string
import datetime
from order.views import SendEmailorder
    
# Create your views here.


def ColorView(request,id):
    product = Product.objects.get(pk=id)
    if product.variant !="None":
        variants = Variants.objects.filter(product_id=id)
        colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id)
        color_code_list=[]
        for i in colors:
            color_code = Color.objects.get(id=i.color_id)
            color_code_list.append(color_code.code)
        return JsonResponse({"Colors":color_code_list},safe=False)
        
def index(request):
    setting = Site_Profile.objects.get(pk=1)
    blogs = BlogModel.objects.all()
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    slider = Slider.objects.all().order_by('id') [:3]
    latest_products = Product.objects.all().order_by('id') [:4]
    popular_products = Product.objects.all().order_by('?') [:4]
    banner = Banner.objects.all().order_by('id') [:3]
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'blogs':blogs, 'banner':banner, 'shopcart': shopcart, 'slider':slider,  'total': total, 'save': save, 'f1': f1, 'topnav': topnav,  'latest_products':latest_products, 'popular_products':popular_products}
    return render(request, 'Index/index.html', context)

def error_404(request,exception):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    context = {'setting':setting, 'f1': f1,   'topnav': topnav,}
    return render(request, 'Pages/404.html', context)

def category_products(request,id,slug):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    products = Product.objects.filter(category_id=id) #default language
    variant = Variants.objects.filter(product_id=id)
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = { 'setting':setting, 'shopcart': shopcart, 'total': total, 'save': save, 'catdata':catdata, 'variant':variant,  'category':category, 'f1': f1,   'topnav': topnav,   'products':products}
    
    return render(request,'Category/category.html',context)

def product_detail(request, id, slug):
    total_rate=0
    review_list=[1,2,3,4,5]
    query = request.GET.get('q')
    topnav = Top_Nav.objects.all()
    
    current_date =  datetime.datetime.now()
    add_two_days = datetime.timedelta(days=3)
    add_five_days = datetime.timedelta(days=5)
    shipping_date = current_date + add_two_days
    shipping_date2 = current_date + add_five_days
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    popular_products = Product.objects.all().order_by('?') [:4]
    product = Product.objects.get(pk=id) #default language
    reviwes = Comment.objects.filter(product=product)
    if reviwes.count() > 1:
        for i in reviwes:
            total_rate=i.rate
        product_rating = round(total_rate/reviwes.count())
    else:
        product_rating=0
    category = Category.objects.all()
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id,status='True')
    setting = Site_Profile.objects.get(pk=1)
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'review_list':review_list,'product_rating':product_rating,'popular_products':popular_products,'current_date':current_date,'shipping_date':shipping_date,'shipping_date2':shipping_date2,'shopcart': shopcart, 'total': total, 'save': save, 'comments':comments, 'setting':setting, 'images':images, 'category':category, 'f1': f1,   'topnav': topnav,   'product':product}
    
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  products_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    
    return render(request,'Product/product.html',context)

def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('Product/color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def search(request):
	q=request.GET['q']
	data=Product.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'Search/search.html',{'data':data})

def pp(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'shopcart': shopcart, 'f1': f1,   'topnav': topnav,  'total': total, 'save': save}
    return render(request, 'Pages/privecy-policy.html', context)
def rp(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'f1': f1,   'topnav': topnav,  'shopcart': shopcart, 'total': total, 'save': save}
    return render(request, 'Pages/return-policy.html', context)
def sp(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'f1': f1,   'topnav': topnav,  'shopcart': shopcart, 'total': total, 'save': save}
    return render(request, 'Pages/shipping-return.html', context)
def tc(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'f1': f1,   'topnav': topnav,  'shopcart': shopcart, 'total': total, 'save': save}
    return render(request, 'Pages/t-c.html', context)
def contact(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    current_user = request.user  # Access User Session information
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    for rs in shopcart:
        total += rs.variant.price * rs.quantity
        totaloff=rs.product.price * rs.quantity
        save += totaloff - total
    context = {'setting':setting, 'f1': f1,   'topnav': topnav,  'shopcart': shopcart, 'total': total, 'save': save}
    return render(request, 'Pages/contact.html', context)