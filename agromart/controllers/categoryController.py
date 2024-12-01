from django.http import JsonResponse
from ..models import Category
import uuid, json

class categoryController:
    @staticmethod
    def addCategory(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                name = body_data.get('name')
                print("name",name)

                new_category = Category(
                    categoryId=uuid.uuid4(),
                    categoryname=name
                )
                new_category.save()
                return JsonResponse({'message': 'Category added successfully'}, status=201)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @staticmethod
    def editCategory(request, category_id):
        if request.method == 'PUT':
            try:
                category = Category.objects.get(categoryId=category_id)
                category.categoryname = request.POST.get('categoryname')
                category.save()
                return JsonResponse({'message': 'Category updated successfully'})
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @staticmethod
    def deleteCategory(request):
        if request.method == 'POST':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                categoryId = body_data.get('categoryId')
                category = Category.objects.get(categoryId=categoryId)
                category.delete()
                return JsonResponse({'message': 'Category deleted successfully'})
            except Category.DoesNotExist:
                return JsonResponse({'error': 'Category not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)

    @staticmethod
    def getAllCategories(request):
        if request.method == 'GET':
            try:
                categories = Category.objects.all()
                categories_list = [{'categoryId': category.categoryId,
                                    'categoryname': category.categoryname} for category in categories]
                return JsonResponse({'categories': categories_list})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
