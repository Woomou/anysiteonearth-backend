# Ultra-High Resolution Earth Engine API

基于Google Earth Engine的超高分辨率卫星影像获取工具，支持亚米级精度的街区和建筑级别详细分析。

## 🚀 核心功能

### 分辨率模式对比

| 模式 | 分辨率 | 适用场景 | 缓冲区 | 瓦片缩放 |
|------|--------|----------|--------|----------|
| **standard** | 10-30m | 城市级别分析 | 500-2000m | 12-15 |
| **high_res** | 1-10m | 街区级别分析 | 50-200m | 16-18 |
| **ultra_high_res** | 0.3-1m | 建筑级别分析 | 10-50m | 19-21 |

### 数据源支持

#### 超高分辨率数据源 (ultra_high_res模式)
- **WorldView-4** - 0.3-0.5m分辨率 (商业最高精度)
- **GeoEye-1** - 0.5m分辨率 (商业高精度)
- **SkySat** - 0.5-1m分辨率 (商业高精度)
- **NAIP** - 1m分辨率 (美国境内免费最高精度)
- **Sentinel-2** - 10m分辨率 (备选)

#### 高分辨率数据源 (high_res模式)
- **NAIP** - 1m分辨率
- **PlanetScope** - 3-5m分辨率
- **Sentinel-2** - 10m分辨率
- **Landsat-8** - 30m分辨率

#### 标准分辨率数据源 (standard模式)
- **Landsat-8** - 30m分辨率
- **Sentinel-2** - 10m分辨率

## 📦 安装

```bash
# 克隆代码
git clone <repository-url>
cd anysiteonearth-backend

# 安装依赖
pip install -r requirements.txt

# 配置Earth Engine认证
earthengine authenticate
```

## 🔧 基本使用

### 1. 超高分辨率模式 (建筑级别细节)

```python
from earth_engine_utils import get_san_francisco_tiles_and_images

# 超高分辨率 - 25米范围内的建筑级别细节
result = get_san_francisco_tiles_and_images(
    lat=37.7749,                    # 旧金山市中心
    lon=-122.4194,
    resolution_mode="ultra_high_res",  # 亚米级精度
    buffer_size=25,                 # 25米半径 (约半个街区)
    zoom_level=20,                  # 建筑级别缩放
    save_json=True                  # 自动保存JSON数据
)

print(f"数据已保存到: {result['saved_to']}")
print(f"可用数据集: {list(result['image_urls'].keys())}")

# 显示分辨率详情
for dataset, meta in result['metadata'].items():
    print(f"{dataset}: {meta['resolution']} 分辨率")
```

### 2. 高分辨率模式 (街区级别)

```python
# 高分辨率 - 100米范围内的街区级别分析
result = get_san_francisco_tiles_and_images(
    lat=37.7749,
    lon=-122.4194,
    resolution_mode="high_res",     # 1-10米分辨率
    buffer_size=100,                # 100米半径 (1-2个街区)
    zoom_level=18
)
```

### 3. 标准分辨率模式 (城市级别)

```python
# 标准分辨率 - 1公里范围内的城市级别分析
result = get_san_francisco_tiles_and_images(
    lat=37.7749,
    lon=-122.4194,
    resolution_mode="standard",     # 10-30米分辨率
    buffer_size=1000,               # 1公里半径
    zoom_level=12
)
```

## 📊 JSON数据输出

每次运行都会自动生成带时间戳的JSON文件：

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

## 🎯 精度对比示例

运行演示脚本查看不同精度效果：

```bash
# 运行基本功能演示
python earth_engine_utils.py

# 运行超高分辨率专项演示
python ultra_high_res_demo.py
```

### 精度对比结果示例

| 模式 | 缓冲区 | 图片尺寸 | 瓦片数量 | 最佳分辨率 |
|------|--------|----------|----------|------------|
| Standard | 1000m | 512px | 4 | 10m |
| High-Res | 100m | 1024px | 16 | 1m |
| Ultra-High-Res | 25m | 2048px | 64 | 0.3m |

## 🏗️ 建模应用场景

### 超高分辨率模式适用于:
- **建筑物检测**: 单体建筑识别和轮廓提取
- **城市规划**: 街道布局和建筑密度分析
- **基础设施监控**: 道路、停车场、绿地精确测量
- **植被分析**: 单棵树木级别的植被覆盖
- **变化检测**: 建筑物新建、拆除监控
- **灾害评估**: 精确的损害范围评估

### 技术优势:
- **亚米级精度**: 0.3-0.5米分辨率，可识别车辆大小目标
- **多数据源融合**: 商业+免费数据源组合
- **实时数据**: 支持最新的卫星影像数据
- **自动化处理**: 一键获取多种分辨率数据
- **完整元数据**: 包含采集时间、云量、数据源等信息

## 📈 性能优化

### 推荐参数设置:

```python
# 建筑级别分析 (最高精度)
ultra_high_params = {
    'resolution_mode': 'ultra_high_res',
    'buffer_size': 15,      # 15-25米
    'zoom_level': 21,       # 最大缩放
    'dimensions': 2048      # 2K图片
}

# 街区级别分析 (平衡精度和效率)
high_res_params = {
    'resolution_mode': 'high_res',
    'buffer_size': 50,      # 50-100米
    'zoom_level': 18,
    'dimensions': 1024      # 1K图片
}
```

## 🔍 数据源详情

### WorldView-4 (0.3-0.5m)
- 最高商业分辨率
- 适合: 精确建筑物轮廓、基础设施细节
- 覆盖: 全球主要城市

### NAIP (1m) 
- 美国境内免费最高分辨率
- 适合: 美国城市的详细分析
- 更新频率: 2-3年

### Sentinel-2 (10m)
- 免费高频更新
- 适合: 大范围植被和土地利用
- 更新频率: 5天

## 🚨 注意事项

1. **商业数据权限**: WorldView、GeoEye等需要相应的Earth Engine权限
2. **区域限制**: NAIP仅覆盖美国境内
3. **云量筛选**: 超高分辨率模式使用更严格的云量阈值(<5%)
4. **数据大小**: 超高分辨率图片文件较大，注意存储空间
5. **API配额**: 高频率请求可能触及Earth Engine使用限额

## 📞 技术支持

如需要更高精度或特定区域的数据支持，可以考虑:
- 无人机航拍数据 (厘米级精度)
- 激光雷达数据 (3D点云)
- 特定区域的高分辨率航空影像

---

**这是目前通过Google Earth Engine可以达到的最高精度 (0.3-0.5米分辨率)，足以进行建筑级别的详细分析和建模。**