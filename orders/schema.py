from graphql_jwt.decorators import login_required

import graphene
import graphene_django

from .models import Order, OrderItem
from carts.models import Cart


class OrderType(graphene_django.DjangoObjectType):
    class Meta:
        model = Order


class OrderItemType(graphene_django.DjangoObjectType):
    class Meta:
        model = OrderItem


class OrderInput(graphene.InputObjectType):
    user_id = graphene.ID()
    product_id = graphene.ID()
    order_id = graphene.ID()


class CreateOrder(graphene.Mutation):
    class Arguments:
        # order_input = OrderInput()
        pass
    
    ok = graphene.Boolean(default_value=False)
    order = graphene.Field(OrderItemType)

    @login_required
    def mutate(root, info):
        order = Order.objects.create(user_id=info.context.user.id)

        cart = Cart.objects.filter(user_id=info.context.user.id)
        for c in cart:
            OrderItem.objects.create(
                product_id=c.product.id,
                order_id=order.id,
                quantity=c.quantity
            )
        ok = True
        return CreateOrder(order=order, ok=ok)


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
