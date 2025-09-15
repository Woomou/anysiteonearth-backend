#!/usr/bin/env python3
"""
Test different global locations for data availability
"""

from earth_engine_utils import get_san_francisco_tiles_and_images
import json

def test_global_locations():
    """
    Test various global locations to demonstrate data coverage
    """
    
    # Test locations across different continents and data coverage zones
    test_locations = [
        # 🇺🇸 USA (Full coverage including NAIP)
        {
            'name': 'New York City, USA',
            'lat': 40.7128,
            'lon': -74.0060,
            'expected_datasets': ['naip', 'sentinel', 'landsat', 'worldview'],
            'coverage': 'Full (USA)'
        },
        
        # 🇨🇳 China (Sentinel + Landsat + some commercial)
        {
            'name': 'Beijing, China',
            'lat': 39.9042,
            'lon': 116.4074,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🇬🇧 Europe (Sentinel + Landsat + some commercial)
        {
            'name': 'London, UK',
            'lat': 51.5074,
            'lon': -0.1278,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🇧🇷 South America (Sentinel + Landsat)
        {
            'name': 'São Paulo, Brazil',
            'lat': -23.5505,
            'lon': -46.6333,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🇰🇪 Africa (Sentinel + Landsat)
        {
            'name': 'Nairobi, Kenya',
            'lat': -1.2921,
            'lon': 36.8219,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🇦🇺 Australia (Sentinel + Landsat)
        {
            'name': 'Sydney, Australia',
            'lat': -33.8688,
            'lon': 151.2093,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🇯🇵 Japan (Sentinel + Landsat + some commercial)
        {
            'name': 'Tokyo, Japan',
            'lat': 35.6762,
            'lon': 139.6503,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Good (Global datasets)'
        },
        
        # 🏝️ Remote location (Limited coverage)
        {
            'name': 'Remote Pacific Island',
            'lat': -15.0,
            'lon': -140.0,
            'expected_datasets': ['sentinel', 'landsat'],
            'coverage': 'Limited (Ocean area)'
        }
    ]
    
    print("🌍 GLOBAL LOCATION DATA AVAILABILITY TEST")
    print("=" * 60)
    
    results = {}
    
    for i, location in enumerate(test_locations, 1):
        print(f"\n{i}. Testing: {location['name']}")
        print(f"   Coordinates: {location['lat']}, {location['lon']}")
        print(f"   Expected coverage: {location['coverage']}")
        
        try:
            # Test with standard resolution first (more reliable)
            result = get_san_francisco_tiles_and_images(
                lat=location['lat'],
                lon=location['lon'],
                zoom_level=12,
                buffer_size=1000,
                resolution_mode="standard",
                start_date="2023-01-01", 
                end_date="2023-12-31",
                save_json=False,  # Don't save to avoid clutter
                output_dir=f"temp_{location['name'].lower().replace(' ', '_').replace(',', '')}"
            )
            
            available_datasets = list(result['image_urls'].keys())
            results[location['name']] = {
                'available': available_datasets,
                'expected': location['expected_datasets'],
                'coverage': location['coverage'],
                'coordinates': [location['lat'], location['lon']]
            }
            
            print(f"   ✅ Available datasets: {available_datasets}")
            print(f"   📊 Dataset count: {len(available_datasets)}")
            
            # Check if high-res datasets are available
            high_res_available = [d for d in available_datasets if d in ['naip', 'worldview', 'geoeye', 'skysat']]
            if high_res_available:
                print(f"   🎯 High-res available: {high_res_available}")
            else:
                print(f"   📡 Only global datasets available")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}...")
            results[location['name']] = {
                'available': [],
                'expected': location['expected_datasets'],
                'coverage': location['coverage'],
                'error': str(e),
                'coordinates': [location['lat'], location['lon']]
            }
    
    # Summary analysis
    print(f"\n" + "=" * 60)
    print("📊 GLOBAL DATA COVERAGE SUMMARY")
    print("=" * 60)
    
    coverage_stats = {
        'Full (USA)': [],
        'Good (Global datasets)': [],
        'Limited (Ocean area)': []
    }
    
    for location, data in results.items():
        coverage_type = data['coverage']
        dataset_count = len(data['available'])
        coverage_stats[coverage_type].append({
            'location': location,
            'count': dataset_count,
            'datasets': data['available']
        })
    
    for coverage_type, locations in coverage_stats.items():
        if locations:
            print(f"\n{coverage_type}:")
            for loc_data in locations:
                print(f"  • {loc_data['location']}: {loc_data['count']} datasets")
    
    # Best resolution recommendations
    print(f"\n🎯 RESOLUTION RECOMMENDATIONS BY REGION:")
    print(f"🇺🇸 USA/Canada: ultra_high_res (0.3-1m) - NAIP + Commercial")
    print(f"🌍 Major cities globally: high_res (1-10m) - Sentinel + some commercial")  
    print(f"🌍 Other global locations: standard (10-30m) - Sentinel + Landsat")
    print(f"🏝️ Remote/ocean areas: standard (10-30m) - Landsat only")
    
    return results

def get_location_recommendations():
    """
    Provide specific recommendations for different types of locations
    """
    recommendations = {
        "🇺🇸 USA": {
            "best_mode": "ultra_high_res",
            "resolution": "0.3-1m",
            "datasets": ["NAIP", "WorldView", "Sentinel-2", "Landsat"],
            "note": "Full access to highest resolution data"
        },
        "🏙️ Major Global Cities": {
            "best_mode": "high_res", 
            "resolution": "1-10m",
            "datasets": ["Sentinel-2", "Some commercial", "Landsat"],
            "note": "Good coverage for urban analysis"
        },
        "🌍 Global Rural/Suburban": {
            "best_mode": "standard",
            "resolution": "10-30m", 
            "datasets": ["Sentinel-2", "Landsat"],
            "note": "Reliable global coverage"
        },
        "🏝️ Remote/Ocean Areas": {
            "best_mode": "standard",
            "resolution": "30m",
            "datasets": ["Landsat"],
            "note": "Limited but consistent coverage"
        }
    }
    
    print("\n📋 LOCATION-SPECIFIC RECOMMENDATIONS:")
    print("=" * 50)
    
    for region, rec in recommendations.items():
        print(f"\n{region}")
        print(f"  Best mode: {rec['best_mode']}")
        print(f"  Resolution: {rec['resolution']}")
        print(f"  Available datasets: {', '.join(rec['datasets'])}")
        print(f"  Note: {rec['note']}")

if __name__ == "__main__":
    print("Testing global location data availability...")
    print("This will test 8 locations across different continents\n")
    
    # Run global test
    results = test_global_locations()
    
    # Show recommendations
    get_location_recommendations()
    
    print(f"\n✅ Test completed!")
    print(f"Key finding: You can use ANY global coordinates, but data availability varies by region.")