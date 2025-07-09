"""Device firmware detection for BWT Perla integration."""

import asyncio
import logging
from typing import Optional

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)

async def determine_bwt_model(host: str) -> str:
    """Determine the BWT model based on available endpoints."""
    
    # First try the new registers endpoint
    if await _test_registers_endpoint(host):
        _LOGGER.debug("Registers endpoint detected at %s", host)
        return "perla_silk_registers"
    
    # Fall back to existing detection logic
    try:
        from bwt_api.bwt import determine_bwt_model as original_determine_bwt_model
        return await original_determine_bwt_model(host)
    except ImportError:
        _LOGGER.warning("bwt_api not available, falling back to basic detection")
        return "perla_silk"  # Default fallback

async def _test_registers_endpoint(host: str) -> bool:
    """Test if the registers endpoint is available."""
    try:
        async with aiohttp.ClientSession() as session:
            async with async_timeout.timeout(5):
                url = f"http://{host}/silk/registers"
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Check if response has expected structure
                        if isinstance(data, dict) and "params" in data:
                            return True
                        elif isinstance(data, list):
                            return True
    except Exception as e:
        _LOGGER.debug("Registers endpoint test failed: %s", e)
    
    return False