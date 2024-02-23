import math
from pyproj import Transformer


def crs_transformer(from_epsg: int, to_epsg: int):
    """좌표계 변환기 생성자"""
    return Transformer.from_crs(from_epsg, to_epsg, always_xy=True).transform


class CrsConverter:
    def __init__(self, xy_epsg):
        self.epsg = xy_epsg
        self._lnglat_to_xy = crs_transformer(4326, xy_epsg)
        self._xy_to_lnglat = crs_transformer(xy_epsg, 4326)

    def lnglat_to_xy(self, lng: float, lat: float) -> tuple:
        return self._lnglat_to_xy(lng, lat)

    def xy_to_lnglat(self, x: float, y: float) -> tuple:
        lng, lat = self._xy_to_lnglat(x, y)
        return lng, lat


class TmsConverter:
    def __init__(self, z: int):
        """
        - z: 타일 레벨 지정
        """
        self.z = z

    def tms2lnglat(self, x, y):
        # TMS에서 사용되는 y 좌표 변환 (TMS는 y 좌표가 반대로 계산될 수 있음)
        n = 2.0**self.z
        y = n - y - 1

        # 경위도 계산
        lng = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
        lat = math.degrees(lat_rad)

        return (lng, lat)

    def lnglat2tms(self, lng, lat):
        lat_rad = math.radians(lat)
        n = 2.0**self.z
        x = int((lng + 180.0) / 360.0 * n)

        _l = 1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi
        y = int(_l / 2.0 * n)

        # TMS의 y 좌표 체계에 맞게 y 좌표 변환
        y = int(n - y - 1)

        return (x, y)
