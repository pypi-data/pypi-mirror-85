from typing import Set, Tuple

import numpy as np
# from nptyping import NDArray

AnglesTuple = Tuple[int, int, int, int]


class BtfFromNpz:
    """BTFDBBのzipファイルから角度や画像を取り出す。"""

    def __init__(self, npz_filepath: str) -> None:
        """使用するzipファイルを指定する。"""
        npz = np.load(npz_filepath)
        self.angles = npz["angles"]
        self.images = npz["images"]

    def get_angles_set(self) -> Set[AnglesTuple]:
        """zip内の"jpg"ファイル名から角度情報を取得し、intのタプルの集合で返す。"""
        return set(self.angles)

    def angles_to_image(self, tl: float, pl: float, tv: float, pv: float) -> np.ndarray:
        """`tl`, `pl`, `tv`, `pv`の角度を持つ画像の実体をndarray形式で返す。"""
        for i, angle in enumerate(self.angles):
            if np.allclose(angle, np.array((tl, pl, tv, pv), dtype=np.float)):
                return self.images[i]


if __name__ == "__main__":
    btf = BtfFromNpz("SweatNavyblue-1D.btf.npz")
    print(btf.angles_to_image(1,0,0,0))
