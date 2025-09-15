import ee
import requests
from typing import Dict, List, Tuple, Optional
import json
import os
from datetime import datetime

def initialize_earth_engine():
    """Initialize Google Earth Engine with authentication."""
    try:
        ee.Initialize()
        print("Earth Engine initialized successfully")
    except Exception as e:
        print(f"Earth Engine initialization failed: {e}")
        print("Please run 'earthengine authenticate' first")
        raise

def get_san_francisco_tiles_and_images(
    lat: float = 37.7749,
    lon: float = -122.4194,
    zoom_level: int = 12,
    buffer_size: int = 1000,
    start_date: str = "2023-01-01",
    end_date: str = "2023-12-31",
    resolution_mode: str = "standard",
    save_json: bool = True,
    output_dir: str = "output"
) -> Dict:
    """
    Get tiles information and images for a point in San Francisco using Google Earth Engine.
    
    Args:
        lat: Latitude of the point (default: San Francisco downtown)
        lon: Longitude of the point (default: San Francisco downtown)
        zoom_level: Zoom level for tiles (default: 12)
        buffer_size: Buffer size around the point in meters (default: 1000m)
        start_date: Start date for image collection (YYYY-MM-DD)
        end_date: End date for image collection (YYYY-MM-DD)
        resolution_mode: "standard", "high_res", or "ultra_high_res" for sub-meter detail
        save_json: Whether to save results to JSON file
        output_dir: Directory to save output files
    
    Returns:
        Dictionary containing tiles info and image data
    """
    initialize_earth_engine()
    
    # Create output directory if it doesn't exist
    if save_json and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a point geometry
    point = ee.Geometry.Point([lon, lat])
    
    # Adjust buffer size and zoom for resolution mode
    if resolution_mode == "high_res":
        # For block-level detail, use smaller buffer (50-200m) and higher zoom
        buffer_size = min(buffer_size, 200)  # Cap at 200m for block level
        zoom_level = max(zoom_level, 18)     # Minimum zoom 18 for street level
    elif resolution_mode == "ultra_high_res":
        # For sub-meter detail, use very small buffer (10-50m) and maximum zoom
        buffer_size = min(buffer_size, 50)   # Cap at 50m for ultra-high detail
        zoom_level = max(zoom_level, 20)     # Minimum zoom 20 for building level
    
    # Create a buffer around the point
    area = point.buffer(buffer_size)
    
    # Get imagery based on resolution mode
    if resolution_mode == "ultra_high_res":
        # Ultra-high resolution mode - sub-meter precision for building/street level detail
        
        # SkySat imagery (0.5-1m resolution) - commercial high-res
        skysat_collection = None
        try:
            skysat_collection = (ee.ImageCollection('SKYSAT/GEN-A/PUBLIC/ORTHO/RGB')
                               .filterBounds(area)
                               .filterDate(start_date, end_date)
                               .filter(ee.Filter.lt('CLOUD_COVER', 5))
                               .sort('CLOUD_COVER'))
        except:
            pass
        
        # WorldView imagery (0.3-0.5m resolution) - commercial very high-res
        worldview_collection = None
        try:
            worldview_collection = (ee.ImageCollection('WORLDVIEW/WV04/PANSHARPENED')
                                  .filterBounds(area)
                                  .filterDate(start_date, end_date)
                                  .filter(ee.Filter.lt('cloud_cover', 5))
                                  .sort('cloud_cover'))
        except:
            pass
        
        # GeoEye-1 imagery (0.5m resolution) - commercial high-res
        geoeye_collection = None
        try:
            geoeye_collection = (ee.ImageCollection('GEOEYE/GE01/PANSHARPENED')
                               .filterBounds(area)
                               .filterDate(start_date, end_date)
                               .filter(ee.Filter.lt('cloud_cover', 5))
                               .sort('cloud_cover'))
        except:
            pass
        
        # NAIP imagery (1m resolution) - highest free resolution for US
        naip_collection = None
        try:
            naip_collection = (ee.ImageCollection('USDA/NAIP/DOQQ')
                             .filterBounds(area)
                             .filterDate('2018-01-01', '2022-12-31')
                             .sort('system:time_start', False))
        except:
            pass
        
        # Sentinel-2 MSI (10m resolution) - backup
        sentinel_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                              .filterBounds(area)
                              .filterDate(start_date, end_date)
                              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 5))
                              .sort('CLOUDY_PIXEL_PERCENTAGE'))
        
    elif resolution_mode == "high_res":
        # Use high-resolution datasets for block-level analysis
        
        # PlanetScope imagery (3-5m resolution) - if available
        planet_collection = None
        try:
            planet_collection = (ee.ImageCollection('PLANET/PSScene/Visual')
                               .filterBounds(area)
                               .filterDate(start_date, end_date)
                               .filter(ee.Filter.lt('cloud_cover', 0.1))
                               .sort('cloud_cover'))
        except:
            pass
        
        # Sentinel-2 (10m resolution) - primary for high-res
        sentinel_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                              .filterBounds(area)
                              .filterDate(start_date, end_date)
                              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                              .sort('CLOUDY_PIXEL_PERCENTAGE'))
        
        # NAIP imagery (1m resolution) - if available in US
        naip_collection = None
        try:
            naip_collection = (ee.ImageCollection('USDA/NAIP/DOQQ')
                             .filterBounds(area)
                             .filterDate('2018-01-01', '2022-12-31')  # NAIP has limited temporal coverage
                             .sort('system:time_start', False))
        except:
            pass
        
        # Landsat (30m) - backup
        landsat_collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                             .filterBounds(area)
                             .filterDate(start_date, end_date)
                             .filter(ee.Filter.lt('CLOUD_COVER', 10))
                             .sort('CLOUD_COVER'))
    else:
        # Standard resolution datasets
        landsat_collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                             .filterBounds(area)
                             .filterDate(start_date, end_date)
                             .filter(ee.Filter.lt('CLOUD_COVER', 20))
                             .sort('CLOUD_COVER'))
        
        sentinel_collection = (ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
                              .filterBounds(area)
                              .filterDate(start_date, end_date)
                              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                              .sort('CLOUDY_PIXEL_PERCENTAGE'))
    
    # Get the best (least cloudy) images
    best_images = {}
    
    if resolution_mode == "ultra_high_res":
        # Ultra-high resolution mode - get best from each dataset
        if 'worldview_collection' in locals() and worldview_collection:
            try:
                best_images['worldview'] = worldview_collection.first()
            except:
                pass
        
        if 'geoeye_collection' in locals() and geoeye_collection:
            try:
                best_images['geoeye'] = geoeye_collection.first()
            except:
                pass
        
        if 'skysat_collection' in locals() and skysat_collection:
            try:
                best_images['skysat'] = skysat_collection.first()
            except:
                pass
        
        if 'naip_collection' in locals() and naip_collection:
            try:
                best_images['naip'] = naip_collection.first()
            except:
                pass
        
        best_images['sentinel'] = sentinel_collection.first()
        
    elif resolution_mode == "high_res":
        # High resolution mode - get best from each dataset
        if 'naip_collection' in locals() and naip_collection:
            try:
                best_images['naip'] = naip_collection.first()
            except:
                pass
        
        if 'planet_collection' in locals() and planet_collection:
            try:
                best_images['planet'] = planet_collection.first()
            except:
                pass
        
        best_images['sentinel'] = sentinel_collection.first()
        best_images['landsat'] = landsat_collection.first()
    else:
        # Standard mode
        best_images['landsat'] = landsat_collection.first()
        best_images['sentinel'] = sentinel_collection.first()
    
    # Calculate tiles for the area
    tiles_info = calculate_tiles_for_area(lat, lon, zoom_level, buffer_size)
    
    # Get image URLs with higher resolution for high_res mode
    image_urls = {}
    dimensions = 2048 if resolution_mode == "ultra_high_res" else (1024 if resolution_mode == "high_res" else 512)
    
    try:
        # WorldView visualization parameters (0.3-0.5m resolution) - highest commercial
        if 'worldview' in best_images and best_images['worldview']:
            worldview_url = best_images['worldview'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png'
            })
            image_urls['worldview'] = worldview_url
        
        # GeoEye-1 visualization parameters (0.5m resolution) - commercial high-res
        if 'geoeye' in best_images and best_images['geoeye']:
            geoeye_url = best_images['geoeye'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png'
            })
            image_urls['geoeye'] = geoeye_url
        
        # SkySat visualization parameters (0.5-1m resolution) - commercial high-res
        if 'skysat' in best_images and best_images['skysat']:
            skysat_url = best_images['skysat'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png'
            })
            image_urls['skysat'] = skysat_url
        
        # NAIP visualization parameters (1m resolution)
        if 'naip' in best_images and best_images['naip']:
            naip_url = best_images['naip'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png'
            })
            image_urls['naip'] = naip_url
        
        # Planet visualization parameters (3-5m resolution)
        if 'planet' in best_images and best_images['planet']:
            planet_url = best_images['planet'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png'
            })
            image_urls['planet'] = planet_url
        
        # Sentinel-2 visualization parameters (10m resolution)
        sentinel_vis_params = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0.0,
            'max': 3000,
            'gamma': 1.4
        }
        
        if 'sentinel' in best_images and best_images['sentinel']:
            sentinel_url = best_images['sentinel'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png',
                **sentinel_vis_params
            })
            image_urls['sentinel'] = sentinel_url
        
        # Landsat visualization parameters (30m resolution)
        landsat_vis_params = {
            'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
            'min': 0.0,
            'max': 0.3,
            'gamma': 1.4
        }
        
        if 'landsat' in best_images and best_images['landsat']:
            landsat_url = best_images['landsat'].getThumbURL({
                'region': area,
                'dimensions': dimensions,
                'format': 'png',
                **landsat_vis_params
            })
            image_urls['landsat'] = landsat_url
            
    except Exception as e:
        print(f"Error getting image URLs: {e}")
        image_urls = {}
    
    # Get image metadata
    metadata = {}
    try:
        for dataset_name, image in best_images.items():
            if image:
                try:
                    props = image.getInfo()['properties']
                    if dataset_name == 'landsat':
                        metadata[dataset_name] = {
                            'date': props.get('DATE_ACQUIRED'),
                            'cloud_cover': props.get('CLOUD_COVER'),
                            'scene_id': props.get('LANDSAT_SCENE_ID'),
                            'resolution': '30m'
                        }
                    elif dataset_name == 'sentinel':
                        metadata[dataset_name] = {
                            'date': props.get('PRODUCT_ID', '').split('_')[2][:8] if 'PRODUCT_ID' in props else None,
                            'cloud_cover': props.get('CLOUDY_PIXEL_PERCENTAGE'),
                            'product_id': props.get('PRODUCT_ID'),
                            'resolution': '10m'
                        }
                    elif dataset_name == 'worldview':
                        metadata[dataset_name] = {
                            'date': props.get('acquisition_date'),
                            'cloud_cover': props.get('cloud_cover'),
                            'resolution': '0.3-0.5m',
                            'dataset': 'WorldView'
                        }
                    elif dataset_name == 'geoeye':
                        metadata[dataset_name] = {
                            'date': props.get('acquisition_date'),
                            'cloud_cover': props.get('cloud_cover'),
                            'resolution': '0.5m',
                            'dataset': 'GeoEye-1'
                        }
                    elif dataset_name == 'skysat':
                        metadata[dataset_name] = {
                            'date': props.get('ACQUIRED'),
                            'cloud_cover': props.get('CLOUD_COVER'),
                            'resolution': '0.5-1m',
                            'dataset': 'SkySat'
                        }
                    elif dataset_name == 'naip':
                        metadata[dataset_name] = {
                            'date': props.get('system:time_start'),
                            'resolution': '1m',
                            'dataset': 'NAIP'
                        }
                    elif dataset_name == 'planet':
                        metadata[dataset_name] = {
                            'date': props.get('acquired'),
                            'cloud_cover': props.get('cloud_cover'),
                            'resolution': '3-5m',
                            'dataset': 'PlanetScope'
                        }
                except Exception as e:
                    print(f"Error getting metadata for {dataset_name}: {e}")
                    
    except Exception as e:
        print(f"Error getting metadata: {e}")
        metadata = {}
    
    # Prepare final result
    result = {
        'timestamp': datetime.now().isoformat(),
        'location': {
            'latitude': lat,
            'longitude': lon,
            'buffer_size_meters': buffer_size
        },
        'configuration': {
            'resolution_mode': resolution_mode,
            'zoom_level': zoom_level,
            'start_date': start_date,
            'end_date': end_date
        },
        'tiles_info': tiles_info,
        'image_urls': image_urls,
        'metadata': metadata,
        'image_collections_info': {
            'landsat_count': landsat_collection.size().getInfo() if 'landsat_collection' in locals() and landsat_collection else 0,
            'sentinel_count': sentinel_collection.size().getInfo() if 'sentinel_collection' in locals() and sentinel_collection else 0
        }
    }
    
    # Add high-res and ultra-high-res specific collection info
    if resolution_mode == "ultra_high_res":
        if 'worldview_collection' in locals() and worldview_collection:
            try:
                result['image_collections_info']['worldview_count'] = worldview_collection.size().getInfo()
            except:
                result['image_collections_info']['worldview_count'] = 0
        
        if 'geoeye_collection' in locals() and geoeye_collection:
            try:
                result['image_collections_info']['geoeye_count'] = geoeye_collection.size().getInfo()
            except:
                result['image_collections_info']['geoeye_count'] = 0
        
        if 'skysat_collection' in locals() and skysat_collection:
            try:
                result['image_collections_info']['skysat_count'] = skysat_collection.size().getInfo()
            except:
                result['image_collections_info']['skysat_count'] = 0
        
        if 'naip_collection' in locals() and naip_collection:
            try:
                result['image_collections_info']['naip_count'] = naip_collection.size().getInfo()
            except:
                result['image_collections_info']['naip_count'] = 0
    
    elif resolution_mode == "high_res":
        if 'naip_collection' in locals() and naip_collection:
            try:
                result['image_collections_info']['naip_count'] = naip_collection.size().getInfo()
            except:
                result['image_collections_info']['naip_count'] = 0
        
        if 'planet_collection' in locals() and planet_collection:
            try:
                result['image_collections_info']['planet_count'] = planet_collection.size().getInfo()
            except:
                result['image_collections_info']['planet_count'] = 0
    
    # Save JSON if requested with organized directory structure
    if save_json:
        # Create organized directory structure
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        data_dir = os.path.join(output_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"earth_engine_data_{resolution_mode}_{timestamp_str}.json"
        filepath = os.path.join(data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Data saved to: {filepath}")
            result['saved_to'] = filepath
        except Exception as e:
            print(f"Error saving JSON: {e}")
    
    return result

def calculate_tiles_for_area(lat: float, lon: float, zoom: int, buffer_meters: int) -> Dict:
    """
    Calculate tile coordinates for a given area.
    
    Args:
        lat: Latitude
        lon: Longitude
        zoom: Zoom level
        buffer_meters: Buffer size in meters
    
    Returns:
        Dictionary with tile information
    """
    import math
    
    # Convert buffer from meters to degrees (approximate)
    lat_buffer = buffer_meters / 111000  # 1 degree lat ≈ 111km
    lon_buffer = buffer_meters / (111000 * math.cos(math.radians(lat)))
    
    # Calculate bounding box
    north = lat + lat_buffer
    south = lat - lat_buffer
    east = lon + lon_buffer
    west = lon - lon_buffer
    
    # Convert lat/lon to tile coordinates
    def deg2tile(lat_deg, lon_deg, zoom):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        x = int((lon_deg + 180.0) / 360.0 * n)
        y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (x, y)
    
    # Get tile bounds
    x_min, y_max = deg2tile(south, west, zoom)
    x_max, y_min = deg2tile(north, east, zoom)
    
    tiles = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.append({
                'x': x,
                'y': y,
                'z': zoom,
                'url': f"https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={zoom}"
            })
    
    return {
        'zoom_level': zoom,
        'bounding_box': {
            'north': north,
            'south': south,
            'east': east,
            'west': west
        },
        'tile_count': len(tiles),
        'tiles': tiles
    }

def download_image_from_url(url: str, filename: str, output_dir: str = "output") -> bool:
    """
    Download an image from URL to local file in organized directory structure.
    
    Args:
        url: Image URL
        filename: Local filename to save
        output_dir: Output directory (default: "output")
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create images subdirectory
        images_dir = os.path.join(output_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        # Full path for the image file
        filepath = os.path.join(images_dir, filename)
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"Image saved to {filepath}")
        return True
    except Exception as e:
        print(f"Error downloading image {filename}: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # San Francisco coordinates (downtown)
    sf_lat = 37.7749
    sf_lon = -122.4194
    
    print("=== Standard Resolution Mode ===")
    try:
        result_standard = get_san_francisco_tiles_and_images(
            lat=sf_lat,
            lon=sf_lon,
            zoom_level=12,
            buffer_size=1000,  # 1km buffer
            resolution_mode="standard",
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
        
        print(f"Standard mode completed. JSON saved to: {result_standard.get('saved_to', 'N/A')}")
        print(f"Available images: {list(result_standard['image_urls'].keys())}")
        
        # Download images if URLs are available
        for dataset, url in result_standard['image_urls'].items():
            filename = f"sf_{dataset}_standard.png"
            download_image_from_url(url, filename, "output/standard")
            
    except Exception as e:
        print(f"Error in standard mode: {e}")
    
    print("\n=== High Resolution Mode (Block Level) ===")
    try:
        result_highres = get_san_francisco_tiles_and_images(
            lat=sf_lat,
            lon=sf_lon,
            zoom_level=18,     # Higher zoom for block level
            buffer_size=100,   # Smaller buffer (100m) for block level
            resolution_mode="high_res",
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
        
        print(f"High-res mode completed. JSON saved to: {result_highres.get('saved_to', 'N/A')}")
        print(f"Available images: {list(result_highres['image_urls'].keys())}")
        print(f"Resolution details:")
        for dataset, meta in result_highres['metadata'].items():
            print(f"  {dataset}: {meta.get('resolution', 'Unknown')} resolution")
        
        # Download high-res images
        for dataset, url in result_highres['image_urls'].items():
            filename = f"sf_{dataset}_highres.png"
            download_image_from_url(url, filename, "output/high_res")
            
    except Exception as e:
        print(f"Error in high-res mode: {e}")
    
    print("\n=== Ultra-High Resolution Mode (Building Level) ===")
    try:
        result_ultrahighres = get_san_francisco_tiles_and_images(
            lat=sf_lat,
            lon=sf_lon,
            zoom_level=20,     # Maximum zoom for building level
            buffer_size=25,    # Very small buffer (25m) for building detail
            resolution_mode="ultra_high_res",
            start_date="2023-01-01",
            end_date="2023-12-31"
        )
        
        print(f"Ultra-high-res mode completed. JSON saved to: {result_ultrahighres.get('saved_to', 'N/A')}")
        print(f"Available images: {list(result_ultrahighres['image_urls'].keys())}")
        print(f"Resolution details:")
        for dataset, meta in result_ultrahighres['metadata'].items():
            print(f"  {dataset}: {meta.get('resolution', 'Unknown')} resolution")
        
        # Download ultra-high-res images
        for dataset, url in result_ultrahighres['image_urls'].items():
            filename = f"sf_{dataset}_ultrahighres.png"
            download_image_from_url(url, filename, "output/ultra_high_res")
            
    except Exception as e:
        print(f"Error in ultra-high-res mode: {e}")
    
    print("\n=== Resolution Comparison Summary ===")
    try:
        modes = []
        if 'result_standard' in locals():
            modes.append(('Standard', result_standard))
        if 'result_highres' in locals():
            modes.append(('High-Res', result_highres))
        if 'result_ultrahighres' in locals():
            modes.append(('Ultra-High-Res', result_ultrahighres))
        
        for mode_name, result in modes:
            print(f"\n{mode_name} Mode:")
            print(f"  Datasets: {list(result['image_urls'].keys())}")
            print(f"  Buffer size: {result['location']['buffer_size_meters']}m")
            print(f"  Zoom level: {result['configuration']['zoom_level']}")
            print(f"  Image dimensions: {2048 if result['configuration']['resolution_mode'] == 'ultra_high_res' else (1024 if result['configuration']['resolution_mode'] == 'high_res' else 512)}px")
    except:
        pass