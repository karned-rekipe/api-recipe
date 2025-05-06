import pytest
import logging
import asyncio
from unittest.mock import patch, MagicMock

from decorators.log_time import log_time, log_time_async


def test_log_time_decorator():
    # Create a test function
    @log_time
    def test_function(x, y):
        return x + y
    
    # Mock the logging.info method
    with patch('logging.info') as mock_log:
        # Call the decorated function
        result = test_function(5, 3)
        
        # Check that the function returns the correct result
        assert result == 8
        
        # Check that logging.info was called twice (start and end)
        assert mock_log.call_count == 2
        
        # Check the content of the first log message (start)
        first_call_args = mock_log.call_args_list[0][0]
        assert "test_function: Start" in first_call_args[0]
        
        # Check the content of the second log message (end)
        second_call_args = mock_log.call_args_list[1][0]
        assert "test_function: End" in second_call_args[0]
        assert "Execution time:" in second_call_args[0]


@pytest.mark.asyncio
async def test_log_time_async_decorator():
    # Create a test async function
    @log_time_async
    async def test_async_function(x, y):
        await asyncio.sleep(0.01)  # Small delay to ensure measurable execution time
        return x * y
    
    # Mock the logging.info method
    with patch('logging.info') as mock_log:
        # Call the decorated async function
        result = await test_async_function(4, 7)
        
        # Check that the function returns the correct result
        assert result == 28
        
        # Check that logging.info was called twice (start and end)
        assert mock_log.call_count == 2
        
        # Check the content of the first log message (start)
        first_call_args = mock_log.call_args_list[0][0]
        assert "test_async_function: Start" in first_call_args[0]
        
        # Check the content of the second log message (end)
        second_call_args = mock_log.call_args_list[1][0]
        assert "test_async_function: End" in second_call_args[0]
        assert "Execution time:" in second_call_args[0]


def test_log_time_with_exception():
    # Create a test function that raises an exception
    @log_time
    def test_function_with_exception():
        raise ValueError("Test exception")
    
    # Mock the logging.info method
    with patch('logging.info') as mock_log:
        # Call the decorated function and expect an exception
        with pytest.raises(ValueError, match="Test exception"):
            test_function_with_exception()
        
        # Check that logging.info was called at least once (for the start)
        assert mock_log.call_count >= 1
        
        # Check the content of the first log message (start)
        first_call_args = mock_log.call_args_list[0][0]
        assert "test_function_with_exception: Start" in first_call_args[0]


@pytest.mark.asyncio
async def test_log_time_async_with_exception():
    # Create a test async function that raises an exception
    @log_time_async
    async def test_async_function_with_exception():
        await asyncio.sleep(0.01)  # Small delay
        raise ValueError("Test async exception")
    
    # Mock the logging.info method
    with patch('logging.info') as mock_log:
        # Call the decorated async function and expect an exception
        with pytest.raises(ValueError, match="Test async exception"):
            await test_async_function_with_exception()
        
        # Check that logging.info was called at least once (for the start)
        assert mock_log.call_count >= 1
        
        # Check the content of the first log message (start)
        first_call_args = mock_log.call_args_list[0][0]
        assert "test_async_function_with_exception: Start" in first_call_args[0]