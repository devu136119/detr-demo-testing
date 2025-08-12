"""
Geodetic Datum Analysis Report Generator
=======================================

Main script to generate comprehensive PDF technical report analyzing
geodetic datum systems for simulation applications.

Usage:
    python generate_geodetic_report.py [output_filename]
"""

import sys
import os
import time
from report_generator import TechnicalReportGenerator


def main():
    """Main function to generate the geodetic analysis report."""
    print("=" * 70)
    print("Geodetic Datum Analysis Report Generator")
    print("=" * 70)
    print()
    
    # Determine output filename
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    else:
        output_filename = "geodetic_datum_analysis_report.pdf"
    
    # Create report generator
    print("Initializing report generator...")
    generator = TechnicalReportGenerator()
    
    print("Generating comprehensive technical report...")
    print("This may take a few minutes to create all visualizations and analysis...")
    print()
    
    start_time = time.time()
    
    try:
        # Generate the report
        generated_file = generator.generate_report(output_filename)
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        # Get file size
        file_size = os.path.getsize(generated_file) / (1024 * 1024)  # MB
        
        print(f"✓ Report generated successfully!")
        print(f"  File: {generated_file}")
        print(f"  Size: {file_size:.2f} MB")
        print(f"  Generation time: {generation_time:.1f} seconds")
        print()
        
        # Report summary
        print("Report Contents Summary:")
        print("  • Executive Summary")
        print("  • Introduction to Geodetic Datums") 
        print("  • Technical Specifications Comparison")
        print("  • Theoretical Framework")
        print("  • VR-Forces Implementation Guide")
        print("  • NavIC Integration Analysis")
        print("  • Practical Recommendations")
        print("  • Case Studies and Examples")
        print("  • Conclusion and Best Practices")
        print("  • Appendices with Code Examples")
        print()
        
        print("Key Analysis Results:")
        print("  • Ellipsoid parameter comparisons with visualizations")
        print("  • Coordinate transformation examples and accuracy analysis")  
        print("  • VR-Forces implementation code examples")
        print("  • NavIC compatibility assessment")
        print("  • Multi-platform simulation case studies")
        print("  • Comprehensive transformation parameter tables")
        print()
        
        print(f"The report has been saved as: {generated_file}")
        print("You can now open this PDF file to review the complete technical analysis.")
        
    except Exception as e:
        print(f"✗ Error generating report: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)