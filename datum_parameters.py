"""
Geodetic Datum Parameters and Data Structures
============================================

This module contains the geodetic parameters for various coordinate systems
and reference ellipsoids used in the technical report analysis.
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Ellipsoid:
    """Represents a reference ellipsoid with its defining parameters."""
    name: str
    semi_major_axis: float  # meters
    flattening: float
    inverse_flattening: float
    
    @property
    def semi_minor_axis(self) -> float:
        """Calculate semi-minor axis from semi-major axis and flattening."""
        return self.semi_major_axis * (1 - self.flattening)
    
    @property
    def eccentricity_squared(self) -> float:
        """First eccentricity squared."""
        return 2 * self.flattening - self.flattening ** 2
    
    @property
    def eccentricity(self) -> float:
        """First eccentricity."""
        return math.sqrt(self.eccentricity_squared)


@dataclass
class DatumParameters:
    """Geodetic datum parameters including ellipsoid and transformation parameters."""
    name: str
    ellipsoid: Ellipsoid
    origin_country: str
    usage_area: str
    coordinate_system: str
    transformation_params: Dict[str, float] = None  # 7-parameter transformation
    
    def __post_init__(self):
        if self.transformation_params is None:
            self.transformation_params = {
                'dx': 0.0, 'dy': 0.0, 'dz': 0.0,  # Translation (meters)
                'rx': 0.0, 'ry': 0.0, 'rz': 0.0,  # Rotation (arc seconds)
                'scale': 0.0  # Scale factor (ppm)
            }


# Define the main ellipsoids for analysis
ELLIPSOIDS = {
    'everest_1830': Ellipsoid(
        name="Everest 1830",
        semi_major_axis=6377276.345,
        flattening=1/300.8017,
        inverse_flattening=300.8017
    ),
    'everest_2002': Ellipsoid(
        name="Everest Spheroid 2002/2004",
        semi_major_axis=6377276.345,
        flattening=1/300.8017,
        inverse_flattening=300.8017
    ),
    'wgs84': Ellipsoid(
        name="WGS 84",
        semi_major_axis=6378137.0,
        flattening=1/298.257223563,
        inverse_flattening=298.257223563
    ),
    'grs80': Ellipsoid(
        name="GRS 80",
        semi_major_axis=6378137.0,
        flattening=1/298.257222101,
        inverse_flattening=298.257222101
    )
}

# Define datum parameters
DATUMS = {
    'indian_1954': DatumParameters(
        name="Indian 1954",
        ellipsoid=ELLIPSOIDS['everest_1830'],
        origin_country="India",
        usage_area="Indian Subcontinent",
        coordinate_system="Geographic 2D",
        transformation_params={
            'dx': 289.0, 'dy': 734.0, 'dz': 257.0,
            'rx': -0.195, 'ry': -0.476, 'rz': -0.359,
            'scale': 2.4985  # ppm
        }
    ),
    'indian_1975': DatumParameters(
        name="Indian 1975",
        ellipsoid=ELLIPSOIDS['everest_1830'],
        origin_country="India",
        usage_area="Indian Peninsula",
        coordinate_system="Geographic 2D",
        transformation_params={
            'dx': 295.0, 'dy': 736.0, 'dz': 257.0,
            'rx': 0.0, 'ry': 0.0, 'rz': 0.0,
            'scale': 0.0
        }
    ),
    'everest_2004': DatumParameters(
        name="Everest Spheroid 2002/2004",
        ellipsoid=ELLIPSOIDS['everest_2002'],
        origin_country="India",
        usage_area="Survey of India modernization",
        coordinate_system="Geographic 2D",
        transformation_params={
            'dx': 283.088, 'dy': 735.321, 'dz': 261.908,
            'rx': -0.195, 'ry': -0.476, 'rz': -0.359,
            'scale': 2.4985
        }
    ),
    'wgs84': DatumParameters(
        name="WGS 84",
        ellipsoid=ELLIPSOIDS['wgs84'],
        origin_country="Global",
        usage_area="Worldwide",
        coordinate_system="Geographic 3D",
        transformation_params={
            'dx': 0.0, 'dy': 0.0, 'dz': 0.0,
            'rx': 0.0, 'ry': 0.0, 'rz': 0.0,
            'scale': 0.0
        }
    )
}

# VR-Forces specific coordinate system data
VR_FORCES_COORDINATE_SYSTEMS = {
    'geocentric': {
        'name': 'Geocentric Coordinate System',
        'origin': 'Earth center of mass',
        'x_axis': 'Intersection of equatorial plane and Greenwich meridian',
        'z_axis': 'Conventional Terrestrial Pole (CTP)',
        'units': 'meters',
        'datum_compatibility': ['wgs84', 'itrs']
    },
    'geodetic': {
        'name': 'Geodetic Coordinate System',
        'coordinates': ['latitude', 'longitude', 'ellipsoidal_height'],
        'units': ['degrees', 'degrees', 'meters'],
        'datum_compatibility': ['wgs84', 'everest_2004', 'indian_1975']
    },
    'utm': {
        'name': 'Universal Transverse Mercator',
        'projection': 'Transverse Mercator',
        'zones': list(range(1, 61)),
        'indian_zones': [43, 44, 45, 46, 47, 48],  # India spans UTM zones 43-48
        'false_easting': 500000.0,
        'false_northing': 0.0,  # Northern hemisphere
        'scale_factor': 0.9996
    }
}

# NavIC (IRNSS) system parameters
NAVIC_PARAMETERS = {
    'system_name': 'NavIC (Navigation with Indian Constellation)',
    'full_name': 'Indian Regional Navigation Satellite System (IRNSS)',
    'reference_system': 'WGS 84',
    'coordinate_system': 'ITRF 2008 (International Terrestrial Reference Frame)',
    'service_area': 'Indian subcontinent and surrounding regions (1500 km)',
    'satellites': {
        'geostationary': 3,
        'geosynchronous_inclined': 4,
        'total': 7
    },
    'positioning_accuracy': {
        'horizontal': '< 10 meters (95% confidence)',
        'vertical': '< 20 meters (95% confidence)'
    },
    'time_reference': 'Indian Standard Time (IST) + UTC offset',
    'compatibility': {
        'gps': 'Interoperable',
        'glonass': 'Interoperable',
        'galileo': 'Interoperable',
        'beidou': 'Interoperable'
    }
}

# Simulation application specific parameters
SIMULATION_PARAMETERS = {
    'dis_standard': {
        'name': 'Distributed Interactive Simulation (DIS)',
        'coordinate_system': 'Geocentric',
        'units': 'meters',
        'precision': 'double precision floating point',
        'datum_requirement': 'WGS 84',
        'transformation_needed': True
    },
    'hla_standard': {
        'name': 'High Level Architecture (HLA)',
        'coordinate_flexibility': 'User-defined',
        'common_systems': ['WGS 84', 'Local tangent plane'],
        'transformation_support': 'Implementation dependent'
    },
    'accuracy_requirements': {
        'air_platforms': {
            'horizontal': '< 5 meters',
            'vertical': '< 10 meters'
        },
        'ground_platforms': {
            'horizontal': '< 1 meter',
            'vertical': '< 2 meters'
        },
        'naval_platforms': {
            'horizontal': '< 10 meters',
            'vertical': '< 5 meters'
        }
    }
}

# Transformation accuracy data
TRANSFORMATION_ACCURACY = {
    'everest_to_wgs84': {
        'horizontal_accuracy': '± 3-5 meters',
        'vertical_accuracy': '± 5-10 meters',
        'method': '7-parameter Helmert transformation',
        'reliability': 'High (well-established parameters)'
    },
    'indian_1975_to_wgs84': {
        'horizontal_accuracy': '± 5-15 meters',
        'vertical_accuracy': '± 10-20 meters',
        'method': '3-parameter or 7-parameter transformation',
        'reliability': 'Medium (regional variations)'
    },
    'navic_to_legacy': {
        'coordinate_system': 'WGS 84 to Indian datums',
        'real_time_accuracy': '± 2-5 meters',
        'post_processing_accuracy': '± 0.5-2 meters',
        'challenges': 'Mixed datum environments'
    }
}