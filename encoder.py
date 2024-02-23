from pathlib import Path

import numpy as np

from converter import CrsConverter, TmsConverter
from geo import Polygon, Point


class TMSEncoder:

    def __init__(self, epsg: int, level: int):
        self.crs = CrsConverter(epsg)
        self.tms = TmsConverter(level)

    def lnglat2tms(self, lng: float, lat: float):
        """
        - 경위도에 대한 타일의 x,y 값을 반환합니다.
        """
        return self.tms.lnglat2tms(lng, lat)

    def xy2tms(self, x: float, y: float):
        """
        - x,y좌표에 대한 타일의 x,y 값을 반환합니다.
        """
        return self.tms.lnglat2tms(*self.crs.xy_to_lnglat(x, y))

    def tms2lnglat(self, tx: int, ty: int):
        """
        - 타일의 x,y값에 대한 경위도를 반환합니다.
        """
        return self.tms.tms2lnglat(tx, ty)

    def tms2xy(self, tx: int, ty: int):
        """
        - 타일의 x,y값에 대한 xy좌표를 반환합니다.
        """
        return self.crs.lnglat_to_xy(*self.tms.tms2lnglat(tx, ty))

    def polygon2tms(self, polygon: Polygon):
        """
        - 다각형 내부에 위치한 모든 타일의 x,y값을 반환합니다.
        """
        assert polygon.is_valid
        polygon_arr = np.array(
            [self.crs.xy_to_lnglat(p.x, p.y) for p in polygon.points]
        )

        min_lng, max_lng = polygon_arr[:, 0].min(), polygon_arr[:, 0].max()
        min_lat, max_lat = polygon_arr[:, 1].min(), polygon_arr[:, 1].max()

        min_tx, min_ty = self.lnglat2tms(min_lng, min_lat)
        max_tx, max_ty = self.lnglat2tms(max_lng, max_lat)

        x_range = range(min_tx, max_tx + 1)
        y_range = range(min_ty, max_ty + 1)
        target_tiles = [
            [tx, ty]
            for tx in x_range
            for ty in y_range
            if Point(*self.tms2xy(tx, ty)) in polygon
        ]
        return target_tiles


class TMSPathEncoder(TMSEncoder):

    def __init__(self, root: Path | str, epsg: int, level: int):
        """
        - root: 타일의 디렉토리 경로
        - epsg: XY 좌표계의 EPSG 코드
        - level: 타일 레벨
        """
        self.root = Path(root)
        super().__init__(epsg, level)

    def path2txy(self, path: Path | str):
        """
        - 타일 경로에서 타일의 x,y값을 추출합니다.
        """
        path = Path(path)
        return int(path.parts[-2]), int(path.stem)

    def txy2path(self, tx: int, ty: int):
        """
        - 타일 x,y값을 경로로 변환합니다.
        """
        return self.root / f"{self.tms.z}/{tx}/{ty}.png"

    def lnglat2tms(self, lng: float, lat: float):
        """
        - 경위도 좌표에 위치한 타일 경로를 반환합니다.
        """
        return self.txy2path(*super().lnglat2tms(lng, lat))

    def xy2tms(self, x: float, y: float):
        """
        - x,y좌표에 위치한 타일 경로를 반환합니다.
        """
        return self.txy2path(*super().xy2tms(x, y))

    def tms2lnglat(self, path: Path | str):
        """
        - 타일의 경위도 좌표를 반환합니다.
        - path 예시: "orthomosaic_tiles/17/111817/80276.png"
        """
        return super().tms2lnglat(*self.path2txy(path))

    def tms2xy(self, path: Path | str):
        """
        - 타일의 xy좌표를 반환합니다.
        - path 예시: "orthomosaic_tiles/17/111817/80276.png"
        """
        return super().tms2xy(*self.path2txy(path))

    def polygon2tms(self, polygon: Polygon):
        """
        - 다각형 내부에 위치한 모든 타일의 경로를 반환합니다.
        """
        txy_arr = TMSEncoder(self.crs.epsg, self.tms.z).polygon2tms(polygon)
        return [self.txy2path(tx, ty) for tx, ty in txy_arr]
