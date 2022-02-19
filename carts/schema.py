from graphql_jwt.decorators import login_required

import graphene
import graphene_django

from .models import Cart


class CartType(graphene_django.DjangoObjectType):
    class Meta:
        model = Cart


class CartInput(graphene.InputObjectType):
    quantity = graphene.Int()
    product_id = graphene.ID()


class CreateCart(graphene.Mutation):
    class Arguments:
        cart_input = CartInput(required=True)

    ok = graphene.Boolean(default_value=True)
    cart = graphene.Field(CartType)

    @login_required
    def mutate(root, info, cart_input):
        cart = Cart(
            user_id=info.context.user.id,
            product_id=cart_input.product_id,
            quantity=cart_input.quantity,
        )
        cart.save()
        ok = True
        return CreateCart(cart=cart, ok=ok)


class Mutation(graphene.ObjectType):
    create_cart = CreateCart.Field()
