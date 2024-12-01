from django.shortcuts import render
from .controllers.userController import UserController
from .controllers.categoryController import categoryController
from .controllers.productController import productController
from .controllers.cartController import CartController
from .controllers.boughtItemController import BoughtItemController

def home(request):
    return render(request,'agromart/common/home.html')
def register(request):
    return render(request,'agromart/common/register.html')
def createUser(request):
    return UserController.createUser(request)
def login(request):
    return render(request,'agromart/common/login.html')
def loginLog(request):
    return UserController.loginUser(request)


def admindash(request):
    return render(request,'agromart/admin/admindash.html')
def adminusers(request):
    return render(request,'agromart/admin/users.html')
def adminproducts(request):
    return render(request,'agromart/admin/products.html')
def viewusers(response):
    return UserController.getAllUsers(response)
def admindeleteuser(request):
    return UserController.deleteUser(request)
def createcategory(request):
    return categoryController.addCategory(request)
def viewcategories(request):
    return categoryController.getAllCategories(request)
def deletecategory(request):
    return categoryController.deleteCategory(request)
def viewadmin(request):
    return UserController.getUser(request)
def viewallboughtproducts(request):
    return BoughtItemController.ViewAllBoughtProducts(request)
def deleteallboughtitems(request):
    return BoughtItemController.DeleteAllBoughtItems(request)

def sellerdash(request):
    return render(request,'agromart/seller/sellerdash.html')
def sellerproducts(request):
    return render(request,'agromart/seller/products.html')
def sellerproduct(request):
    return render(request,'agromart/seller/product.html')
def addproduct(request):
    return render(request,'agromart/seller/addproduct.html')
def sellerprofile(request):
    return render(request,'agromart/seller/profile.html')
def sellerfunds(request):
    return render(request,'agromart/seller/funds.html')
def createproduct(request):
    return productController.addProduct(request)
def deleteproduct(request):
    return productController.deleteProduct(request)
def editproduct(request):
    return productController.editProduct(request)
def getproduct(request):
    return productController.getProduct(request)
def getallproducts(request):
    return productController.getAllProducts(request)
def getalluserproducts(request):
    return productController.getAllUserProducts(request)
    
def products(request):
    return render(request,'agromart/user/products.html')
def checkout(request):
    return render(request,'agromart/user/checkout.html')
def cart(request):
    return render(request,'agromart/user/cart.html')
def buyerprofile(request):
    return render(request,'agromart/user/profile.html')
def buyerfunds(request):
    return render(request,'agromart/user/funds.html')
def viewproduct(request):
    return render(request,'agromart/user/productinfo.html')
def viewuserboughtitemspage(request):
    return render(request,'agromart/user/BoughtItems.html')
def addtocart(request):
    return CartController.addToCart(request)
def viewcartitems(request):
    return CartController.getAllItems(request)
def viewcartitem(request):
    return CartController.getcartitem(request)
def removefromcart(request):
    return CartController.removeFromCart(request)
def clearCart(request):
    return CartController.clearCart(request)
def buyitem(request):
    return productController.buyProduct(request)
def loadfunds(request):
    return UserController.loadCash(request)
def spendcash(request):
    return UserController.spendCash(request)
def viewuserboughtitems(request):
    return BoughtItemController.ViewUserBoughtProducts(request)
def deleteuserboughtitem(request):
    return BoughtItemController.DeleteBoughtItem(request)

def notfoundpage(request, exception):
    return render(request,'agromart/common/404.html',status=404)