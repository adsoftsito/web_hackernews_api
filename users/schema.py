# se importa el modulo de manejo de usuarios de django
from django.contrib.auth import get_user_model

# se importa el modulo graphene para usar operaciones Graphql
import graphene
# se importa los tipos de datos permitidos por Django
from graphene_django import DjangoObjectType

#  define un objeto UserType del modelo de usuarios de Django
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

#Query
# ...code
class Query(graphene.ObjectType):
    # operacion query para verificar un token, y regresar el usuario
    me = graphene.Field(UserType)
    
    # objeto de retorno : Lista de usuarios
    users = graphene.List(UserType)

    # metodo resolve_users ejecuta el query
    # self, info son parametros obligatorios
    def resolve_users(self, info):
        # regresa todos los usuarios guardados
        # equivale a: select * from users
        return get_user_model().objects.all()
    
    # metodo resolve_me
    # self, info son obligatorios
    # info ==> guarda informacion del usuario activo
    def resolve_me(self, info):
        # obtiene el usuario activo de info y se guarda en user
        user = info.context.user

        # si no pasamos un token
        if user.is_anonymous:
            # lanza una exception controlada y termina el proceso
            raise Exception('Not logged in!')

        # si hay un usuario activo (token) regreso el objeto user 
        return user


# Mutation para crear un usuario
class CreateUser(graphene.Mutation):
    # define el objeto de retorno
    # user ( id, username, email, name, lastname......)
    user = graphene.Field(UserType)

    # para crear un usuario nuevo solo pedira :  username, password, email
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    # self, info son obligatorios
    # despues de info, van los parametros username, password, email

    def mutate(self, info, username, password, email):
        # se crea el objeto user, de tipo User (Django) y se le pasan username, email
        user = get_user_model()(
            username=username,
            email=email,
        )
        # se encripta el password, por razones de seguridad
        user.set_password(password)
        # se guarda en la base de datos
        user.save()

        # se retorna el ojeto user completo
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
