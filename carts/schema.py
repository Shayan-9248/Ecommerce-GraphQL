import graphene
import graphene_django

from .models import Cart, CartItem


class CartType(graphene_django.DjangoObjectType):
    class Meta:
        model = Cart


class CartItemType(graphene_django.DjangoObjectType):
    class Meta:
        model = CartItem


class CartItemInput(graphene.InputObjectType):
    quantity = graphene.Int()
    product_id = graphene.ID()
    cart_id = graphene.ID()


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


class CreateCartItem(graphene.Mutation):
    class Arguments:
        cart_item_input = CartItemInput(required=True)

    ok = graphene.Boolean(default_value=True)
    cart_item = graphene.Field(CartItemType)

    def mutate(root, info, cart_item_input):
        cart_item = CartItem(
            cart_id=cart_item_input.cart_id,
            product_id=cart_item_input.product_id,
            quantity=cart_item_input.quantity,
        )
        cart_item.save()
        ok = True
        return CreateCartItem(cart_item=cart_item, ok=ok)


class Mutation(graphene.ObjectType):
    create_cart = CreateCart.Field()
    create_cart_item = CreateCartItem.Field()
