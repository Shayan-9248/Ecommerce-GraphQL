from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from graphql_jwt.decorators import staff_member_required
import graphene
import graphene_django
import graphql_jwt

User = get_user_model()


class UserType(graphene_django.DjangoObjectType):
    class Meta:
        model = User
        fields = ("username", "email", "password")
    

class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID())
    users = graphene.List(UserType)

    def resolve_user(root, info, **kwargs):
        return get_object_or_404(User, pk=kwargs.get("id"))
    
    @staff_member_required
    def resolve_users(root, info, *kwargs):
        return User.objects.all()    


class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    password = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_input = UserInput(required=True)
    
    ok = graphene.Boolean(default_value=False)
    user = graphene.Field(UserType)

    def mutate(root, info, user_input):
        user = User(
            username=user_input.username,
            email=user_input.email,
            password=user_input.password
        )
        user.save()
        ok = True
        return CreateUser(user=user, ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
