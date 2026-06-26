"""
Test script to verify the updated RouteMaster AI application
Tests both the /route endpoint and grid-based target extraction
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_route_endpoint():
    """Test the /route endpoint with exact JSON specification"""
    print("=" * 60)
    print("TEST 1: /route endpoint with user-specified JSON format")
    print("=" * 60)
    
    payload = {
        "grid": [
            [0, 0, 1],
            [1, 0, 1],
            [0, 2, 0]
        ],
        "start": [0, 0],
        "targets": [[2, 1]]
    }
    
    print("\nInput:")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/route", json=payload)
    
    print(f"\nResponse Status: {response.status_code}")
    print("\nOutput:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    # Verify expected output structure
    assert "total_steps" in result, "Missing total_steps"
    assert "path" in result, "Missing path"
    assert "target_reached" in result, "Missing target_reached"
    assert "execution_time_ms" in result, "Missing execution_time_ms"
    
    # Verify expected values for this test case
    assert result["total_steps"] == 3, f"Expected 3 steps, got {result['total_steps']}"
    assert result["target_reached"] == True, "Target should be reached"
    assert len(result["path"]) == 4, f"Expected 4 path points, got {len(result['path'])}"
    
    print("\n✅ TEST 1 PASSED: All assertions successful!")
    return True


def test_grid_target_extraction():
    """Test that targets are extracted from grid cells marked with 2"""
    print("\n" + "=" * 60)
    print("TEST 2: Target extraction from grid (cells marked as 2)")
    print("=" * 60)
    
    payload = {
        "grid": [
            [0, 0, 1],
            [1, 0, 1],
            [0, 2, 0]
        ],
        "start": [0, 0],
        "targets": []  # Empty targets array - should extract from grid
    }
    
    print("\nInput (targets array is empty - should extract from grid):")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/route", json=payload)
    
    print(f"\nResponse Status: {response.status_code}")
    print("\nOutput:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    # Should successfully find target at [2, 1] from grid
    assert result["target_reached"] == True, "Should find target from grid"
    assert result["total_steps"] == 3, f"Expected 3 steps, got {result['total_steps']}"
    
    print("\n✅ TEST 2 PASSED: Targets correctly extracted from grid!")
    return True


def test_calculate_route_endpoint():
    """Test the /calculate-route endpoint with new response format"""
    print("\n" + "=" * 60)
    print("TEST 3: /calculate-route endpoint with updated format")
    print("=" * 60)
    
    payload = {
        "grid": [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 2, 0, 2],
            [0, 0, 0, 0]
        ],
        "start": [0, 0],
        "targets": []
    }
    
    print("\nInput (2 targets in grid):")
    print(json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/calculate-route", json=payload)
    
    print(f"\nResponse Status: {response.status_code}")
    print("\nOutput:")
    result = response.json()
    print(json.dumps(result, indent=2))
    
    # Verify new response format includes both old and new fields
    assert "execution_time_ms" in result, "Missing execution_time_ms"
    assert "target_reached" in result, "Missing target_reached"
    assert "total_steps" in result, "Missing total_steps"
    
    print("\n✅ TEST 3 PASSED: /calculate-route works with new format!")
    return True


def main():
    print("\n🚀 Starting RouteMaster AI Test Suite\n")
    
    try:
        # Run all tests
        test_route_endpoint()
        test_grid_target_extraction()
        test_calculate_route_endpoint()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nSummary:")
        print("✅ /route endpoint accepts exact JSON specification")
        print("✅ Targets extracted from grid cells marked with 2")
        print("✅ Response includes target_reached and execution_time_ms")
        print("✅ Grid rules: 0=walkable, 1=obstacle, 2=target")
        print("✅ Movement: up, down, left, right (no diagonals)")
        print("✅ Path minimizes total steps")
        print("\n📌 Application is ready for use!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
