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


class Review(View):
    def get(self, request):
        product_id = request.GET.get('product_id', None)
        user_id = request.GET.get('user_id', None)
        review_id = request.GET.get('review_id', None)

        if product_id:
            review_data = ProductReview.objects.filter(product_id=product_id).values()
            review_list = [review for review in review_data]
        elif user_id:
            review_data = ProductReview.objects.filter(user_id=user_id).values()
            review_list = [review for review in review_data]
        elif review_id:
            review_data = ProductReview.objects.filter(id=review_id).values()
            review_list = [review for review in review_data]
            if len(review_list) == 0:
                return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status=404)

        return JsonResponse({'REVIEWS': review_list}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        target_product = Product.objects.get(id=data['product_id'])

        if ProductReview.objects.filter(product=data['product_id'], user=data['user_id']).exists():
            return JsonResponse({'MESSAGE': 'ALREADY_WROTE_REVIEW'}, status=400)
        else:
            ProductReview(
                user=User.objects.get(id=data['user_id']),
                product=target_product,
                rating=data['rating'],
                title=data['title'],
                content=data['content'],
                image_url=data['image_url'],
            ).save()

            return JsonResponse({'MESSAGE': 'REVIEW_UPLOADED'}, status=201)

    def patch(self, request):
        data = json.loads(request.body)
        target_review = ProductReview.objects.get(id=data['review_id'])

        if not ProductReview.objects.filter(id=target_review.id).exists():
            return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status=404)
        else:
            ProductReview.objects.filter(id=target_review.id).update(
                rating=data['rating'],
                title=data['title'],
                content=data['content'],
                image_url=data['image_url'],
                updated_at=timezone.now(),
            )
            return JsonResponse({'MESSAGE': 'REVIEW_UPDATED'}, status=201)

    def delete(self, request):
        data = json.loads(request.body)
        target_review = ProductReview.objects.get(id=data['review_id'])

        if not ProductReview.objects.filter(id=target_review.id).exists():
            return JsonResponse({'MESSAGE': 'REVIEW_DOES_NOT_EXIST'}, status=404)
        else:
            ProductReview.objects.filter(id=target_review.id).delete()
            return JsonResponse({'MESSAGE': 'REVIEW_DELETED'}, status=200)
