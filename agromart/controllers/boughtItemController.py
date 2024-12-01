from ..models import BoughtItem,ProductImage,User
from django.http import JsonResponse
import json

class BoughtItemController:
    @staticmethod
    def ViewAllBoughtProducts(request):
        if request.method == 'GET':
            try:
                products = BoughtItem.objects.all()
                products_list = []
                for product in products:
                    images = ProductImage.objects.filter(product=product.product)
                    product_data = {
                        'productId': product.boughtItemId,
                        'product': product.product.name,
                        'quantity': product.quantity,
                        'userId': product.userId.userId,
                        'quantity': product.quantity,
                        'images': [image.image.url for image in images]
                    }
                    products_list.append(product_data)
                return JsonResponse({'products': products_list})
            except Exception as e:
                print('error',str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    @staticmethod
    def ViewUserBoughtProducts(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user_id = body_data.get('userId')
                user = User.objects.get(userId=user_id)
                products = BoughtItem.objects.filter(userId=user)
                products_list = []
                for product in products:
                    images = ProductImage.objects.filter(product=product.product)
                    product_data = {
                        'productId': product.boughtItemId,
                        'product': product.product.productId,
                        'productName':product.product.name,
                        'productQuantity':product.product.quantity,
                        'quantity': product.quantity,
                        'userId': product.userId.userId,
                        'purchasedDate':product.purchase_date,
                        'images': [image.image.url for image in images]
                    }
                    products_list.append(product_data)
                return JsonResponse({'products': products_list}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    @staticmethod
    def DeleteBoughtItem(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                productId = body.get('productId')
                product = BoughtItem.objects.get(boughtItemId=productId)
                product.delete()
                return JsonResponse({'message':'Product Deleted sucessfully'},status=200)
            except BoughtItem.DoesNotExist:
                return JsonResponse({'error':'Product not Found'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    @staticmethod
    def DeleteAllBoughtItems(request):
        if request.method == 'GET':
            try:
               BoughtItem.objects.all().delete()
               return JsonResponse({'message':'Deleted sucessfully'},status=200)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)        
        else:
            return JsonResponse({'error':'Method not allowed'}, status=405)
        

    