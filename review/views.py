# autopep8: off
import json

from django.views           import View
from pathlib                import Path
from django.http            import JsonResponse
from django.db              import IntegrityError
from django.core            import serializers
from django.core.exceptions import FieldError
from django.http            import JsonResponse
from django.utils           import timezone
from user.models            import User
from product.models         import Product
from review.models          import ProductReview
from django.db.models       import Avg

class Review(View):
    def get(self, request):
        try:
            product_id = request.GET.get('product_id', None)
            user_id    = request.GET.get('user_id', None)
            review_id  = request.GET.get('review_id', None)

            if product_id:
                review_data = ProductReview.objects.filter(product_id=product_id)
                review_list = [review for review in review_data.values()]
                average     = review_data.aggregate(Avg('rating'))

            elif user_id:
                review_data = ProductReview.objects.filter(user_id=user_id)
                review_list = [review for review in review_data.values()]
                average     = review_data.aggregate(Avg('rating'))
            elif review_id:
                review_data = ProductReview.objects.filter(id=review_id)
                review_list = [review for review in review_data.values()]
                average     = review_data.aggregate(Avg('rating'))

                if len(review_list) == 0:
                    return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

            average_round = (average['rating__avg'] * 2) / 2

            return JsonResponse({'data': review_list, 'average_rating' : average_round}, status=200)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except ProductReview.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

    def post(self, request):
        try:
            data = json.loads(request.body)
            target_product = Product.objects.get(id=data['product_id'])

            if ProductReview.objects.filter(product=data['product_id'], user=data['user_id']).exists():
                return JsonResponse({'message': 'ALREADY_WROTE_REVIEW'}, status=400)
            else:
                ProductReview(
                    user      = User.objects.get(id=data['user_id']),
                    product   = target_product,
                    rating    = data['rating'],
                    title     = data['title'],
                    content   = data['content'],
                    image_url = data['image_url'],
                ).save()

                return JsonResponse({'message': 'REVIEW_UPLOADED'}, status=201)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except FieldError:
            return JsonResponse({'message': 'FIELD_ERROR'}, status=400)

    def patch(self, request):
        try:
            data = json.loads(request.body)
            target_review = ProductReview.objects.get(id=data['review_id'])

            if not target_review:
                return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

            if data['rating']: target_review.rating       = data['rating']
            if data['title']: target_review.title         = data['title']
            if data['content']: target_review.content     = data['content']
            if data['image_url']: target_review.image_url = data['image_url']

            target_review.updated_at = timezone.now()

            target_review.save()

            return JsonResponse({'message': 'REVIEW_UPDATED'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except ProductReview.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)


    def delete(self, request):
        try:
            data = json.loads(request.body)
            target_review = ProductReview.objects.get(id=data['review_id'])

            if not ProductReview.objects.filter(id=target_review.id).exists():
                return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)
            else:
                ProductReview.objects.filter(id=target_review.id).delete()
                return JsonResponse({'message': 'REVIEW_DELETED'}, status=200)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
        except ProductReview.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_DOES_NOT_EXIST'}, status=404)

