"""
Geodetic Analysis Module
========================

This module provides analysis functions for comparing geodetic datums,
calculating transformations, and generating comparative data for the technical report.
"""

import math
import numpy as np
from typing import Dict, List, Tuple, Any
from datum_parameters import ELLIPSOIDS, DATUMS, NAVIC_PARAMETERS, SIMULATION_PARAMETERS


class GeodeticAnalyzer:
    """Main class for geodetic datum analysis and comparisons."""
    
    def __init__(self):
        self.ellipsoids = ELLIPSOIDS
        self.datums = DATUMS
        
    def compare_ellipsoids(self, ellipsoid1_key: str, ellipsoid2_key: str) -> Dict[str, Any]:
        """
        Compare two ellipsoids and return detailed analysis.
        
        Args:
            ellipsoid1_key: Key for first ellipsoid
            ellipsoid2_key: Key for second ellipsoid
            
        Returns:
            Dictionary containing comparison analysis
        """
        e1 = self.ellipsoids[ellipsoid1_key]
        e2 = self.ellipsoids[ellipsoid2_key]
        
        # Calculate differences
        semi_major_diff = e2.semi_major_axis - e1.semi_major_axis
        flattening_diff = e2.flattening - e1.flattening
        semi_minor_diff = e2.semi_minor_axis - e1.semi_minor_axis
        
        # Calculate percentage differences
        semi_major_pct = (semi_major_diff / e1.semi_major_axis) * 100
        flattening_pct = (flattening_diff / e1.flattening) * 100
        
        return {
            'ellipsoid_1': {
                'name': e1.name,
                'semi_major_axis': e1.semi_major_axis,
                'semi_minor_axis': e1.semi_minor_axis,
                'flattening': e1.flattening,
                'inverse_flattening': e1.inverse_flattening,
                'eccentricity': e1.eccentricity,
                'eccentricity_squared': e1.eccentricity_squared
            },
            'ellipsoid_2': {
                'name': e2.name,
                'semi_major_axis': e2.semi_major_axis,
                'semi_minor_axis': e2.semi_minor_axis,
                'flattening': e2.flattening,
                'inverse_flattening': e2.inverse_flattening,
                'eccentricity': e2.eccentricity,
                'eccentricity_squared': e2.eccentricity_squared
            },
            'differences': {
                'semi_major_axis': {
                    'absolute': semi_major_diff,
                    'percentage': semi_major_pct,
                    'meters': semi_major_diff
                },
                'semi_minor_axis': {
                    'absolute': semi_minor_diff,
                    'percentage': (semi_minor_diff / e1.semi_minor_axis) * 100,
                    'meters': semi_minor_diff
                },
                'flattening': {
                    'absolute': flattening_diff,
                    'percentage': flattening_pct,
                    'significance': 'High impact on coordinate transformations' if abs(flattening_pct) > 1 else 'Moderate impact'
                },
                'inverse_flattening': {
                    'absolute': e2.inverse_flattening - e1.inverse_flattening,
                    'e1_value': e1.inverse_flattening,
                    'e2_value': e2.inverse_flattening
                }
            },
            'analysis': {
                'coordinate_impact': self._assess_coordinate_impact(semi_major_diff, flattening_diff),
                'transformation_complexity': self._assess_transformation_complexity(semi_major_diff, flattening_diff),
                'simulation_implications': self._assess_simulation_implications(semi_major_diff, flattening_diff)
            }
        }
    
    def _assess_coordinate_impact(self, semi_major_diff: float, flattening_diff: float) -> str:
        """Assess the impact on coordinate values."""
        if abs(semi_major_diff) > 500 or abs(flattening_diff) > 1e-6:
            return "High - Significant coordinate shifts expected"
        elif abs(semi_major_diff) > 100 or abs(flattening_diff) > 1e-7:
            return "Moderate - Noticeable coordinate differences"
        else:
            return "Low - Minimal coordinate impact"
    
    def _assess_transformation_complexity(self, semi_major_diff: float, flattening_diff: float) -> str:
        """Assess transformation complexity."""
        if abs(semi_major_diff) > 800:
            return "Complex - Requires full 7-parameter transformation"
        elif abs(semi_major_diff) > 200:
            return "Moderate - 3 or 7-parameter transformation recommended"
        else:
            return "Simple - Basic translation may suffice"
    
    def _assess_simulation_implications(self, semi_major_diff: float, flattening_diff: float) -> str:
        """Assess implications for simulation applications."""
        if abs(semi_major_diff) > 500:
            return "Critical - Platform positions will diverge significantly without proper transformation"
        elif abs(semi_major_diff) > 100:
            return "Important - Transformation required for accurate multi-platform coordination"
        else:
            return "Minor - Transformation recommended but not critical for most applications"

    def calculate_helmert_transformation(self, source_datum: str, target_datum: str, 
                                       coordinates: List[Tuple[float, float, float]]) -> Dict[str, Any]:
        """
        Calculate 7-parameter Helmert transformation between datums.
        
        Args:
            source_datum: Source datum key
            target_datum: Target datum key
            coordinates: List of (lat, lon, height) tuples in decimal degrees and meters
            
        Returns:
            Transformation results and analysis
        """
        source = self.datums[source_datum]
        target = self.datums[target_datum]
        
        # Get transformation parameters (source to WGS84, then WGS84 to target)
        if source_datum != 'wgs84' and target_datum != 'wgs84':
            # Chain transformation through WGS84
            source_params = source.transformation_params
            target_params = target.transformation_params
            
            # Combine parameters (simplified approach)
            combined_params = {
                'dx': source_params['dx'] - target_params['dx'],
                'dy': source_params['dy'] - target_params['dy'],
                'dz': source_params['dz'] - target_params['dz'],
                'rx': source_params['rx'] - target_params['rx'],
                'ry': source_params['ry'] - target_params['ry'],
                'rz': source_params['rz'] - target_params['rz'],
                'scale': source_params['scale'] - target_params['scale']
            }
        else:
            combined_params = source.transformation_params if source_datum != 'wgs84' else target.transformation_params
        
        transformed_coords = []
        coordinate_shifts = []
        
        for lat, lon, height in coordinates:
            # Convert to cartesian
            x, y, z = self._geodetic_to_cartesian(lat, lon, height, source.ellipsoid)
            
            # Apply 7-parameter transformation
            x_new, y_new, z_new = self._apply_helmert_7param(x, y, z, combined_params)
            
            # Convert back to geodetic
            lat_new, lon_new, height_new = self._cartesian_to_geodetic(x_new, y_new, z_new, target.ellipsoid)
            
            transformed_coords.append((lat_new, lon_new, height_new))
            
            # Calculate shifts
            shift = self._calculate_coordinate_shift((lat, lon, height), (lat_new, lon_new, height_new))
            coordinate_shifts.append(shift)
        
        return {
            'source_datum': source.name,
            'target_datum': target.name,
            'transformation_parameters': combined_params,
            'original_coordinates': coordinates,
            'transformed_coordinates': transformed_coords,
            'coordinate_shifts': coordinate_shifts,
            'statistics': {
                'mean_horizontal_shift': np.mean([s['horizontal_distance'] for s in coordinate_shifts]),
                'max_horizontal_shift': max([s['horizontal_distance'] for s in coordinate_shifts]),
                'mean_vertical_shift': np.mean([s['vertical_difference'] for s in coordinate_shifts]),
                'max_vertical_shift': max([abs(s['vertical_difference']) for s in coordinate_shifts])
            }
        }
    
    def _geodetic_to_cartesian(self, lat: float, lon: float, height: float, ellipsoid) -> Tuple[float, float, float]:
        """Convert geodetic coordinates to cartesian coordinates."""
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        a = ellipsoid.semi_major_axis
        e2 = ellipsoid.eccentricity_squared
        
        # Calculate radius of curvature in prime vertical
        N = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)
        
        # Calculate cartesian coordinates
        x = (N + height) * math.cos(lat_rad) * math.cos(lon_rad)
        y = (N + height) * math.cos(lat_rad) * math.sin(lon_rad)
        z = (N * (1 - e2) + height) * math.sin(lat_rad)
        
        return x, y, z
    
    def _cartesian_to_geodetic(self, x: float, y: float, z: float, ellipsoid) -> Tuple[float, float, float]:
        """Convert cartesian coordinates to geodetic coordinates."""
        a = ellipsoid.semi_major_axis
        b = ellipsoid.semi_minor_axis
        e2 = ellipsoid.eccentricity_squared
        
        # Calculate longitude
        lon = math.atan2(y, x)
        
        # Calculate latitude and height iteratively
        p = math.sqrt(x**2 + y**2)
        lat = math.atan2(z, p * (1 - e2))
        
        for _ in range(10):  # Iterate to convergence
            N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
            height = p / math.cos(lat) - N
            lat_new = math.atan2(z, p * (1 - e2 * N / (N + height)))
            if abs(lat_new - lat) < 1e-12:
                break
            lat = lat_new
        
        # Final height calculation
        N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
        height = p / math.cos(lat) - N
        
        return math.degrees(lat), math.degrees(lon), height
    
    def _apply_helmert_7param(self, x: float, y: float, z: float, params: Dict[str, float]) -> Tuple[float, float, float]:
        """Apply 7-parameter Helmert transformation."""
        # Extract parameters
        dx, dy, dz = params['dx'], params['dy'], params['dz']
        rx, ry, rz = params['rx'], params['ry'], params['rz']
        scale = params['scale']
        
        # Convert rotations from arc seconds to radians
        rx_rad = math.radians(rx / 3600)
        ry_rad = math.radians(ry / 3600)
        rz_rad = math.radians(rz / 3600)
        
        # Scale factor (convert from ppm to absolute)
        s = 1 + (scale * 1e-6)
        
        # Apply transformation
        x_new = dx + s * (x - rz_rad * y + ry_rad * z)
        y_new = dy + s * (rz_rad * x + y - rx_rad * z)
        z_new = dz + s * (-ry_rad * x + rx_rad * y + z)
        
        return x_new, y_new, z_new
    
    def _calculate_coordinate_shift(self, original: Tuple[float, float, float], 
                                  transformed: Tuple[float, float, float]) -> Dict[str, float]:
        """Calculate coordinate shift between original and transformed coordinates."""
        lat1, lon1, h1 = original
        lat2, lon2, h2 = transformed
        
        # Calculate horizontal distance using haversine formula
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        R = 6371000  # Earth radius in meters
        
        horizontal_distance = R * c
        vertical_difference = h2 - h1
        
        return {
            'horizontal_distance': horizontal_distance,
            'vertical_difference': vertical_difference,
            'latitude_shift': lat2 - lat1,
            'longitude_shift': lon2 - lon1,
            'height_shift': vertical_difference
        }

    def generate_sample_coordinates(self, region: str = 'india') -> List[Tuple[float, float, float]]:
        """Generate sample coordinates for different regions."""
        if region == 'india':
            return [
                (28.6139, 77.2090, 216.0),    # New Delhi
                (19.0760, 72.8777, 14.0),     # Mumbai
                (13.0827, 80.2707, 6.0),      # Chennai
                (22.5726, 88.3639, 9.0),      # Kolkata
                (12.2958, 76.6394, 770.0),    # Mysore
                (26.9124, 75.7873, 431.0),    # Jaipur
                (17.3850, 78.4867, 542.0),    # Hyderabad
                (23.0225, 72.5714, 53.0),     # Ahmedabad
                (8.5241, 76.9366, 1.0),       # Trivandrum  
                (25.5941, 91.8820, 55.0),     # Shillong
            ]
        else:
            # Global coordinates for comparison
            return [
                (51.5074, -0.1278, 35.0),     # London
                (40.7128, -74.0060, 10.0),    # New York
                (35.6762, 139.6503, 40.0),    # Tokyo
                (-33.8688, 151.2093, 58.0),   # Sydney
                (55.7558, 37.6176, 156.0),    # Moscow
            ]

    def analyze_navic_compatibility(self) -> Dict[str, Any]:
        """Analyze NavIC system compatibility with existing datums."""
        navic = NAVIC_PARAMETERS
        
        return {
            'system_overview': {
                'name': navic['system_name'],
                'reference_system': navic['reference_system'],
                'coordinate_system': navic['coordinate_system'],
                'service_area': navic['service_area']
            },
            'compatibility_analysis': {
                'wgs84_compatibility': {
                    'status': 'Fully Compatible',
                    'transformation_required': False,
                    'accuracy_impact': 'None - Same reference system'
                },
                'indian_legacy_compatibility': {
                    'everest_1830': {
                        'compatibility': 'Requires Transformation',
                        'transformation_type': '7-parameter Helmert',
                        'expected_accuracy': '± 2-5 meters',
                        'complexity': 'Medium'
                    },
                    'indian_1975': {
                        'compatibility': 'Requires Transformation',
                        'transformation_type': '7-parameter Helmert',
                        'expected_accuracy': '± 3-8 meters',
                        'complexity': 'Medium to High'
                    }
                }
            },
            'implementation_recommendations': {
                'new_systems': 'Use WGS 84 directly for NavIC compatibility',
                'legacy_integration': 'Implement real-time coordinate transformation',
                'mixed_environments': 'Use common reference system (WGS 84) with transformation layers',
                'accuracy_considerations': 'Account for transformation uncertainty in error budgets'
            },
            'positioning_performance': navic['positioning_accuracy']
        }

    def analyze_simulation_impact(self) -> Dict[str, Any]:
        """Analyze impact of datum choice on simulation applications."""
        return {
            'dis_protocol_requirements': {
                'standard_datum': SIMULATION_PARAMETERS['dis_standard']['datum_requirement'],
                'coordinate_system': SIMULATION_PARAMETERS['dis_standard']['coordinate_system'],
                'precision': SIMULATION_PARAMETERS['dis_standard']['precision'],
                'transformation_implications': 'All platforms must use consistent datum or implement real-time transformation'
            },
            'platform_accuracy_requirements': SIMULATION_PARAMETERS['accuracy_requirements'],
            'multi_datum_challenges': {
                'position_correlation': 'Platforms using different datums will show false relative positioning',
                'weapon_engagement': 'Target acquisition affected by coordinate system mismatches',
                'navigation_accuracy': 'Route planning and waypoint navigation impacted',
                'data_fusion': 'Sensor data correlation requires consistent coordinate systems'
            },
            'best_practices': {
                'datum_standardization': 'Use single datum (preferably WGS 84) throughout simulation',
                'transformation_layers': 'Implement transparent coordinate transformation for legacy data',
                'accuracy_monitoring': 'Monitor transformation accuracy in real-time',
                'documentation': 'Clearly document coordinate system assumptions and transformations'
            }
        }