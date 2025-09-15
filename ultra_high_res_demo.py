#!/usr/bin/env python3
"""
Ultra-High Resolution Earth Engine Demo
Demonstrates sub-meter precision satellite imagery for building-level detail analysis
"""

from earth_engine_utils import get_san_francisco_tiles_and_images
import json

def demo_ultra_high_resolution():
    """
    Demonstrate ultra-high resolution capabilities with different SF locations
    """
    
    # Different interesting locations in San Francisco for testing
    locations = [
        {
            'name': 'Financial District (Downtown)',
            'lat': 37.7749,
            'lon': -122.4194,
            'description': 'Dense urban area with skyscrapers'
        },
        {
            'name': 'Golden Gate Park',
            'lat': 37.7694,
            'lon': -122.4862,
            'description': 'Large urban park with mixed vegetation'
        },
        {
            'name': 'Lombard Street (Crooked Street)',
            'lat': 37.8021,
            'lon': -122.4187,
            'description': 'Famous winding street with residential buildings'
        },
        {
            'name': 'Pier 39/Fisherman\'s Wharf',
            'lat': 37.8087,
            'lon': -122.4098,
            'description': 'Waterfront area with piers and tourist attractions'
        }
    ]
    
    print("=== ULTRA-HIGH RESOLUTION EARTH ENGINE DEMO ===")
    print("Testing sub-meter precision across different San Francisco locations\n")
    
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location['name']}")
        print(f"   Description: {location['description']}")
        print(f"   Coordinates: {location['lat']}, {location['lon']}")
        
        try:
            result = get_san_francisco_tiles_and_images(
                lat=location['lat'],
                lon=location['lon'],
                zoom_level=21,                    # Maximum zoom for extreme detail
                buffer_size=15,                   # Very small area (15m radius)
                resolution_mode="ultra_high_res", # Ultra-high resolution mode
                start_date="2023-01-01",
                end_date="2023-12-31",
                save_json=True,
                output_dir=f"output/{location['name'].lower().replace(' ', '_').replace('/', '_')}"
            )
            
            print(f"   ✓ Data collected successfully")
            print(f"   ✓ JSON saved to: {result.get('saved_to', 'N/A')}")
            print(f"   ✓ Available datasets: {list(result['image_urls'].keys())}")
            
            # Show resolution details
            if result['metadata']:
                print(f"   ✓ Resolution details:")
                for dataset, meta in result['metadata'].items():
                    resolution = meta.get('resolution', 'Unknown')
                    date = meta.get('date', 'Unknown')
                    print(f"     - {dataset}: {resolution} (acquired: {date})")
            
            # Show tiles information
            tiles_count = result['tiles_info']['tile_count']
            zoom = result['tiles_info']['zoom_level']
            print(f"   ✓ Tiles: {tiles_count} tiles at zoom level {zoom}")
            
            print()
            
        except Exception as e:
            print(f"   ✗ Error: {e}")
            print()
    
    return locations

def compare_resolution_modes():
    """
    Compare all three resolution modes for the same location
    """
    print("=== RESOLUTION MODE COMPARISON ===")
    print("Comparing Standard vs High-Res vs Ultra-High-Res for the same location\n")
    
    # Use Financial District as test location
    lat, lon = 37.7749, -122.4194
    
    modes = [
        {
            'name': 'Standard Resolution',
            'mode': 'standard',
            'buffer': 500,
            'zoom': 12,
            'description': 'City-level view (30m resolution)'
        },
        {
            'name': 'High Resolution',
            'mode': 'high_res',
            'buffer': 100,
            'zoom': 18,
            'description': 'Block-level view (1-10m resolution)'
        },
        {
            'name': 'Ultra-High Resolution',
            'mode': 'ultra_high_res',
            'buffer': 25,
            'zoom': 21,
            'description': 'Building-level view (0.3-1m resolution)'
        }
    ]
    
    results = {}
    
    for mode_config in modes:
        print(f"Testing {mode_config['name']}...")
        print(f"  {mode_config['description']}")
        
        try:
            result = get_san_francisco_tiles_and_images(
                lat=lat,
                lon=lon,
                zoom_level=mode_config['zoom'],
                buffer_size=mode_config['buffer'],
                resolution_mode=mode_config['mode'],
                start_date="2023-01-01",
                end_date="2023-12-31",
                save_json=True,
                output_dir=f"output/comparison_{mode_config['mode']}"
            )
            
            results[mode_config['mode']] = result
            
            print(f"  ✓ Buffer area: {result['location']['buffer_size_meters']}m")
            print(f"  ✓ Zoom level: {result['configuration']['zoom_level']}")
            print(f"  ✓ Image size: {2048 if result['configuration']['resolution_mode'] == 'ultra_high_res' else (1024 if result['configuration']['resolution_mode'] == 'high_res' else 512)}px")
            print(f"  ✓ Datasets: {list(result['image_urls'].keys())}")
            print(f"  ✓ Tiles: {result['tiles_info']['tile_count']}")
            print()
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()
    
    # Summary comparison
    print("=== SUMMARY COMPARISON ===")
    if results:
        for mode, result in results.items():
            mode_name = mode.replace('_', '-').title()
            print(f"\n{mode_name} Mode Summary:")
            print(f"  Area covered: {result['location']['buffer_size_meters']}m radius")
            print(f"  Zoom level: {result['configuration']['zoom_level']}")
            print(f"  Available datasets: {len(result['image_urls'])}")
            
            if result['metadata']:
                best_resolution = min([meta.get('resolution', '999m') for meta in result['metadata'].values()])
                print(f"  Best resolution: {best_resolution}")
    
    return results

if __name__ == "__main__":
    print("Starting Ultra-High Resolution Earth Engine Demo...")
    print("This demo showcases sub-meter precision satellite imagery capabilities.\n")
    
    # Run location-based demo
    locations = demo_ultra_high_resolution()
    
    print("\n" + "="*60 + "\n")
    
    # Run resolution comparison
    comparison_results = compare_resolution_modes()
    
    print("\n" + "="*60)
    print("Demo completed! Check the 'output' directory for saved JSON files and images.")
    print("\nKey capabilities demonstrated:")
    print("• Sub-meter resolution (0.3-0.5m with commercial satellites)")
    print("• Building-level detail analysis")
    print("• Multiple high-resolution data sources")
    print("• Automatic JSON data saving with timestamps")
    print("• Flexible buffer sizes (15-50m for ultra-high detail)")
    print("• Maximum zoom levels (19-21 for street/building level)")
    print("\nFor modeling applications, ultra_high_res mode provides:")
    print("• Individual building detection")
    print("• Street-level infrastructure analysis")
    print("• Vegetation mapping at tree level")
    print("• Urban planning and development monitoring")