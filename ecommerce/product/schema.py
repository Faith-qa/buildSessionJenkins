# define schema
import graphene
from graphene import Mutation
from graphene_django import DjangoObjectType
from .models import Product, Order

# --------define types -----

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    total_price = graphene.Decimal()
    class Meta:
        model = Order
        fields = ("id", "product", "quantity", "created_at","total_price" )

    def resolve_total_price(self, info):
        return self.product.price * self.quantity()



#---------Queries ------
class Query(graphene.ObjectType):
    product = graphene.Field(ProductType, id= graphene.ID(required=True))
    products = graphene.List(ProductType)

    order = graphene.Field(OrderType, id= graphene.ID(required=True))
    orders = graphene.List(OrderType)

    def resolve_product(self, info, id):
        return Product.objects.filter(id=id).first()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_order(self, info, id):
        return Order.objects.filter(id=id).select_related("product").first()

    def resolve_orders(self, info, product_id=None):
        qs = Order.objects.select_related("product").all()
        if product_id is not None:
            qs = qs.filter(product_id=product_id)

        return qs

#---- Mutations -----

class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls, root, info, name, price, stock):
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class UpdateProduct(graphene.Mutation):
    class Argument:
        id = graphene.ID(required=True)
        name = graphene.String()
        price = graphene.Decimal()
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    @classmethod
    def mutate(cls,root, info, id, **kwargs):
        product = Product.objects.get(pk=id)
        for field, value in kwargs.items():
            if value is not None:
                setattr(product, field, value)
        product.save()
        return UpdateProduct(product=product)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)