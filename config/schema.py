import graphene

from accounts import schema as account_schema
from products import schema as product_schema
from carts import schema as cart_schema


class Query(
    account_schema.UserQuery, 
    product_schema.Query, 
    graphene.ObjectType
):
    pass


class Mutation(
    account_schema.Mutation,
    product_schema.Mutation,
    cart_schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
