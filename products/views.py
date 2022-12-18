from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import Foot1_Nav,Site_Profile,Top_Nav
# Create your views here.
from products.models import CommentForm, Comment , BlogModel


def index(request):
   return  HttpResponse("My Product Page")


def addcomment(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
        data = Comment()  # create relation with model
        data.subject = form.cleaned_data['subject']
        data.comment = form.cleaned_data['comment']
        data.rate = form.cleaned_data['rate']
        data.ip = request.META.get('REMOTE_ADDR')
        data.product_id=id
        current_user= request.user
        data.user_id=current_user.id
        data.save()  # save data to table
        messages.success(request, "Your review has ben sent. Thank you for your interest.")
        return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)



def BlogDetailView(request,id):
   setting = Site_Profile.objects.get(pk=1)
   topnav = Top_Nav.objects.all()
   f1 = Foot1_Nav.objects.all() [:5]
   blog = BlogModel.objects.get(id=id)
   context={'blog':blog,'setting':setting,'topnav':topnav,'f1':f1}
   return render(request,'Pages/blog.html',context)