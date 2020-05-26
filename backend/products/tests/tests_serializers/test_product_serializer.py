# from django.test import TestCase, RequestFactory
# from model_mommy import mommy

# from products.serializers import ProductSerializer
# from products.models import Product


# class UserFieldsTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = mommy.make('CustomUser')
#         cls.product = mommy.make('Product', owner=cls.user)

#     def create_request_of_user(self, user):
#         request = RequestFactory().get('/')
#         request.user = user
#         return request

#     def test_user_product_field(self):
#         request = self.create_request_of_user(self.user)
#         serializer = ProductSerializer(
#             instance=self.product, context={'request': request})

#         data = serializer.data
#         import pdb
#         pdb.set_trace()

#     def test_user_subproduct_field_queryset(self):
#         pass

#     def test_user_packagingObject_field_queryset(self):
#         pass
