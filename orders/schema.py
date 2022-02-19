import graphene
import graphene_django

from .models import Order, OrderItem
# from carts.models import Cart


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
        order_input = OrderInput()
    
    ok = graphene.Boolean(default_value=False)
    order = graphene.Field(OrderItemType)

    def mutate(root, info, order_input):
        order = Order.objects.create(user_id=info.context.user.id)

        # cart = Cart.objects.filter()
