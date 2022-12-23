from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from home import views
from user import views as UserViews
from order import views as OrderViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('colors/<int:id>',views.ColorView),
    path('order/', include('order.urls')),
    path('product/', include('products.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('blog/<int:id>/<slug:slug>', views.BlogDetailView, name='blogdetail'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('search/', views.search, name='search'),
    path('privacy-policy/', views.pp),
    path('return-policy/', views.rp),
    path('shipping-policy/', views.sp),
    path('terms-conditions/', views.tc),
    path('contact-us/', views.contact),
    path('login/', UserViews.login_form, name='login'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('signup/', UserViews.signup_form, name='signup'),
    path('cart/', OrderViews.shopcart, name='shopcart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'home.views.error_404'