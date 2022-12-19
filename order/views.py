from django.contrib.auth.models import AnonymousUser ,User
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Site_Profile, Foot1_Nav, Top_Nav
from order.models import ShopCart, ShopCartForm, OrderForm, Order
from order.forms import PaymentMethodForm
from products.models import Category, Product,Variants,Images
import razorpay
from django.http import JsonResponse
from user.models import UserProfile
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import requests
# Create your views here.

def index(request):
    return HttpResponse (" ored page ")

def shopcart(request):
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    
    f1 = Foot1_Nav.objects.all() [:5]
    
    
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    # shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    totaloff=0
    save=0
    id = request.GET.get('id')
    quantity = (request.GET.get('quantity'))
    if id and quantity:
        cart_data ={}
        cart_dict ={}
        cart_list = []
        shopcart = Variants.objects.filter(id=id)
        for j in shopcart:
            total = j.price * int(quantity)
            cart_dict["name"]= j.product.title
            cart_dict["price"]=float(j.price)
            cart_dict["quantity"]=quantity
            image = Images.objects.get(id=j.image_id)
            cart_dict["image"] = image.image.url
            cart_dict["color"] = j.color.name
            cart_list.append(cart_dict)
        cart_data["data"]=cart_list
        cart_data["total"]=float(total)
        print(cart_data)
        return JsonResponse(data=cart_data,safe=False)



    # for rs in shopcart:
    #     total += rs.variant.price * rs.quantity
    #     totaloff += rs.product.price * rs.quantity
    #     save += totaloff - total
    #return HttpResponse(str(total))
    context={
             'category':category,
             'total': total,
             'save': save,
             'setting': setting, 'f1': f1, 'topnav': topnav, 
             }
    return render(request,'Checkout/checkout1.html',context)

def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect("/cart/")

def orderproduct(request):
    user = User()
    anonymous = AnonymousUser()
    setting = Site_Profile.objects.get(pk=1)
    topnav = Top_Nav.objects.all()
    f1 = Foot1_Nav.objects.all() [:5]
    category = Category.objects.all()



    # shopcart = ShopCart.objects.filter(user_id=current_user.id)
    # total=0
    # totaloff=0
    # save=0
    # for rs in shopcart:
    #     product  = rs.product_id
    #     total += rs.variant.price * rs.quantity
    #     totaloff += rs.product.price * rs.quantity
    #     save += totaloff - total

    # product = Product.objects.get(id=product)
    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        #return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            data = Order()
            current_user = request.user  # Access User Session information
            if current_user == anonymous :
                user.first_name = form.cleaned_data['full_name']
                user.username = request.POST['email']
                user.email = request.POST['email']
                user.password = 'pass@123'
                user.save()
                login(request,user)
                SendEmailUserCreated(user.username,user.username,user.password)
            else :
                print('inside current!!',current_user)
                user = current_user
              
            id_variant = request.POST['productId']
            variant = Variants.objects.get(id=id_variant)
            product = Product.objects.get(id=variant.product.id)
            data.product = product
            data.full_name = form.cleaned_data['full_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.state = form.cleaned_data['state']
            data.pincode = form.cleaned_data['pincode']
            data.phone = form.cleaned_data['phone']
            data.variant = variant
            data.user=user
            data.payment_method = form.cleaned_data['payment_method']
            # data.user_id = current_user.id
            data.total = product.price
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode= get_random_string(5).upper() # random cod
            data.code =  ordercode
            if  data.payment_method == 'Semi Cash On Delivery':
                data.save()
                SendEmailorder(to=data.user.email)
                # ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
                request.session['cart_items']=0
                messages.success(request, "Your Order has been completed. Thank you ")
                return render(request, 'Checkout/checkout3.html',{'ordercode':ordercode,'category': category,'setting': setting, 'f1': f1,'topnav': topnav,})
            elif data.payment_method == 'RazorPay':
                SendEmailorder(to=data.user.email)
                data.save()
                # ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
                request.session['cart_items']=0
                messages.success(request, "Your Order has been completed. Thank you ")
                return render(request, 'Checkout/checkout3.html',{'ordercode':ordercode,'category': category,'setting': setting, 'f1': f1,'topnav': topnav,})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/")
    payment_method = PaymentMethodForm
    form= OrderForm()
    # profile = UserProfile.objects.get(user_id=current_user.id)
    context={'shopcart': shopcart,
             'category':category,
             'total': 1,
             'save': 1,
            #  'profile':profile,
             'payment_method':payment_method,
             'setting': setting, 'f1': f1,'topnav': topnav, 
             }
    return render(request,'Checkout/checkout2.html',context)

#Handler for retriving data of cart from cart models
def data(request):
    cart_data = ShopCart.objects.filter(user=request.user)
    total=0
    totaloff=0
    save=0
    for rs in cart_data:
        total += rs.variant.price * rs.quantity
        totaloff += rs.product.price * rs.quantity
        save += totaloff - total
    return {'grand':str(total)}

#Razorpay payment handler
def Create_RazorPayOrder(request):
    response=shopcart(request)
    id=request.GET.get('id')
    setting = Site_Profile.objects.get(id=1)
    quantity=request.GET.get('quantity')
    response = requests.request('GET',f'{ setting.url }/cart/?id={id}&quantity={quantity}')
    grand_total=response.json()['total']
    grand_total=float(grand_total)
    #authenticating with razorpay client
    client = razorpay.Client(auth=('rzp_live_szMbVIbgvLVk1W','AE1RadvqaHXXbRymUrlEHViS' ))


    #creating order in razorpay dashboard
    order_data_razorpay = client.order.create({'amount':(grand_total)*100, 'currency': 'INR','payment_capture': '1'})


    #responssing order_id generated by razorpay and amount for frontend
    return JsonResponse(order_data_razorpay)

def Create_RazorPayOrder_Cod(request):
    # response=data(request)
    # grand_total=response['grand']
    # grand_total=float(grand_total)
    #authenticating with razorpay client
    client = razorpay.Client(auth=('rzp_live_szMbVIbgvLVk1W','AE1RadvqaHXXbRymUrlEHViS' ))


    #creating order in razorpay dashboard
    order_data_razorpay = client.order.create({'amount':(1500)*100, 'currency': 'INR','payment_capture': '1'})


    #responssing order_id generated by razorpay and amount for frontend
    return JsonResponse(order_data_razorpay)



@login_required(login_url='/login/') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product= Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id) # Check product in shopcart
        if checkinproduct:
            control = 1 # The product is in the cart
        else:
            control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
                if product.variant == 'None':
                    data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                else:
                    data = ShopCart.objects.get(product_id=id, variant_id=variantid, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()  # save data
            else : # Inser to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id =None
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)




def SendEmailorder(to):
    pending_amount = 0
    user=User.objects.filter(email=to).first()
    order = Order.objects.filter(user=user).order_by('-create_at')
    setting = Site_Profile.objects.get(pk=1)
    for i in order:
        if i.payment_method == 'Semi Cash On Delivery':
            pending_amount = i.variant.price - 1500
    context={
        "user":user,
        "order":order,
        "setting":setting,
        "pending":pending_amount
    }
    msg_html = render_to_string('Pages/order-success.html',context)
    message = EmailMultiAlternatives('regarding order',"hello this is confirmation!!",settings.EMAIL_HOST_USER,[to])
    message.attach_alternative(msg_html,"text/html")
    message.send()
    

def SendEmailUserCreated(to,username,password):
    message = EmailMultiAlternatives('Acoount created',f"Your account is successfully created !!\n Username :{username}\n Password :{password}",settings.EMAIL_HOST_USER,[to])
    message.send()
