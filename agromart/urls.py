from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register,name='register'),
    path('login/', views.login,name='login'),
    path('loginlog/',views.loginLog,name='loginlog'),
    path('createuser/',views.createUser,name='createuser'),
    
    path('admindash/',views.admindash,name='admindash'),
    path('adminusers/',views.adminusers,name='adminusers'),
    path('adminproducts/',views.adminproducts,name='adminproducts'),
    path('viewusers/',views.viewusers,name='viewusers'),
    path('admindeleteuser/',views.admindeleteuser,name='admindeleteuser'),
    path('createcategory/',views.createcategory,name='createcategory'),
    path('viewcategories/',views.viewcategories,name='viewcategories'),
    path('deletecategory/',views.deletecategory,name='deletecategory'),
    path('viewadmin/',views.viewadmin,name='viewadmin'),
    path('viewallboughtproducts/',views.viewallboughtproducts,name='viewallboughtproducts'),
    path('deleteallboughtitems/',views.deleteallboughtitems,name='deleteallboughtitems'),

    path('sellerdash/',views.sellerdash,name='sellerdash'),
    path('sellerproducts/',views.sellerproducts,name='sellerproducts'),
    path('sellerproduct/',views.sellerproduct,name='sellerproduct'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('sellerprofile/',views.sellerprofile,name='sellerprofile'),
    path('sellerfunds/',views.sellerfunds,name='sellerfunds'),
    path('createproduct/',views.createproduct,name='createproduct'),
    path('deleteproduct/',views.deleteproduct,name='deleteproduct'),
    path('editproduct/',views.editproduct,name='editproduct'),
    path('getproduct/',views.getproduct,name='getproduct'),
    path('getallproducts/',views.getallproducts,name='getallproducts'),
    path('getalluserproducts/',views.getalluserproducts,name='getalluserproducts'),

    path('products/',views.products,name='products'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart/',views.cart,name='cart'),
    path('addtocart/',views.addtocart,name='addtocart'),
    path('viewcartitems/',views.viewcartitems,name='viewcartitems'),
    path('removefromcart/',views.removefromcart,name='removefromcart'),
    path('clearcart/',views.clearCart,name='clearcart'),
    path('viewproduct/',views.viewproduct,name='viewproduct'),
    path('buyitem/',views.buyitem,name='buyitem'),
    path('buyerfunds/',views.buyerfunds,name='buyerfunds'),
    path('buyerprofile/',views.buyerprofile,name='buyerprofile'),
    path('loadfunds/',views.loadfunds,name='loadfunds'),
    path('spendcash/',views.spendcash,name='spendcash'),
    path('viewuserboughtitemspage/',views.viewuserboughtitemspage,name='viewuserboughtitemspage'),
    path('viewuserboughtitems/',views.viewuserboughtitems,name='viewuserboughtitems'),
    path('deleteuserboughtitem/',views.deleteuserboughtitem,name='deleteuserboughtitem')
]

handler404 = views.notfoundpage