import factory
from django.utils.text import slugify

from accounts.models import User
from communities.models import Community
from crafts.models import AttributeDefinition, Craft, CraftType


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    display_name = factory.Sequence(lambda n: f"User {n}")
    password = factory.PostGenerationMethodCall("set_password", "Correct-Horse-42")

    @factory.post_generation
    def _save(obj, create, extracted, **kwargs):  # noqa: N805
        if create:
            obj.save()


class CommunityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Community

    name = factory.Sequence(lambda n: f"Community {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    region = "Somewhere"


class CraftTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CraftType

    name = factory.Sequence(lambda n: f"Craft type {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))


class AttributeDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttributeDefinition

    craft_type = factory.SubFactory(CraftTypeFactory)
    key = factory.Sequence(lambda n: f"field_{n}")
    label = factory.Sequence(lambda n: f"Field {n}")


class CraftFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Craft

    title = factory.Sequence(lambda n: f"Craft {n}")
    slug = factory.LazyAttribute(lambda o: slugify(o.title))
    craft_type = factory.SubFactory(CraftTypeFactory)
    community = factory.SubFactory(CommunityFactory)
    maker_credit = "A maker"
    visibility = Craft.Visibility.PUBLIC
    status = Craft.Status.PUBLISHED
