import os
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import json
import uuid
from ..models import Product, ProductImage, User,BoughtItem
import base64
from django.utils import timezone

class productController:
    @staticmethod
    def addProduct(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format in request body'}, status=400)

            try:
                user = User.objects.get(userId=data.get('sellerId'))
                new_product = Product.objects.create(
                    productId=uuid.uuid4(),
                    name=data.get('name'),
                    description=data.get('description'),
                    price=data.get('price'),
                    quantity=data.get('quantity'),
                    category_id=data.get('categoryId'),
                    sellerId=user
                )

                images = data.get('images')
                for image_data in images:
                    decodedImage = base64.b64decode(image_data)
                    image_id = uuid.uuid4()
                    image_filename = f'{image_id}.png'
                    image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
                    with open(image_path, 'wb') as image_file:
                        image_file.write(decodedImage)

                    ProductImage.objects.create(
                        imageId=image_id,
                        product=new_product,
                        image=image_filename
                    )

                return JsonResponse({'message': 'Product added successfully'}, status=201)
            except Exception as e:
                print(str(e))
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        
    @staticmethod
    def getAllProducts(request):
        if request.method == 'GET':
            try:
                products = Product.objects.all()
                products_list = []
                for product in products:
                    images = ProductImage.objects.filter(product=product)
                    product_data = {
                        'productId': product.productId,
                        'name': product.name,
                        'description': product.description,
                        'price': str(product.price),
                        'quantity': product.quantity,
                        'category_id': product.category_id,
                        'sellerId': product.sellerId.userId,
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
    def getProduct(request):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            productId = body.get('productId')
            product = Product.objects.get(productId=productId)
            images = ProductImage.objects.filter(product=product)
            product_data = {
                'productId': product.productId,
                'name': product.name,
                'description': product.description,
                'price': str(product.price),
                'quantity': product.quantity,
                'category_id': product.category_id,
                'sellerId': product.sellerId.userId,
                'images': [image.image.url for image in images]
            }
            return JsonResponse({'product': product_data},status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    @staticmethod
    def deleteProduct(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                productId = body.get('productId')
                product = Product.objects.get(productId=productId)
                product.delete()
                return JsonResponse({'message':'Product Deleted sucessfully'},status=200)
            except Product.DoesNotExist:
                return JsonResponse({'error':'Product not Found'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @staticmethod
    def buyProduct(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                product = Product.objects.get(productId=body_data.get('productId'))
                buyer = User.objects.get(userId=body_data.get('userId'))
                buyerBalance = Decimal(buyer.acc_balance)
                boughtQuantity = int(body_data.get('quantity'))
                seller = User.objects.get(userId=product.sellerId.userId)
                productQuantity = int(product.quantity)
                if productQuantity < boughtQuantity:
                    return JsonResponse({'error': 'Choose a lower value please'}, status=400)
                total_price = Decimal(product.price) * Decimal(boughtQuantity)
                if buyerBalance < total_price:
                    return JsonResponse({'error': 'Insufficient balance'}, status=400)
                productQuantity -= boughtQuantity 
                product.quantity = productQuantity
                product.save()
                buyer.acc_balance -= total_price
                buyer.save()
                seller.acc_balance += total_price
                seller.save()
                bought_item = BoughtItem.objects.create(
                        userId=buyer,
                        product=product,
                        quantity=boughtQuantity,
                        purchase_date=timezone.now()
                    )
                return JsonResponse({'message': 'Product bought successfully'}, status=200)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
  
    @staticmethod
    def getAllUserProducts(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                user_id = body_data.get('userId')
                user = User.objects.get(userId=user_id)
                products = Product.objects.filter(sellerId=user)
                products_list = []
                for product in products:
                    images = ProductImage.objects.filter(product=product)
                    product_data = {
                        'productId': product.productId,
                        'name': product.name,
                        'description': product.description,
                        'price': str(product.price),
                        'quantity': product.quantity,
                        'category_id': product.category_id,
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

