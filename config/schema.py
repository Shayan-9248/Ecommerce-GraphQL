import graphene

from accounts import schemas as account_schema


class Query(account_schema.UserQuery, graphene.ObjectType):
    pass


class Mutation(account_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
