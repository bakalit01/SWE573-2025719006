import pytest
from django.core.management import call_command

from crafts.models import AttributeDefinition, Craft, Media

from .factories import AttributeDefinitionFactory, CraftFactory, CraftTypeFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestVisibility:
    """Craft.objects.visible_to() is the single gate for what a user may see."""

    @pytest.fixture
    def crafts(self):
        return {
            "public": CraftFactory(visibility=Craft.Visibility.PUBLIC),
            "members": CraftFactory(visibility=Craft.Visibility.MEMBERS),
            "community": CraftFactory(visibility=Craft.Visibility.COMMUNITY),
            "restricted": CraftFactory(visibility=Craft.Visibility.RESTRICTED),
            "draft": CraftFactory(status=Craft.Status.DRAFT),
        }

    def test_anonymous_sees_only_published_public(self, crafts):
        from django.contrib.auth.models import AnonymousUser

        visible = set(Craft.objects.visible_to(AnonymousUser()))
        assert visible == {crafts["public"]}

    def test_member_also_sees_members_only(self, crafts):
        visible = set(Craft.objects.visible_to(UserFactory()))
        assert visible == {crafts["public"], crafts["members"]}

    def test_staff_sees_everything(self, crafts):
        visible = set(Craft.objects.visible_to(UserFactory(is_staff=True)))
        assert visible == set(crafts.values())


class TestAttributes:
    def test_rows_use_definition_labels_units_and_skip_empty(self):
        craft_type = CraftTypeFactory()
        AttributeDefinitionFactory(
            craft_type=craft_type,
            key="height",
            label="Height",
            data_type="number",
            unit="cm",
            order=1,
        )
        AttributeDefinitionFactory(craft_type=craft_type, key="glaze", label="Glaze", order=2)
        AttributeDefinitionFactory(
            craft_type=craft_type,
            key="watertight",
            label="Watertight",
            data_type="boolean",
            order=3,
        )
        craft = CraftFactory(
            craft_type=craft_type, attributes={"height": 30, "glaze": "", "watertight": True}
        )
        assert craft.attribute_rows() == [("Height", "30 cm"), ("Watertight", "Yes")]

    def test_retired_definition_is_hidden_but_data_kept(self):
        definition = AttributeDefinitionFactory(label="Old field", is_active=False)
        craft = CraftFactory(craft_type=definition.craft_type, attributes={definition.key: "kept"})
        assert craft.attribute_rows() == []
        craft.refresh_from_db()
        assert craft.attributes[definition.key] == "kept"

    def test_multi_choice_is_joined(self):
        definition = AttributeDefinitionFactory(data_type="multi_choice")
        assert definition.display_value(["Glass", "Shell"]) == "Glass, Shell"


class TestSampleData:
    def test_seed_is_idempotent_and_labelled(self):
        call_command("seed_sample_data", fictional=True)
        counts = (Craft.objects.count(), Media.objects.count(), AttributeDefinition.objects.count())
        call_command("seed_sample_data", fictional=True)
        assert (
            Craft.objects.count(),
            Media.objects.count(),
            AttributeDefinition.objects.count(),
        ) == counts
        assert counts[0] >= 10
        assert not Craft.objects.filter(is_sample=False).exists()
        assert Craft.objects.values("craft_type").distinct().count() >= 4

    def test_every_sample_credits_maker_and_has_alt_text(self):
        call_command("seed_sample_data", fictional=True)
        assert not Craft.objects.filter(maker_credit="").exists()
        assert not Media.objects.filter(alt_text="").exists()
