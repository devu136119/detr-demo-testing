"""
Test Script for Geodetic Analysis System
========================================

Simple test script to validate the geodetic analysis components
before generating the full report.
"""

import sys
import traceback
from datum_parameters import ELLIPSOIDS, DATUMS
from geodetic_analysis import GeodeticAnalyzer
from visualizations import GeodeticVisualizer


def test_datum_parameters():
    """Test datum parameter loading."""
    print("Testing datum parameter loading...")
    
    # Test ellipsoids
    assert 'everest_2002' in ELLIPSOIDS, "Everest 2002 ellipsoid missing"
    assert 'wgs84' in ELLIPSOIDS, "WGS 84 ellipsoid missing"
    
    everest = ELLIPSOIDS['everest_2002']
    wgs84 = ELLIPSOIDS['wgs84']
    
    print(f"  Everest 2002: semi-major axis = {everest.semi_major_axis:,.1f} m")
    print(f"  WGS 84: semi-major axis = {wgs84.semi_major_axis:,.1f} m")
    print(f"  Difference: {wgs84.semi_major_axis - everest.semi_major_axis:,.1f} m")
    
    # Test datums
    assert 'wgs84' in DATUMS, "WGS 84 datum missing"
    assert 'everest_2004' in DATUMS, "Everest 2004 datum missing"
    
    print("✓ Datum parameters loaded successfully")


def test_geodetic_analyzer():
    """Test geodetic analysis functionality."""
    print("Testing geodetic analyzer...")
    
    analyzer = GeodeticAnalyzer()
    
    # Test ellipsoid comparison
    comparison = analyzer.compare_ellipsoids('everest_2002', 'wgs84')
    
    assert 'ellipsoid_1' in comparison, "Missing ellipsoid_1 data"
    assert 'ellipsoid_2' in comparison, "Missing ellipsoid_2 data"
    assert 'differences' in comparison, "Missing differences data"
    assert 'analysis' in comparison, "Missing analysis data"
    
    semi_major_diff = comparison['differences']['semi_major_axis']['meters']
    print(f"  Semi-major axis difference: {semi_major_diff:,.1f} meters")
    print(f"  Coordinate impact: {comparison['analysis']['coordinate_impact']}")
    
    # Test coordinate transformation
    sample_coords = [(28.6139, 77.2090, 216.0)]  # New Delhi
    transformation = analyzer.calculate_helmert_transformation('everest_2004', 'wgs84', sample_coords)
    
    assert 'transformed_coordinates' in transformation, "Missing transformed coordinates"
    assert 'coordinate_shifts' in transformation, "Missing coordinate shifts"
    
    shift = transformation['coordinate_shifts'][0]
    print(f"  New Delhi coordinate shift: {shift['horizontal_distance']:.1f}m horizontal, {shift['vertical_difference']:.1f}m vertical")
    
    # Test NavIC compatibility analysis
    navic_analysis = analyzer.analyze_navic_compatibility()
    assert 'system_overview' in navic_analysis, "Missing NavIC system overview"
    assert 'compatibility_analysis' in navic_analysis, "Missing NavIC compatibility analysis"
    
    print("✓ Geodetic analyzer working correctly")


def test_visualizations():
    """Test visualization generation."""
    print("Testing visualizations...")
    
    visualizer = GeodeticVisualizer()
    
    # Test ellipsoid comparison chart
    try:
        chart = visualizer.create_ellipsoid_comparison_chart('everest_2002', 'wgs84')
        assert chart is not None, "Failed to create ellipsoid comparison chart"
        print("  ✓ Ellipsoid comparison chart created")
    except Exception as e:
        print(f"  ✗ Ellipsoid comparison chart failed: {e}")
        raise
    
    # Test accuracy comparison chart
    try:
        accuracy_chart = visualizer.create_accuracy_comparison_chart()
        assert accuracy_chart is not None, "Failed to create accuracy comparison chart"
        print("  ✓ Accuracy comparison chart created")
    except Exception as e:
        print(f"  ✗ Accuracy comparison chart failed: {e}")
        raise
    
    # Test transformation flow chart
    try:
        flow_chart = visualizer.create_datum_transformation_flow_chart()
        assert flow_chart is not None, "Failed to create transformation flow chart"
        print("  ✓ Transformation flow chart created")
    except Exception as e:
        print(f"  ✗ Transformation flow chart failed: {e}")
        raise
    
    print("✓ Visualizations working correctly")


def test_integration():
    """Test full integration."""
    print("Testing full integration...")
    
    try:
        from report_generator import TechnicalReportGenerator
        
        # Create a minimal report generator (don't generate full report)
        generator = TechnicalReportGenerator()
        
        # Test that all required components are accessible
        assert generator.analyzer is not None, "Analyzer not initialized"
        assert generator.visualizer is not None, "Visualizer not initialized"
        assert generator.styles is not None, "Styles not initialized"
        
        print("✓ Report generator initialized successfully")
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        raise


def main():
    """Run all tests."""
    print("=" * 50)
    print("Geodetic Analysis System Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        test_datum_parameters,
        test_geodetic_analyzer,
        test_visualizations,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
            print()
        except Exception as e:
            failed += 1
            print(f"✗ Test failed: {test_func.__name__}")
            print(f"  Error: {str(e)}")
            traceback.print_exc()
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✓ All tests passed! System ready for report generation.")
        return 0
    else:
        print("✗ Some tests failed. Please fix issues before generating report.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)