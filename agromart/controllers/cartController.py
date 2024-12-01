
from django.http import JsonResponse
from ..models import Cart, User,Product,ProductImage,BoughtItem
import json
import uuid
from django.db import transaction
from django.db.models import F

class CartController:
    @staticmethod
    def addToCart(request):
        if request.method == 'POST':
            try:
                data = request.body.decode('utf-8')
                body = json.loads(data)
                user = User.objects.get(userId=body.get('userId'))
                product = Product.objects.get(productId=body.get('productId'))
                quantity = body.get('quantity')
                existing_cart_item = Cart.objects.filter(userId=user, product=product).first()
                if existing_cart_item:
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return JsonResponse({'message': 'Product quantity updated in cart successfully'}, status=200)
                else:
                    newCartItem = {
                        'cartId': uuid.uuid4(),
                        'userId': user,
                        'product': product,
                        'quantity': quantity
                    }
                    Cart.objects.create(**newCartItem)
                    return JsonResponse({'message': 'Product added to cart successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)


    @staticmethod
    def removeFromCart(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                product = Product.objects.get(productId=body_data.get('productId'))
                cart_item = Cart.objects.get(product=product)
                cart_item.delete()
                return JsonResponse({'message': 'Product removed from cart successfully'})
            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart item not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @staticmethod
    def getUserCart(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user_cart_items = Cart.objects.filter(userId=body_data.userId)
                cart_items_list = [{'cartId': item.cartId,
                                    'userId': item.userId,
                                    'product_id': item.product_id,
                                    'quantity': item.quantity} for item in user_cart_items]
                return JsonResponse({'user_cart_items': cart_items_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    @staticmethod
    def getAllItems(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                user = User.objects.get(userId=body.get('userId'))
                user_cart_items = Cart.objects.filter(userId=user)
                products = []
                for item in user_cart_items:
                    product = item.product
                    product_info = {
                        'productId': product.productId,
                        'name': product.name,
                        'description': product.description,
                        'price': product.price,
                        'itemsLeft':product.quantity,
                        'quantity': item.quantity,
                        'images': []
                    }
                    product_images = ProductImage.objects.filter(product=product)
                    for image in product_images:
                        product_info['images'].append(image.image.url)
                    products.append(product_info)
                return JsonResponse({'products': products})
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    @staticmethod
    def clearCart(request):
        if request.method == 'POST':
            try:
                data = request.body.decode('utf-8')
                body = json.loads(data)
                user = User.objects.get(userId=body.get('userId'))
                Cart.objects.filter(userId=user).delete()
                return JsonResponse({'message': 'Cart cleared successfully'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)