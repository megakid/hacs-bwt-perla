from .data import ApiData
from datetime import datetime, timedelta
import logging

_LOGGER = logging.getLogger(__name__)

class SilkRegistersApiData(ApiData):
    """Data class for BWT Water Softener Silk Registers API data."""
    _registers: list[int]

    def __init__(self, registers: list[int]) -> None:
        """Initialize the SilkRegistersApiData with a list of registers."""
        self._registers = registers
    
    def current_flow(self) -> int:
        """Current flow rate in L/s converted to L/h."""
        flow_ls = self.get_register(FLOW_RATE_LS)
        return flow_ls * 3600 if flow_ls is not None else 0  # Convert L/s to L/h

    def total_output(self) -> int:
        """Total water served in liters."""
        return (self.get_register(TOTAL_WATER_SERVED) or 0) * 100

    def hardness_in(self):
        """Input water hardness - not available in this API."""
        return None

    def regenerativ_level(self) -> int:
        """Current salt level percentage."""
        current_salt = self.get_register(CURRENT_SALT_LEVEL)
        max_salt = self.get_register(MAX_SALT_CAPACITY)
        if current_salt is not None and max_salt is not None and max_salt > 0:
            return int((current_salt / max_salt) * 100)
        return 0
    
    def day_output(self) -> int:
        """Daily water usage."""
        return self.get_register(TODAY_WATER_USE) or 0
    
    def capacity_1(self) -> int:
        """Current capacity remaining."""
        return self.get_register(CURRENT_CAPACITY) or 0
    
    def capacity_percentage(self) -> int:
        """Current capacity percentage."""
        current_capacity = self.get_register(CURRENT_CAPACITY)
        if current_capacity is not None:
            return int((current_capacity / 2630) * 100)
        return 0
    
    def last_regeneration_1(self) -> datetime | None:
        """Last regeneration time - not available in this API."""
        return None
    
    def days_in_service(self) -> int:
        """Days in service."""
        return self.get_register(DAYS_IN_SERVICE) or 0
    
    def warranty_days_remaining(self) -> int:
        """Warranty days remaining."""
        return self.get_register(WARRANTY_DAYS_REMAINING) or 0
    
    def regeneration_count_1(self) -> int:
        """Total recharges count."""
        return self.get_register(TOTAL_RECHARGES) or 0
    
    def daily_average_water_use(self) -> int:
        """Daily average water use."""
        return self.get_register(DAILY_AVERAGE_WATER_USE) or 0
    
    def max_salt_capacity(self) -> float:
        """Maximum salt capacity in kg."""
        capacity = self.get_register(MAX_SALT_CAPACITY)
        return (capacity / 10.0) if capacity is not None else 0.0
    
    def current_salt_level(self) -> float:
        """Current salt level in kg."""
        level = self.get_register(CURRENT_SALT_LEVEL)
        return (level / 10.0) if level is not None else 0.0

    def get_register(self, index: int) -> int | None:
        """Get register value by index."""
        if index < 0 or index >= len(self._registers):
            return None
        return self._registers[index]

# Register indices based on the provided configuration
DAILY_AVERAGE_WATER_USE = 14
TOTAL_WATER_SERVED = 15
FLOW_RATE_LS = 16
DAYS_IN_SERVICE = 17
TOTAL_RECHARGES = 19
CURRENT_CAPACITY = 23
MAX_SALT_CAPACITY = 30
CURRENT_SALT_LEVEL = 31
WARRANTY_DAYS_REMAINING = 34
TODAY_WATER_USE = 42