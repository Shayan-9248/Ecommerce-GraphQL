from django.shortcuts import get_object_or_404

import graphene
import graphene_django

from .models import Cart, CartItem


class CartType(graphene_django.DjangoObjectType):
    class Meta:
        model = Cart


class CartItemType(graphene_django.DjangoObjectType):
    class Meta:
        model = CartItem


# class CartQuery(graphene.ObjectType):
#     carts = graphene.List(CartType)
#     cart = graphene.Field(CartType)

#     def resolve_carts(root, info, **kwargs):
#         return Cart.objects.filter(user_id=root.request.user.id)


class CreateCart(graphene.Mutation):
    class Arguments:
        pass

    ok = graphene.Boolean(default_value=True)
    cart = graphene.Field(CartType)

    def mutate(root, info):
        cart = Cart()
        cart.save()
        ok = True
        return CreateCart(cart=cart, ok=ok)


class Mutation(graphene.ObjectType):
    create_cart = CreateCart.Field()
