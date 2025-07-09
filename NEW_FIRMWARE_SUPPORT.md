# BWT Water Softener - New Registers API Support

## Overview

This integration now supports BWT water softeners with the new registers API firmware. This firmware exposes a simplified `/silk/registers` endpoint that provides water usage and salt monitoring data without requiring a login code.

## Features

### Automatic Detection
- The integration automatically detects if your device supports the new registers API
- No manual configuration required - just enter your device's IP address
- Falls back to existing API methods if the new endpoint is not available

### New Sensor Entities

When using the new registers API, you'll get these additional sensors:

| Sensor | Description | Unit |
|--------|-------------|------|
| **Daily Average Water Use** | Average daily water consumption | L |
| **Flow Rate** | Current water flow rate | L/s |
| **Total Water Served** | Total water output since installation | L |
| **Today's Water Use** | Water consumption for today | L |
| **Days in Service** | Number of days the device has been active | days |
| **Total Recharges** | Total number of regeneration cycles | count |
| **Current Capacity** | Remaining water capacity | L |
| **Current Capacity Percentage** | Percentage of capacity remaining | % |
| **Warranty Days Remaining** | Days left on warranty | days |
| **Max Salt Capacity** | Maximum salt capacity | kg |
| **Current Salt Level** | Current salt level | kg |
| **Salt Level Percentage** | Percentage of salt remaining | % |

## Installation

1. Install the BWT Perla integration through HACS
2. Go to Settings > Devices & Services > Add Integration
3. Search for "BWT Perla"
4. Enter your device's IP address
5. The integration will automatically detect the firmware type and configure appropriate sensors

## Configuration

### For New Registers API (No Login Required)
- Simply enter the IP address of your BWT water softener
- The integration will detect the `/silk/registers` endpoint
- No login code required

### For Legacy API (Login Required)
- Enter the IP address
- Provide the login code sent to you during device registration
- The integration will use the traditional API endpoints

## Benefits of New Registers API

- **No Authentication Required**: No need for login codes or device registration
- **Enhanced Water Monitoring**: More detailed water usage statistics
- **Salt Management**: Precise salt level monitoring in kilograms
- **Capacity Tracking**: Real-time capacity percentage monitoring
- **Simplified Setup**: Just IP address configuration

## API Endpoint Details

The new firmware exposes data through:
```
http://<device-ip>/silk/registers
```

Response format:
```json
{
  "params": [0, -1, 18, 23, 285, 29, 16, 2, 0, 9, 8, 1, 8, 4, 296, 158, 0, 52, 2138, 9, 40, 0, 100, 2275, 11, 20, 50, 1, 1, 0, 160, 141, 20, 0, 678, 1, -1, -1, 6, 1, 1, 15, 355, -1, -1, -1, -1, 0]
}
```

## Troubleshooting

### Device Not Detected
- Ensure your BWT water softener is connected to the same network
- Check that the IP address is correct
- Verify the device is accessible: `http://<ip>/silk/registers`

### Missing Sensors
- The integration shows different sensors based on firmware capabilities
- Legacy devices will show traditional BWT Perla sensors
- New registers API devices will show enhanced water and salt monitoring

### Connection Issues
- Check network connectivity
- Ensure firewall allows access to the device
- Verify the device is powered on and operational

## Technical Details

The integration uses intelligent firmware detection:
1. First attempts to connect to `/silk/registers` endpoint
2. If successful, uses the new registers API data structure
3. Falls back to existing BWT API detection if registers endpoint is unavailable
4. Automatically configures appropriate sensors for detected firmware

This ensures backward compatibility while providing enhanced functionality for newer firmware versions.