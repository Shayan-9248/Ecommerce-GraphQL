from django.shortcuts import get_object_or_404

import graphene
import graphene_django
from graphql_jwt.decorators import staff_member_required

from .models import Product


class ProductType(graphene_django.DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID())

    def resolve_products(root, info, **kwargs):
        return Product.objects.filter(available=True)

    def resolve_product(root, info, **kwargs):
        return get_object_or_404(Product, pk=kwargs.get("id"))


class ProductInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    unit_price = graphene.Int()
    amount = graphene.Int()
    discount = graphene.Int()
    total_price = graphene.Int()


class CreateProduct(graphene.Mutation):
    class Arguments:
        product_input = ProductInput()

    ok = graphene.Boolean(default_value=False)
    product = graphene.Field(ProductType)

    @staff_member_required
    @staticmethod
    def mutate(root, info, product_input=None):
        product = Product(
            title=product_input.title,
            description=product_input.description,
            unit_price=product_input.unit_price,
            amount=product_input.amount,
            discount=product_input.discount,
            total_price=product_input.total_price,
        )
        product.save()
        ok = True
        return CreateProduct(product=product, ok=ok)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID()

    ok = graphene.Boolean(default_value=False)
    product = graphene.Field(ProductType)

    @staff_member_required
    def mutate(root, info, product_id):
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        ok = True
        return DeleteProduct(product=product, ok=ok)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    delete_product = DeleteProduct.Field()
