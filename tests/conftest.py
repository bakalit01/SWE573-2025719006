import os

import pytest

from crafts.models import AttributeDefinition

from .factories import (
    AttributeDefinitionFactory,
    CommunityFactory,
    CraftTypeFactory,
    UserFactory,
)

PASSWORD = "Correct-Horse-42"


@pytest.fixture
def password():
    return PASSWORD


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def member_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def setup(db):
    """A craft type with a text and a choice field, and a community (add-form tests)."""
    craft_type = CraftTypeFactory(name="Carving", slug="carving")
    AttributeDefinitionFactory(craft_type=craft_type, key="tools", label="Tools")
    AttributeDefinitionFactory(
        craft_type=craft_type,
        key="finish",
        label="Finish",
        data_type=AttributeDefinition.DataType.CHOICE,
        options=["Oiled", "Waxed"],
    )
    return {"type": craft_type, "community": CommunityFactory()}


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Use a pre-installed Chromium when PLAYWRIGHT_CHROMIUM_EXECUTABLE is set."""
    path = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    return {**browser_type_launch_args, **({"executable_path": path} if path else {})}
