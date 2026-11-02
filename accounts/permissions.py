"""Who may do what (US-05). Views and templates call these; nothing relies on hidden buttons.

Roles: member < maker < steward < admin. Stewards act only for the communities they are
assigned to (Community.stewards). Superusers and staff count as admins.
"""


def is_site_admin(user):
    return bool(
        user
        and user.is_authenticated
        and user.is_active
        and (user.is_superuser or user.is_staff or user.role == user.Role.ADMIN)
    )


def can_contribute(user):
    """Add crafts and edit one's own. Members only browse."""
    return bool(
        user and user.is_authenticated and user.is_active and user.role != user.Role.MEMBER
    ) or is_site_admin(user)


def stewarded_community_ids(user):
    if not (user and user.is_authenticated and user.is_active):
        return set()
    if user.role != user.Role.STEWARD:
        return set()
    return set(user.stewarded_communities.values_list("pk", flat=True))


def is_steward_of(user, community_id):
    return is_site_admin(user) or community_id in stewarded_community_ids(user)


def can_review(user, craft):
    """Approve, reject or unpublish records, and see consent details."""
    return is_steward_of(user, craft.community_id)


def is_author(user, craft):
    return bool(user and user.is_authenticated and craft.created_by_id == user.pk)


def can_edit(user, craft):
    """Authors (makers and up), admins, and the community's stewards for submitted records
    (other people's drafts stay private to their author)."""
    if not (user and user.is_authenticated and user.is_active):
        return False
    if is_author(user, craft):
        return can_contribute(user)
    if is_site_admin(user):
        return True
    return craft.status != "draft" and is_steward_of(user, craft.community_id)


def can_delete(user, craft):
    """Only the author or an admin deletes; stewards unpublish instead (it is recorded)."""
    return (is_author(user, craft) and can_contribute(user)) or is_site_admin(user)


def can_edit_community(user, community):
    return is_steward_of(user, community.pk)
