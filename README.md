## 경위도 좌표에 기반한 계산을 TMS 경로로 인코딩하는 Python 패키지

- 원하는 프로젝트에 클론하여 사용하세요

### TMSPathEncoder 메서드 목록

- path2txy: 타일 경로에서 타일의 x,y값을 반환합니다.
- txy2path: 타일 x,y값을 경로로 변환해 반환합니다.
- lnglat2tms: 경위도 좌표에 위치한 타일 경로를 반환합니다.
- xy2tms: x,y좌표에 위치한 타일 경로를 반환합니다.
- tms2lnglat: 타일의 경위도 좌표를 반환합니다.
- tms2xy: 타일의 xy좌표를 반환합니다.
- polygon2tms: 다각형 내부에 위치한 모든 타일의 경로를 반환합니다.

### 예시 코드

```python
from tms_encoder import TMSPathEncoder, Polygon, Point

# Encoder 객체 정의
encoder = TMSPathEncoder(root="./orthomosaic_tiles", epsg=5186, level=23)

# ========== 1. 타일 경로를 좌표로 변환 ==========

# INPUT
tile_path = "./orthomosaic_tiles/23/7156367/5137722.png"
# OUTPUT
tile_xy = encoder.tms2xy(tile_path)
tile_lnglat = encoder.tms2lnglat(tile_path)


# ========== 2. 좌표를 타일 경로로 변환 ==========

# INPUT
lng, lat = 127.117956, 37.485553
# OUTPUT
tile_path = encoder.lnglat2tms(lng, lat)  # xy좌표를 위한 xy2tms 메서드도 있음


# ========== 3. 구역 내 타일 경로 탐색 ==========

# INPUT
area_polygon = [  # 구역을 지정하는 다각형 x,y좌표 배열
    [210444.61, 542924.79],
    [210437.68, 542912.79],
    [210433.86, 542903.09],
    [210441.79, 542908.07],
    [210434.42, 542895.01],
    [210459.32, 542905.53],
    [210475.90, 542908.28],
    [210477.14, 542922.22],
    [210465.95, 542937.51],
    [210456.16, 542920.63],
]
# OUTPUT
inner_tiles = encoder.polygon2tms(Polygon(*[Point(x, y) for x, y in area_polygon]))
```
