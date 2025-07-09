"""API class for BWT Water Softener with Registers endpoint."""

import asyncio
import json
import logging
from typing import Dict, List, Any

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)

class BwtRegistersApi:
    """API client for BWT water softener registers endpoint."""
    
    def __init__(self, host: str) -> None:
        """Initialize the registers API client."""
        self.host = host
        self.session = None
        self._close_session = False
        
    async def __aenter__(self):
        """Async context manager entry."""
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        
    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session and self._close_session:
            await self.session.close()
            self.session = None
            
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            self._close_session = True
        return self.session
    
    async def get_registers(self) -> List[int]:
        """Get the registers data from the device."""
        session = await self._get_session()
        url = f"http://{self.host}/silk/registers"
        
        try:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, dict) and "params" in data:
                            return data["params"]
                        elif isinstance(data, list):
                            return data
                        else:
                            _LOGGER.error("Unexpected response format: %s", data)
                            raise ValueError("Unexpected response format")
                    else:
                        _LOGGER.error("HTTP error %s when fetching registers", response.status)
                        raise aiohttp.ClientError(f"HTTP {response.status}")
                        
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout when fetching registers from %s", url)
            raise
        except aiohttp.ClientError as e:
            _LOGGER.error("HTTP error when fetching registers: %s", e)
            raise
        except Exception as e:
            _LOGGER.error("Unexpected error when fetching registers: %s", e)
            raise
    
    async def test_connection(self) -> bool:
        """Test if the registers endpoint is available."""
        try:
            await self.get_registers()
            return True
        except Exception:
            return False