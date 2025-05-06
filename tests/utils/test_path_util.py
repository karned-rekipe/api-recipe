import pytest
from unittest.mock import patch

from utils.path_util import is_unprotected_path, is_unlicensed_path


def test_is_unprotected_path_with_protected_path():
    with patch('utils.path_util.UNPROTECTED_PATHS', ['/docs', '/favicon.ico']):
        # Test with a path that is not in UNPROTECTED_PATHS
        assert not is_unprotected_path('/api/v1/items')
        
        # Test with a path that is in UNPROTECTED_PATHS but with different case
        assert is_unprotected_path('/DOCS')
        
        # Test with a path that is in UNPROTECTED_PATHS
        assert is_unprotected_path('/docs')


def test_is_unlicensed_path_with_licensed_path():
    with patch('utils.path_util.UNLICENSED_PATHS', ['/health', '/metrics']):
        # Test with a path that is not in UNLICENSED_PATHS
        assert not is_unlicensed_path('/api/v1/items')
        
        # Test with a path that is in UNLICENSED_PATHS but with different case
        assert is_unlicensed_path('/HEALTH')
        
        # Test with a path that is in UNLICENSED_PATHS
        assert is_unlicensed_path('/health')


def test_is_unprotected_path_with_empty_list():
    with patch('utils.path_util.UNPROTECTED_PATHS', []):
        # Test with any path when UNPROTECTED_PATHS is empty
        assert not is_unprotected_path('/docs')
        assert not is_unprotected_path('/api/v1/items')


def test_is_unlicensed_path_with_empty_list():
    with patch('utils.path_util.UNLICENSED_PATHS', []):
        # Test with any path when UNLICENSED_PATHS is empty
        assert not is_unlicensed_path('/health')
        assert not is_unlicensed_path('/api/v1/items')