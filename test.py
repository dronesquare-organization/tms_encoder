from encoder import TMSPathEncoder, Polygon, Point

# Encoder 객체 생성
encoder = TMSPathEncoder(root="./orthomosaic_tiles", epsg=5186, level=23)

print("========== 타일 경로를 좌표로 변환 ==========")

# INPUT
tile_path = "./orthomosaic_tiles/23/7156367/5137722.png"
# OUTPUT
tile_xy = encoder.tms2xy(tile_path)
tile_lnglat = encoder.tms2lnglat(tile_path)

print(f"타일: {tile_path}")
print(f"타일의 xy 좌표: {tile_xy}")
print(f"타일의 경위도 좌표: {tile_lnglat}")


print("========== 좌표를 타일 경로로 변환 ==========")

# INPUT
lng, lat = 127.117956, 37.485553
# OUTPUT
tile_path = encoder.lnglat2tms(lng, lat)  # xy좌표를 위한 xy2tms 메서드도 있음

print(f"경위도 좌표: {lng, lat}")
print(f"좌표에 대한 타일 경로: {tile_path}")


print("========== 구역 내 타일 경로 탐색 ==========")

# INPUT
area_polygon = [  # 구역을 지정하는 다각형 x,y좌표 배열 정의
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

print(f"대상 구역: {area_polygon}")
print(f"대상 구역 내 타일들 (총{len(inner_tiles)}개), 샘플: {inner_tiles[0]}")
