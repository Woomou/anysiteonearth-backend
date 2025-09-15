# Ultra-High Resolution Earth Engine API

An advanced Google Earth Engine-based tool for acquiring ultra-high resolution satellite imagery with sub-meter precision for block and building-level detailed analysis.

> **🌍 English Version**: [README_EN.md](./README_EN.md) | **中文版**: [README.md](./README.md)

## 🚀 Core Features

### Resolution Mode Comparison

| Mode | Resolution | Use Case | Buffer Zone | Tile Zoom |
|------|------------|----------|-------------|-----------|
| **standard** | 10-30m | City-level analysis | 500-2000m | 12-15 |
| **high_res** | 1-10m | Block-level analysis | 50-200m | 16-18 |
| **ultra_high_res** | 0.3-1m | Building-level analysis | 10-50m | 19-21 |

### Data Source Support

#### Ultra-High Resolution Sources (ultra_high_res mode)
- **WorldView-4** - 0.3-0.5m resolution (Commercial highest precision)
- **GeoEye-1** - 0.5m resolution (Commercial high precision)
- **SkySat** - 0.5-1m resolution (Commercial high precision)
- **NAIP** - 1m resolution (US free highest precision)
- **Sentinel-2** - 10m resolution (Backup)

#### High Resolution Sources (high_res mode)
- **NAIP** - 1m resolution
- **PlanetScope** - 3-5m resolution
- **Sentinel-2** - 10m resolution
- **Landsat-8** - 30m resolution

#### Standard Resolution Sources (standard mode)
- **Landsat-8** - 30m resolution
- **Sentinel-2** - 10m resolution

## 📦 Installation

```bash
# Clone repository
git clone <repository-url>
cd anysiteonearth-backend

# Install dependencies
pip install -r requirements.txt

# Configure Earth Engine authentication
earthengine authenticate
```

## 🔧 Basic Usage

### 1. Ultra-High Resolution Mode (Building-level detail)

```python
from earth_engine_utils import get_san_francisco_tiles_and_images

# Ultra-high resolution - Building-level detail within 25m radius
result = get_san_francisco_tiles_and_images(
    lat=37.7749,                    # San Francisco downtown
    lon=-122.4194,
    resolution_mode="ultra_high_res",  # Sub-meter precision
    buffer_size=25,                 # 25m radius (about half a block)
    zoom_level=20,                  # Building-level zoom
    save_json=True                  # Auto-save JSON data
)

print(f"Data saved to: {result['saved_to']}")
print(f"Available datasets: {list(result['image_urls'].keys())}")

# Display resolution details
for dataset, meta in result['metadata'].items():
    print(f"{dataset}: {meta['resolution']} resolution")
```

### 2. High Resolution Mode (Block-level)

```python
# High resolution - Block-level analysis within 100m radius
result = get_san_francisco_tiles_and_images(
    lat=37.7749,
    lon=-122.4194,
    resolution_mode="high_res",     # 1-10m resolution
    buffer_size=100,                # 100m radius (1-2 blocks)
    zoom_level=18
)
```

### 3. Standard Resolution Mode (City-level)

```python
# Standard resolution - City-level analysis within 1km radius
result = get_san_francisco_tiles_and_images(
    lat=37.7749,
    lon=-122.4194,
    resolution_mode="standard",     # 10-30m resolution
    buffer_size=1000,               # 1km radius
    zoom_level=12
)
```

## 🌍 Global Location Support

### 📊 **Data Coverage by Region**

| Region | Best Mode | Resolution | Available Datasets |
|--------|-----------|------------|-------------------|
| 🇺🇸 **USA** | `ultra_high_res` | **0.3-1m** | NAIP + Commercial + Global |
| 🏙️ **Major Global Cities** | `high_res` | **1-10m** | Some Commercial + Global |
| 🌍 **Other Global Locations** | `standard` | **10-30m** | Sentinel-2 + Landsat |
| 🏝️ **Remote Areas** | `standard` | **30m** | Landsat only |

### 🧪 **Test Global Locations**

```bash
python location_test.py
```

This script tests 8 locations across different continents:
- 🇺🇸 New York (Full coverage)
- 🇨🇳 Beijing (Global datasets)
- 🇬🇧 London (Global datasets)
- 🇧🇷 São Paulo (Global datasets)
- 🇰🇪 Nairobi (Global datasets)
- 🇦🇺 Sydney (Global datasets)
- 🇯🇵 Tokyo (Global datasets)
- 🏝️ Remote Pacific Island (Limited coverage)

### 💡 **Usage Recommendations**

```python
# 🇺🇸 US locations - Highest precision
result = get_san_francisco_tiles_and_images(
    lat=40.7128, lon=-74.0060,  # New York
    resolution_mode="ultra_high_res"  # 0.3m precision
)

# 🌍 Other global locations - Standard precision
result = get_san_francisco_tiles_and_images(
    lat=39.9042, lon=116.4074,  # Beijing
    resolution_mode="standard"  # 10-30m precision
)
```

## 📊 JSON Data Output

Each run automatically generates timestamped JSON files:

```json
{
  "timestamp": "2023-09-15T14:30:22.123456",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "buffer_size_meters": 25
  },
  "configuration": {
    "resolution_mode": "ultra_high_res",
    "zoom_level": 20,
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  },
  "tiles_info": {
    "zoom_level": 20,
    "tile_count": 16,
    "tiles": [...]
  },
  "image_urls": {
    "worldview": "https://earthengine.googleapis.com/...",
    "naip": "https://earthengine.googleapis.com/...",
    "sentinel": "https://earthengine.googleapis.com/..."
  },
  "metadata": {
    "worldview": {
      "resolution": "0.3-0.5m",
      "date": "2023-08-15",
      "cloud_cover": 2.1
    }
  }
}
```

## 📁 Organized File Structure

```
output/
├── standard/
│   ├── data/           # JSON data files
│   └── images/         # Standard resolution images
├── high_res/
│   ├── data/
│   └── images/         # High resolution images
└── ultra_high_res/
    ├── data/
    └── images/         # Ultra-high resolution images
```

## 🎯 Precision Comparison Examples

Run demo scripts to see different precision effects:

```bash
# Run basic functionality demo
python earth_engine_utils.py

# Run ultra-high resolution specific demo
python ultra_high_res_demo.py

# Test download functionality
python test_download.py
```

### Precision Comparison Results

| Mode | Buffer | Image Size | Tile Count | Best Resolution |
|------|--------|------------|------------|-----------------|
| Standard | 1000m | 512px | 4 | 10m |
| High-Res | 100m | 1024px | 16 | 1m |
| Ultra-High-Res | 25m | 2048px | 64 | 0.3m |

## 🏗️ Modeling Applications

### Ultra-High Resolution Mode suitable for:
- **Building Detection**: Individual building identification and outline extraction
- **Urban Planning**: Street layout and building density analysis
- **Infrastructure Monitoring**: Precise measurement of roads, parking lots, green spaces
- **Vegetation Analysis**: Tree-level vegetation coverage
- **Change Detection**: Building construction/demolition monitoring
- **Disaster Assessment**: Precise damage extent evaluation

### Technical Advantages:
- **Sub-meter Precision**: 0.3-0.5m resolution, capable of identifying vehicle-sized targets
- **Multi-source Fusion**: Commercial + free data source combination
- **Real-time Data**: Support for latest satellite imagery data
- **Automated Processing**: One-click acquisition of multi-resolution data
- **Complete Metadata**: Including acquisition time, cloud cover, data sources, etc.

## 📈 Performance Optimization

### Recommended Parameter Settings:

```python
# Building-level analysis (Highest precision)
ultra_high_params = {
    'resolution_mode': 'ultra_high_res',
    'buffer_size': 15,      # 15-25m
    'zoom_level': 21,       # Maximum zoom
    'dimensions': 2048      # 2K image
}

# Block-level analysis (Balance precision and efficiency)
high_res_params = {
    'resolution_mode': 'high_res',
    'buffer_size': 50,      # 50-100m
    'zoom_level': 18,
    'dimensions': 1024      # 1K image
}
```

## 🔍 Data Source Details

### WorldView-4 (0.3-0.5m)
- Highest commercial resolution
- Suitable for: Precise building outlines, infrastructure details
- Coverage: Major global cities

### NAIP (1m) 
- Highest free resolution within USA
- Suitable for: Detailed analysis of US cities
- Update frequency: 2-3 years

### Sentinel-2 (10m)
- Free high-frequency updates
- Suitable for: Large-scale vegetation and land use
- Update frequency: 5 days

## 🚨 Important Notes

1. **Commercial Data Permissions**: WorldView, GeoEye, etc. require corresponding Earth Engine permissions
2. **Regional Limitations**: NAIP covers only within USA
3. **Cloud Filtering**: Ultra-high resolution mode uses stricter cloud cover threshold (<5%)
4. **Data Size**: Ultra-high resolution image files are larger, mind storage space
5. **API Quotas**: High-frequency requests may hit Earth Engine usage limits

## 📞 Technical Support

For higher precision or specific regional data support, consider:
- Drone aerial survey data (centimeter-level precision)
- LiDAR data (3D point clouds)
- High-resolution aerial imagery for specific regions

## 🎯 Key Features

- **ANY Global Coordinates**: Works anywhere on Earth with appropriate resolution mode
- **Automatic JSON Saving**: Complete metadata and configuration saved with timestamps
- **Organized File Structure**: Images and data files properly organized by resolution
- **Multiple Data Sources**: Automatic fallback from commercial to free datasets
- **Flexible Buffer Sizes**: From 15m (building-level) to 2000m (city-level)
- **Maximum Precision**: Up to 0.3m resolution for building-level analysis

---

**This represents the highest precision achievable through Google Earth Engine (0.3-0.5m resolution), sufficient for building-level detailed analysis and modeling.**

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Earth Engine for providing satellite imagery data
- Various satellite data providers (Landsat, Sentinel, NAIP, WorldView, etc.)
- Open source community for tools and libraries used