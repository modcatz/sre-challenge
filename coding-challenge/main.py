import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class SeverityLevel(Enum):
    """Enum for alert severity levels with priority weights"""
    CRITICAL = ("critical", 10)
    WARNING = ("warning", 5)
    INFO = ("info", 1)

    def __init__(self, label: str, weight: int):
        self.label = label
        self.weight = weight


@dataclass
class Alert:
    """Data class representing an alert"""
    id: str
    timestamp: str
    service: str
    component: str
    severity: str
    metric: str
    value: float
    threshold: float
    description: str
    
    def get_datetime(self) -> datetime:
        """Convert timestamp string to datetime object"""
        # Handle 'Z' suffix for UTC
        timestamp = self.timestamp.replace('Z', '+00:00')
        return datetime.fromisoformat(timestamp)
    
    def get_deviation_percentage(self) -> float:
        """Calculate percentage deviation from threshold"""
        if self.threshold == 0:
            return 0.0
        return ((self.value - self.threshold) / self.threshold) * 100


@dataclass
class AlertGroup:
    """Data class representing a group of related alerts"""
    service: str
    component: str
    alerts: List[Alert] = field(default_factory=list)
    severity_counts: Dict[str, int] = field(default_factory=dict)
    total_alerts: int = 0
    
    def add_alert(self, alert: Alert):
        """Add an alert to the group"""
        self.alerts.append(alert)
        self.severity_counts[alert.severity] = self.severity_counts.get(alert.severity, 0) + 1
        self.total_alerts = len(self.alerts)


class AlertProcessor:
    """Main class for processing and analyzing alerts"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.alerts: List[Alert] = []
        self.load_alerts()
    
    def load_alerts(self) -> bool:
        """Load and parse alerts from JSON file"""
        try:
            if not os.path.exists(self.file_path):
                print(f"Error: File not found - {self.file_path}")
                return False
            
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            if 'alerts' not in data or not isinstance(data['alerts'], list):
                print("Error: Invalid JSON structure - missing 'alerts' array")
                return False
            
            self.alerts = []
            for alert_data in data['alerts']:
                try:
                    alert = Alert(**alert_data)
                    self.alerts.append(alert)
                except Exception as e:
                    print(f"Warning: Skipping invalid alert - {e}")
            
            print(f"Successfully loaded {len(self.alerts)} alerts")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format - {e}")
            return False
        except Exception as e:
            print(f"Error: Failed to load alerts - {e}")
            return False
    
    def filter_alerts(self, 
                     severity: Optional[str] = None,
                     service: Optional[str] = None,
                     time_window_minutes: Optional[int] = None) -> List[Alert]:
        """
        Filter alerts based on multiple criteria
        
        Args:
            severity: Filter by severity level (critical, warning, info)
            service: Filter by service name
            time_window_minutes: Filter alerts within last X minutes
            
        Returns:
            List of filtered alerts
        """
        filtered_alerts = self.alerts.copy()
        
        # Filter by severity
        if severity:
            severity = severity.lower()
            filtered_alerts = [alert for alert in filtered_alerts 
                             if alert.severity.lower() == severity]
        
        # Filter by service
        if service:
            service = service.lower()
            filtered_alerts = [alert for alert in filtered_alerts 
                             if alert.service.lower() == service]
        
        # Filter by time window
        if time_window_minutes:
            # Use UTC timezone to match the alert timestamps
            cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)
            filtered_alerts = [alert for alert in filtered_alerts 
                             if alert.get_datetime() >= cutoff_time]
        
        return filtered_alerts
    
    def group_alerts(self, alerts: Optional[List[Alert]] = None) -> List[AlertGroup]:
        """
        Group related alerts to reduce noise
        
        Args:
            alerts: List of alerts to group (uses all alerts if None)
            
        Returns:
            List of alert groups
        """
        if alerts is None:
            alerts = self.alerts
        
        # Group by service and component
        groups_dict = defaultdict(lambda: AlertGroup("", ""))
        
        for alert in alerts:
            group_key = (alert.service, alert.component)
            if groups_dict[group_key].service == "":
                groups_dict[group_key].service = alert.service
                groups_dict[group_key].component = alert.component
            groups_dict[group_key].add_alert(alert)
        
        # Convert to list
        groups = list(groups_dict.values())
        
        return groups
    
    def calculate_incident_priority(self, alerts: List[Alert]) -> float:
        """
        Calculate incident priority based on weighted algorithm
        
        Args:
            alerts: List of alerts to analyze
            
        Returns:
            Priority score (higher = more critical)
        """
        if not alerts:
            return 0.0
        
        # Calculate severity score
        severity_score = 0
        for alert in alerts:
            severity_level = next((level for level in SeverityLevel if level.label == alert.severity), None)
            if severity_level:
                severity_score += severity_level.weight
        
        # Calculate average deviation from threshold
        deviations = [abs(alert.get_deviation_percentage()) for alert in alerts]
        avg_deviation = sum(deviations) / len(deviations) if deviations else 0
        
        # Calculate number of affected components
        affected_components = len(set((alert.service, alert.component) for alert in alerts))
        
        # Weighted priority calculation
        priority_score = (severity_score * 0.5) + (avg_deviation * 0.3) + (affected_components * 0.2)
        
        return priority_score
    
    def get_alert_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all alerts"""
        if not self.alerts:
            return {"total_alerts": 0}
        
        severity_counts = defaultdict(int)
        service_counts = defaultdict(int)
        component_counts = defaultdict(int)
        
        for alert in self.alerts:
            severity_counts[alert.severity] += 1
            service_counts[alert.service] += 1
            component_counts[alert.component] += 1
        
        return {
            "total_alerts": len(self.alerts),
            "severity_distribution": dict(severity_counts),
            "service_distribution": dict(service_counts),
            "component_distribution": dict(component_counts),
            "time_range": {
                "earliest": min(alert.get_datetime() for alert in self.alerts).isoformat(),
                "latest": max(alert.get_datetime() for alert in self.alerts).isoformat()
            }
        }
    
    def print_filtered_alerts(self, alerts: List[Alert], title: str = "Filtered Alerts"):
        """Print filtered alerts in a clean format"""
        print(f"\n{title}: {len(alerts)} alerts")
        for alert in alerts:
            print(f"  {alert.id}: {alert.severity} - {alert.service}/{alert.component} - {alert.metric}={alert.value}")
    
    def print_alert_groups(self, groups: List[AlertGroup]):
        """Print alert groups in a clean format"""
        print(f"\nAlert Groups: {len(groups)} groups")
        for group in groups:
            print(f"  {group.service}/{group.component}: {group.total_alerts} alerts")
            for alert in group.alerts:
                print(f"    {alert.id}: {alert.severity} - {alert.metric}={alert.value}")

    def get_affected_components_count(self, alerts: List[Alert]) -> int:
        """Return the number of unique affected components in a set of alerts"""
        return len(set((alert.service, alert.component) for alert in alerts))


def main():
    """Main function with simplified output"""
    processor = AlertProcessor("sample_alerts.json")
    
    if not processor.alerts:
        print("No alerts loaded.")
        return
    
    # Summary
    summary = processor.get_alert_summary()
    print(f"Loaded {summary['total_alerts']} alerts")
    print(f"Severity: {summary['severity_distribution']}")
    
    # Filter examples
    critical_alerts = processor.filter_alerts(severity="critical")
    processor.print_filtered_alerts(critical_alerts, "Critical Alerts")
    
    payment_alerts = processor.filter_alerts(service="payment-processor")
    processor.print_filtered_alerts(payment_alerts, "Payment Processor Alerts")
    
    # Group alerts
    alert_groups = processor.group_alerts()
    processor.print_alert_groups(alert_groups)
    
    # Priority
    overall_priority = processor.calculate_incident_priority(processor.alerts)
    print(f"\nOverall Priority: {overall_priority:.1f}")


if __name__ == "__main__":
    main()
