import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()


# Mutation
#1
class CreateLink(graphene.Mutation):
    # Datos que va a regresar la operacion create, si tiene exito.
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    # se definen los parametros con los datos a insertar
    # NOTA: id no se pasa como parametro, porque se genera automaticamente
    #2
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    # Metodo mutate, es quien realiza la operacion
    # self, info son parametros obligatorios
    # despues de info, van los parametros de url, descripcion
    #3
    def mutate(self, info, url, description):
        # creamos un objeto tipo Link, llamado link y pasan los parametros
        # url y description.
        link = Link(url=url, description=description)
        # inserta en la base de datos el objeto creado.
        # equivale.. insert into link(..,..) values (..,..)
        link.save()

        # regresa los valores del objeto insertado
        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )

# exponer la operacion de Mutation
#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
