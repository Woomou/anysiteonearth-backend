#!/usr/bin/env python3
"""
Test script for ultra-high resolution image download
"""

from earth_engine_utils import get_san_francisco_tiles_and_images
import os

def test_ultra_high_res_download():
    """
    Test ultra-high resolution image download with proper error handling
    """
    print("Testing ultra-high resolution image download...")
    
    try:
        result = get_san_francisco_tiles_and_images(
            lat=37.7749,
            lon=-122.4194,
            zoom_level=20,
            buffer_size=25,
            resolution_mode="ultra_high_res",
            start_date="2023-01-01",
            end_date="2023-12-31",
            save_json=True,
            output_dir="output/test_ultra_high_res"
        )
        
        print(f"\n✓ Data collection completed")
        print(f"✓ JSON saved to: {result.get('saved_to', 'N/A')}")
        print(f"✓ Available image URLs: {len(result['image_urls'])}")
        
        # Check what datasets we got
        available_datasets = list(result['image_urls'].keys())
        print(f"✓ Datasets found: {available_datasets}")
        
        # Show metadata for available datasets
        if result['metadata']:
            print(f"\n📊 Dataset Details:")
            for dataset, meta in result['metadata'].items():
                resolution = meta.get('resolution', 'Unknown')
                date = meta.get('date', 'Unknown')
                cloud_cover = meta.get('cloud_cover', 'N/A')
                print(f"  • {dataset}: {resolution} resolution, acquired {date}, cloud cover: {cloud_cover}%")
        
        # Test image downloads
        print(f"\n📥 Downloading images...")
        download_count = 0
        for dataset, url in result['image_urls'].items():
            print(f"  Downloading {dataset}...")
            filename = f"sf_{dataset}_test_ultra.png"
            
            # Import download function
            from earth_engine_utils import download_image_from_url
            success = download_image_from_url(url, filename, "output/test_ultra_high_res")
            
            if success:
                download_count += 1
                # Check file size
                filepath = os.path.join("output/test_ultra_high_res/images", filename)
                if os.path.exists(filepath):
                    size_mb = os.path.getsize(filepath) / (1024 * 1024)
                    print(f"    ✓ {dataset}: {size_mb:.2f} MB")
                else:
                    print(f"    ✗ {dataset}: File not found after download")
            else:
                print(f"    ✗ {dataset}: Download failed")
        
        print(f"\n📈 Summary:")
        print(f"  • Total datasets available: {len(result['image_urls'])}")
        print(f"  • Successfully downloaded: {download_count}")
        print(f"  • Download success rate: {download_count/len(result['image_urls'])*100:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_ultra_high_res_download()
    
    if result:
        print(f"\n🎉 Test completed successfully!")
        print(f"Check the 'output/test_ultra_high_res' directory for files:")
        print(f"  📁 data/ - JSON files")
        print(f"  📁 images/ - Downloaded images")
    else:
        print(f"\n❌ Test failed. Please check your Earth Engine authentication.")