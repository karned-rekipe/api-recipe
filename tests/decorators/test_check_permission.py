import pytest

from decorators.check_permission import check_roles
from fastapi import HTTPException, status


def test_check_roles_sufficient_permissions():
    user_roles = {'api-recipe': ['admin', 'editor']}
    required_permissions = ['editor']

    check_roles(user_roles, required_permissions)


def test_check_roles_insufficient_permissions():
    user_roles = {'api-recipe': ['reader']}
    required_permissions = ['editor', 'writer']

    with pytest.raises(HTTPException) as e:
        check_roles(user_roles, required_permissions)

    assert e.value.status_code == status.HTTP_403_FORBIDDEN
    assert "Insufficient permissions !" in str(e.value.detail)
    assert "Need : api-recipe/editor, api-recipe/writer" in str(e.value.detail)
    assert "Got : api-recipe/reader" in str(e.value.detail)
