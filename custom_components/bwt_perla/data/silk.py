from .data import ApiData
from datetime import datetime, timedelta

class SilkApiData(ApiData):
    """Data class for BWT Perla Silk API data."""
    _registers: list[int]

    def __init__(self, registers: list[int]) -> None:
        """Initialize the SilkApiData with a list of registers."""
        self._registers = registers
    
    def current_flow(self) -> int:
        return self._registers[CURRENT_FLOW_RATE]

    def total_output(self) -> int:
        return self._registers[TOTAL_WATER_SERVED]

    def hardness_in(self):
        return self._registers[WATER_HARDNESS]
    
    def hardness_out(self):
        # We don't yet get the outgoing hardness. For the calculated entity -1 means we just return the original value.
        return self._registers[WATER_HARDNESS] -1

    def customer_service(self) -> int:
        service_days = self._registers[DAYS_UNTIL_SERVICE]
        return (datetime.now().astimezone() + timedelta(days=service_days)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)

    def regenerativ_level(self) -> int:
        return int(self._registers[REGENERATIV_REMAINING] / self._registers[REGENERATIV_CAPACITY] * 100)
    
    def day_output(self) -> int:
        return self._registers[DAILY_WATER_USAGE]
    
    def capacity_1(self) -> int:
        return self._registers[REMAINING_CAPACITY]
    
    def last_regeneration_1(self) -> datetime:
        hour = self._registers[LAST_REGENERATION_HOUR]
        minute = self._registers[LAST_REGENERATION_MINUTE]
        now = datetime.now().astimezone()
        if hour < now.hour or (hour == now.hour and minute <= now.minute):
            # today
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # yesterday
        return now.replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(days=1)
    
    def register(self, index: int) -> int | None:
        if index < 0 or index >= len(self._registers):
            return None
        return self._registers[index]

# Maybe salt type?
CURRENT_HOUR = 2
CURRENT_MINUTE = 3
# ppm
WATER_HARDNESS = 4

LAST_REGENERATION_HOUR = 7
LAST_REGENERATION_MINUTE = 8

BASE_MODEL_NUMBER = 10
DUPLEX_SETTING = 11

TURBINE_PULSES_PER_LITER = 13
AVG_WATER_SERVED_PER_DAY = 14
TOTAL_WATER_SERVED = 15
CURRENT_FLOW_RATE = 16
DAYS_IN_SERVICE = 17
WARRANTY_DAYS_REMAINING = 18
TOTAL_NUMBER_OF_RECHARGES = 19

REMAINING_CAPACITY = 23

DWELL_DURATION = 25
BRINE_DURATION = 26
ALLOW_CHANGING_SALT_TYPE = 27
ALLOW_CHANGING_REGEN_TIME = 28

REGENERATIV_CAPACITY = 30
REGENERATIV_REMAINING = 31

DAYS_UNTIL_SERVICE = 34

DAILY_WATER_USAGE = 43
