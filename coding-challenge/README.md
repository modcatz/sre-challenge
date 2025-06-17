# Alert Processing System

This python script processes alert data to help SRE teams and DevOps engineers quickly identify and prioritize incidents. It provides functionality to:

- Parse JSON alert files
- Filter alerts by multiple criteria
- Group related alerts to reduce noise
- Calculate incident priority using a weighted algorithm

## Usage

Run the main demo:
```bash
python main.py
```

Run the test functions:
```bash
python test_functions.py
```

## Features

### 🔍 **Alert Filtering**
Filter alerts based on multiple criteria:
- **Severity level** (critical, warning, info)
- **Service name** 
- **Time window** (within the last X minutes)

### 📊 **Alert Grouping**
Group related alerts by service and component to reduce noise and provide better incident context.

### ⚡ **Priority Calculation**
Calculate incident priority using a weighted algorithm based on:
- **Severity** (critical=10, warning=5, info=1) - 50% weight
- **Average deviation from threshold** - 30% weight  
- **Number of affected components** - 20% weight

## Data Structure

### Input JSON Format
```json
{
  "alerts": [
    {
      "id": "ALT-1023",
      "timestamp": "2024-04-28T09:15:22Z",
      "service": "payment-processor",
      "component": "api-gateway",
      "severity": "critical",
      "metric": "latency",
      "value": 2300,
      "threshold": 1000,
      "description": "API response time exceeded threshold"
    }
  ]
}
```

### Required Fields
- `id`: Unique alert identifier
- `timestamp`: ISO 8601 timestamp
- `service`: Service name
- `component`: Component name
- `severity`: Alert severity (critical, warning, info)
- `metric`: Metric name
- `value`: Current metric value
- `threshold`: Threshold value
- `description`: Alert description



## Priority Algorithm

The incident priority is calculated using this weighted formula:

```
Priority = (Severity Score × 0.5) + (Average Deviation × 0.3) + (Affected Components × 0.2)
```

Where:
- **Severity Score**: Sum of severity weights for all alerts
- **Average Deviation**: Average percentage deviation from thresholds
- **Affected Components**: Number of unique (service, component) pairs