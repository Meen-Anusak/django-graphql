import graphene
from graphene_django import DjangoObjectType
from .models import  Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")



class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        
    ingredient = graphene.Field(IngredientType)
    
    @classmethod
    def mutate(cls,root,info,id,name,notes):
        ingredient = Ingredient.objects.get(pk=id)
        ingredient.name = name
        ingredient.notes = notes
        ingredient.save()
        
        return UpdateIngredient(ingredient=ingredient)


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

class Mutations(graphene.ObjectType):
    update_ingredient = UpdateIngredient.Field()



schema = graphene.Schema(query=Query, mutation=Mutations)

