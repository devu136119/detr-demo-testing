"""
Visualization Module for Geodetic Analysis
==========================================

This module creates charts, diagrams, and visualizations for the technical report.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Dict, List, Tuple, Any
from datum_parameters import ELLIPSOIDS, DATUMS
import io
from reportlab.lib.utils import ImageReader


class GeodeticVisualizer:
    """Class for creating visualizations for geodetic analysis."""
    
    def __init__(self):
        plt.style.use('default')
        self.colors = {
            'everest': '#FF6B6B',
            'wgs84': '#4ECDC4', 
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01'
        }
        
    def create_ellipsoid_comparison_chart(self, ellipsoid1_key: str, ellipsoid2_key: str) -> str:
        """Create a comparative chart of ellipsoid parameters."""
        e1 = ELLIPSOIDS[ellipsoid1_key]
        e2 = ELLIPSOIDS[ellipsoid2_key]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Ellipsoid Parameter Comparison', fontsize=16, fontweight='bold')
        
        # Semi-major axis comparison
        ax1.bar([e1.name, e2.name], [e1.semi_major_axis, e2.semi_major_axis], 
                color=[self.colors['everest'], self.colors['wgs84']])
        ax1.set_title('Semi-major Axis (meters)')
        ax1.set_ylabel('Meters')
        for i, v in enumerate([e1.semi_major_axis, e2.semi_major_axis]):
            ax1.text(i, v + 100, f'{v:,.0f}', ha='center', va='bottom')
        
        # Semi-minor axis comparison
        ax2.bar([e1.name, e2.name], [e1.semi_minor_axis, e2.semi_minor_axis], 
                color=[self.colors['everest'], self.colors['wgs84']])
        ax2.set_title('Semi-minor Axis (meters)')
        ax2.set_ylabel('Meters')
        for i, v in enumerate([e1.semi_minor_axis, e2.semi_minor_axis]):
            ax2.text(i, v + 100, f'{v:,.0f}', ha='center', va='bottom')
        
        # Flattening comparison
        ax3.bar([e1.name, e2.name], [e1.flattening * 1000, e2.flattening * 1000], 
                color=[self.colors['everest'], self.colors['wgs84']])
        ax3.set_title('Flattening (×10⁻³)')
        ax3.set_ylabel('Flattening ×10⁻³')
        for i, v in enumerate([e1.flattening * 1000, e2.flattening * 1000]):
            ax3.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        # Eccentricity comparison
        ax4.bar([e1.name, e2.name], [e1.eccentricity, e2.eccentricity], 
                color=[self.colors['everest'], self.colors['wgs84']])
        ax4.set_title('First Eccentricity')
        ax4.set_ylabel('Eccentricity')
        for i, v in enumerate([e1.eccentricity, e2.eccentricity]):
            ax4.text(i, v + 0.0001, f'{v:.6f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return self._fig_to_image_reader(fig)
    
    def create_coordinate_shift_visualization(self, transformation_results: Dict[str, Any]) -> str:
        """Create visualization of coordinate shifts after transformation."""
        shifts = transformation_results['coordinate_shifts']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Coordinate Transformation Shifts', fontsize=16, fontweight='bold')
        
        # Horizontal shifts
        horizontal_shifts = [s['horizontal_distance'] for s in shifts]
        locations = [f'Point {i+1}' for i in range(len(shifts))]
        
        bars1 = ax1.bar(locations, horizontal_shifts, color=self.colors['primary'])
        ax1.set_title('Horizontal Coordinate Shifts')
        ax1.set_ylabel('Distance (meters)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars1, horizontal_shifts):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{value:.1f}m', ha='center', va='bottom')
        
        # Vertical shifts
        vertical_shifts = [s['vertical_difference'] for s in shifts]
        colors = [self.colors['accent'] if v >= 0 else self.colors['secondary'] for v in vertical_shifts]
        
        bars2 = ax2.bar(locations, vertical_shifts, color=colors)
        ax2.set_title('Vertical Coordinate Shifts')
        ax2.set_ylabel('Height Difference (meters)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars2, vertical_shifts):
            height = bar.get_height()
            if height >= 0:
                va = 'bottom'
                y_pos = height + 0.1
            else:
                va = 'top'
                y_pos = height - 0.1
            ax2.text(bar.get_x() + bar.get_width()/2., y_pos,
                    f'{value:.1f}m', ha='center', va=va)
        
        plt.tight_layout()
        return self._fig_to_image_reader(fig)
    
    def create_accuracy_comparison_chart(self) -> str:
        """Create chart comparing accuracy requirements for different applications."""
        applications = ['Air Platforms', 'Ground Platforms', 'Naval Platforms', 'NavIC System']
        horizontal_accuracy = [5, 1, 10, 10]  # meters
        vertical_accuracy = [10, 2, 5, 20]    # meters
        
        x = np.arange(len(applications))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars1 = ax.bar(x - width/2, horizontal_accuracy, width, label='Horizontal Accuracy', 
                      color=self.colors['primary'])
        bars2 = ax.bar(x + width/2, vertical_accuracy, width, label='Vertical Accuracy',
                      color=self.colors['accent'])
        
        ax.set_xlabel('Application Type')
        ax.set_ylabel('Accuracy (meters)')
        ax.set_title('Positioning Accuracy Requirements by Application')
        ax.set_xticks(x)
        ax.set_xticklabels(applications)
        ax.legend()
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{height}m', ha='center', va='bottom')
        
        plt.tight_layout()
        return self._fig_to_image_reader(fig)
    
    def create_datum_transformation_flow_chart(self) -> str:
        """Create a flow chart showing datum transformation process."""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        
        # Define boxes and their positions
        boxes = [
            {'text': 'Source Datum\n(Everest 1830)', 'pos': (1, 6), 'color': self.colors['everest']},
            {'text': 'Geodetic to\nCartesian', 'pos': (3, 6), 'color': self.colors['primary']},
            {'text': '7-Parameter\nHelmert Transform', 'pos': (5, 6), 'color': self.colors['secondary']},
            {'text': 'Cartesian to\nGeodetic', 'pos': (7, 6), 'color': self.colors['primary']},
            {'text': 'Target Datum\n(WGS 84)', 'pos': (9, 6), 'color': self.colors['wgs84']},
        ]
        
        # Draw boxes
        for box in boxes:
            rect = patches.FancyBboxPatch(
                (box['pos'][0] - 0.6, box['pos'][1] - 0.4), 1.2, 0.8,
                boxstyle="round,pad=0.1", 
                facecolor=box['color'], 
                alpha=0.7,
                edgecolor='black'
            )
            ax.add_patch(rect)
            ax.text(box['pos'][0], box['pos'][1], box['text'], 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw arrows
        arrow_positions = [(1.6, 6), (3.6, 6), (5.6, 6), (7.6, 6)]
        for pos in arrow_positions:
            ax.arrow(pos[0], pos[1], 0.8, 0, head_width=0.1, head_length=0.1, 
                    fc='black', ec='black')
        
        # Add transformation parameters
        param_text = ("Transformation Parameters:\n"
                     "• Translation: (dx, dy, dz)\n"
                     "• Rotation: (rx, ry, rz)\n"
                     "• Scale: (s)")
        ax.text(5, 4, param_text, ha='center', va='top', fontsize=11,
               bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
        
        # Add coordinate examples
        coord_text = ("Coordinate Examples:\n"
                     "Input: 28.6139°N, 77.2090°E\n"
                     "Output: 28.6141°N, 77.2088°E\n"
                     "Shift: ~150m horizontal")
        ax.text(5, 2, coord_text, ha='center', va='top', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
        
        ax.set_title('Geodetic Datum Transformation Process', fontsize=16, fontweight='bold', pad=20)
        
        return self._fig_to_image_reader(fig)
    
    def create_india_coverage_map(self) -> str:
        """Create a simplified map showing UTM zones and coordinate systems coverage in India."""
        fig, ax = plt.subplots(figsize=(10, 12))
        
        # Simplified India outline (approximate coordinates)
        india_outline_lon = [68, 97, 97, 88, 85, 80, 77, 72, 68, 68]
        india_outline_lat = [35, 35, 28, 22, 20, 15, 8, 8, 20, 35]
        
        ax.plot(india_outline_lon, india_outline_lat, 'k-', linewidth=2, label='India Boundary')
        ax.fill(india_outline_lon, india_outline_lat, color='lightblue', alpha=0.3)
        
        # UTM zones
        utm_zones = [(72, 78), (78, 84), (84, 90), (90, 96)]
        zone_numbers = [43, 44, 45, 46]
        colors_utm = ['red', 'green', 'blue', 'orange']
        
        for i, (lon_min, lon_max) in enumerate(utm_zones):
            ax.axvline(x=lon_min, color=colors_utm[i], linestyle='--', alpha=0.7, linewidth=2)
            ax.axvline(x=lon_max, color=colors_utm[i], linestyle='--', alpha=0.7, linewidth=2)
            ax.text(lon_min + 3, 32, f'UTM {zone_numbers[i]}', rotation=90, 
                   color=colors_utm[i], fontweight='bold', fontsize=12)
        
        # Major cities with different datum representations
        cities = [
            {'name': 'New Delhi', 'lon': 77.2090, 'lat': 28.6139},
            {'name': 'Mumbai', 'lon': 72.8777, 'lat': 19.0760},
            {'name': 'Chennai', 'lon': 80.2707, 'lat': 13.0827},
            {'name': 'Kolkata', 'lon': 88.3639, 'lat': 22.5726},
        ]
        
        for city in cities:
            ax.plot(city['lon'], city['lat'], 'ro', markersize=8, markerfacecolor='red')
            ax.text(city['lon'] + 0.5, city['lat'] + 0.5, city['name'], fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Longitude (degrees)')
        ax.set_ylabel('Latitude (degrees)')
        ax.set_title('Indian Coordinate Systems Coverage and UTM Zones', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='black', linewidth=2, label='India Boundary'),
            plt.Line2D([0], [0], color='red', linestyle='--', label='UTM Zone 43'),
            plt.Line2D([0], [0], color='green', linestyle='--', label='UTM Zone 44'),
            plt.Line2D([0], [0], color='blue', linestyle='--', label='UTM Zone 45'),
            plt.Line2D([0], [0], color='orange', linestyle='--', label='UTM Zone 46'),
            plt.Line2D([0], [0], marker='o', color='red', linewidth=0, markersize=8, label='Major Cities')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        return self._fig_to_image_reader(fig)
    
    def create_transformation_accuracy_chart(self) -> str:
        """Create chart showing transformation accuracy for different methods."""
        methods = ['3-Parameter\nTransformation', '7-Parameter\nHelmert', 'Grid-based\nInterpolation', 
                  'High-precision\nSurvey']
        horizontal_accuracy = [15, 5, 2, 0.5]
        vertical_accuracy = [20, 10, 5, 1]
        
        x = np.arange(len(methods))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        bars1 = ax.bar(x - width/2, horizontal_accuracy, width, label='Horizontal Accuracy (±m)', 
                      color=self.colors['primary'], alpha=0.8)
        bars2 = ax.bar(x + width/2, vertical_accuracy, width, label='Vertical Accuracy (±m)',
                      color=self.colors['accent'], alpha=0.8)
        
        ax.set_xlabel('Transformation Method')
        ax.set_ylabel('Accuracy (meters)')
        ax.set_title('Coordinate Transformation Accuracy by Method')
        ax.set_xticks(x)
        ax.set_xticklabels(methods)
        ax.legend()
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3, which='both')
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                       f'±{height}m', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        return self._fig_to_image_reader(fig)
    
    def create_vr_forces_architecture_diagram(self) -> str:
        """Create VR-Forces system architecture diagram."""
        fig, ax = plt.subplots(figsize=(12, 9))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 9)
        ax.axis('off')
        
        # System components
        components = [
            {'name': 'VR-Forces\nSimulation Engine', 'pos': (6, 7), 'size': (2, 1), 'color': self.colors['primary']},
            {'name': 'Coordinate\nTransformation\nModule', 'pos': (6, 5), 'size': (2, 1), 'color': self.colors['secondary']},
            {'name': 'WGS 84\nReference', 'pos': (3, 5), 'size': (1.5, 0.8), 'color': self.colors['wgs84']},
            {'name': 'Everest 1830\nLegacy Data', 'pos': (9, 5), 'size': (1.5, 0.8), 'color': self.colors['everest']},
            {'name': 'DIS Network\nProtocol', 'pos': (6, 3), 'size': (2, 0.8), 'color': self.colors['accent']},
            {'name': 'Platform 1\n(Air)', 'pos': (2, 1), 'size': (1.2, 0.8), 'color': 'lightblue'},
            {'name': 'Platform 2\n(Ground)', 'pos': (6, 1), 'size': (1.2, 0.8), 'color': 'lightgreen'},
            {'name': 'Platform 3\n(Naval)', 'pos': (10, 1), 'size': (1.2, 0.8), 'color': 'lightcoral'},
        ]
        
        # Draw components
        for comp in components:
            rect = patches.FancyBboxPatch(
                (comp['pos'][0] - comp['size'][0]/2, comp['pos'][1] - comp['size'][1]/2), 
                comp['size'][0], comp['size'][1],
                boxstyle="round,pad=0.1", 
                facecolor=comp['color'], 
                alpha=0.7,
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(rect)
            ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                   ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Draw connections
        connections = [
            ((6, 6.5), (6, 5.5)),  # Engine to Transform
            ((4.5, 5), (5, 5)),    # WGS84 to Transform
            ((7.5, 5), (7, 5)),    # Everest to Transform
            ((6, 4.5), (6, 3.8)),  # Transform to DIS
            ((6, 2.2), (2, 1.8)),  # DIS to Platform 1
            ((6, 2.2), (6, 1.8)),  # DIS to Platform 2
            ((6, 2.2), (10, 1.8)), # DIS to Platform 3
        ]
        
        for start, end in connections:
            ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)
            # Add arrowheads
            dx, dy = end[0] - start[0], end[1] - start[1]
            length = np.sqrt(dx**2 + dy**2)
            if length > 0:
                dx, dy = dx/length, dy/length
                ax.arrow(end[0] - 0.15*dx, end[1] - 0.15*dy, 0.1*dx, 0.1*dy, 
                        head_width=0.1, head_length=0.1, fc='black', ec='black')
        
        ax.set_title('VR-Forces Coordinate System Integration Architecture', 
                    fontsize=14, fontweight='bold', pad=20)
        
        return self._fig_to_image_reader(fig)
    
    def _fig_to_image_reader(self, fig) -> str:
        """Convert matplotlib figure to temporary image file for ReportLab."""
        import tempfile
        import os
        
        # Create temporary file
        temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(temp_fd)
        
        # Save figure to temporary file
        fig.savefig(temp_path, format='png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return temp_path