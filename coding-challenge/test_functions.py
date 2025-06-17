#!/usr/bin/env python3
"""
Test script to demonstrate the alert processing functions
"""

from main import AlertProcessor


def test_filtering_functions():
    """Test the filtering functions"""
    print("FILTERING TESTS")
    
    processor = AlertProcessor("sample_alerts.json")
    
    # Test 1: Filter by severity
    critical_alerts = processor.filter_alerts(severity="critical")
    print(f"Critical: {len(critical_alerts)} alerts")
    for alert in critical_alerts:
        print(f"  {alert.id}: {alert.service}/{alert.component}")
    
    # Test 2: Filter by service
    payment_alerts = processor.filter_alerts(service="payment-processor")
    print(f"Payment processor: {len(payment_alerts)} alerts")
    for alert in payment_alerts:
        print(f"  {alert.id}: {alert.severity} - {alert.metric}")
    
    # Test 3: Filter by time window
    recent_alerts = processor.filter_alerts(time_window_minutes=60)
    print(f"Recent (60min): {len(recent_alerts)} alerts")
    
    # Test 4: Combined filters
    combined_alerts = processor.filter_alerts(severity="critical", service="payment-processor")
    print(f"Critical + payment: {len(combined_alerts)} alerts")


def test_grouping_function():
    """Test the alert grouping function"""
    print("\nGROUPING TESTS")
    
    processor = AlertProcessor("sample_alerts.json")
    groups = processor.group_alerts()
    
    print(f"Groups: {len(groups)}")
    for group in groups:
        print(f"  {group.service}/{group.component}: {group.total_alerts} alerts")


def test_priority_calculation():
    """Test the priority calculation function"""
    print("\nPRIORITY TESTS")
    
    processor = AlertProcessor("sample_alerts.json")
    
    overall_priority = processor.calculate_incident_priority(processor.alerts)
    print(f"Overall incident priority: {overall_priority:.1f}")
    


if __name__ == "__main__":
    print("ALERT PROCESSING TESTS")
    print("=" * 40)
    
    try:
        test_filtering_functions()
        test_grouping_function()
        test_priority_calculation()
        
        print("\n" + "=" * 40)
        print("ALL TESTS COMPLETED")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc() 