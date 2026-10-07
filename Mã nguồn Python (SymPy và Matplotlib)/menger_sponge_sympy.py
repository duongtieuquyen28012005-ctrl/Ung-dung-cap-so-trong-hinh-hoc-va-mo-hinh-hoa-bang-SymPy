"""
Bot bien Menger - dung SymPy de tinh the tich con lai chinh xac (phan so),
dung Matplotlib 3D (voxels) de ve hinh.
Ung voi muc 2.4 trong bao cao nhom.
"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, LinearSegmentedColormap

a = 9  # canh hinh lap phuong ban dau (nhu de bai trong file nhom)


def is_kept(ix, iy, iz, n):
    """Kiem tra o nho (ix,iy,iz) trong luoi 3^n x 3^n x 3^n co duoc GIU LAI hay
    khong, bang cach xet tung chu so co so 3 cua ix,iy,iz: o bi loai neu, o bat
    ky muc nao, co TU HAI toa do tro len bang 1 (tam khoi hoac tam mat)."""
    for _ in range(n):
        dx, dy, dz = ix % 3, iy % 3, iz % 3
        count_center = (dx == 1) + (dy == 1) + (dz == 1)
        if count_center >= 2:
            return False
        ix //= 3
        iy //= 3
        iz //= 3
    return True


def build_grid(n):
    size = 3 ** n
    grid = np.zeros((size, size, size), dtype=bool)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                grid[i, j, k] = is_kept(i, j, k, n)
    return grid


def remaining_volume_exact(a, n):
    """The tich con lai chinh xac sau n buoc: V(n) = a^3 * (20/27)^n."""
    a_sym = sp.nsimplify(a)
    return sp.simplify(a_sym**3 * sp.Rational(20, 27) ** n)


if __name__ == "__main__":
    n_values = [0, 1, 2]
    fig = plt.figure(figsize=(5.8 * len(n_values), 5.8))

    for idx, n in enumerate(n_values):
        grid = build_grid(n)
        V_exact = remaining_volume_exact(a, n)
        print(f"n = {n}: so khoi nho con lai = {grid.sum()}, "
              f"the tich chinh xac = {V_exact}  (xap xi {float(V_exact):.3f})")

        ax = fig.add_subplot(1, len(n_values), idx + 1, projection="3d")

        # To mau theo khoang cach den tam khoi -> tao hieu ung dam nhat (lop
        # ngoai sang mau hon, cac "hang" o sau toi dan), ket hop LightSource
        # de co do bong 3 chieu ro net hon.
        size = grid.shape[0]
        c = (size - 1) / 2
        ii, jj, kk = np.indices(grid.shape)
        dist = np.sqrt((ii - c) ** 2 + (jj - c) ** 2 + (kk - c) ** 2)
        dist_norm = dist / dist.max() if dist.max() > 0 else dist

        cmap = LinearSegmentedColormap.from_list("menger", ["#f7c59f", "#8c1c13"])
        facecolors = cmap(0.25 + 0.65 * dist_norm)

        ls = LightSource(azdeg=315, altdeg=55)
        ax.voxels(grid, facecolors=facecolors, edgecolor=(0, 0, 0, 0.25),
                  linewidth=0.15, shade=True, lightsource=ls)
        ax.set_title(f"n = {n}", pad=10, fontsize=26)
        ax.set_box_aspect([1, 1, 1])
        ax.view_init(elev=22, azim=38)
        ax.set_axis_off()

    plt.tight_layout(pad=1.5)
    plt.savefig("menger_sponge.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: menger_sponge.png")
