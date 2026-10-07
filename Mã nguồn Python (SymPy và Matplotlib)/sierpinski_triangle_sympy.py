"""
Tam giac Sierpinski - dung SymPy de tinh dien tich con lai chinh xac (phan so),
dung Matplotlib de ve hinh.
Ung voi muc 2.3 trong bao cao nhom.
"""
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

a = 1  # canh tam giac deu ban dau


def midpoint(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def sierpinski_triangles(p1, p2, p3, depth):
    """De quy: tra ve danh sach cac tam giac CON LAI (moi phan tu la (p1,p2,p3))
    sau 'depth' buoc chia (bo tam giac giua)."""
    if depth == 0:
        return [(p1, p2, p3)]
    m12, m23, m31 = midpoint(p1, p2), midpoint(p2, p3), midpoint(p3, p1)
    tris = []
    tris += sierpinski_triangles(p1, m12, m31, depth - 1)
    tris += sierpinski_triangles(m12, p2, m23, depth - 1)
    tris += sierpinski_triangles(m31, m23, p3, depth - 1)
    return tris


def remaining_area_exact(a, n):
    """Dien tich con lai chinh xac sau n lan chia: S(n) = (a^2*sqrt3/4) * (3/4)^n."""
    a_sym = sp.nsimplify(a)
    S0 = a_sym**2 * sp.sqrt(3) / 4
    return sp.simplify(S0 * sp.Rational(3, 4) ** n)


if __name__ == "__main__":
    h = a * sp.sqrt(3) / 2
    P1, P2, P3 = (0, 0), (a, 0), (a / 2, float(h))

    n_values = [0, 1, 3, 5]
    fig, axes = plt.subplots(1, len(n_values), figsize=(4.6 * len(n_values), 4.6))

    for ax, n in zip(axes, n_values):
        tris = sierpinski_triangles(P1, P2, P3, n)
        S_exact = remaining_area_exact(a, n)
        print(f"n = {n}: so tam giac con lai = {len(tris)}, "
              f"dien tich chinh xac = {S_exact}  (xap xi {float(S_exact):.5f})")

        for (q1, q2, q3) in tris:
            ax.add_patch(patches.Polygon([q1, q2, q3], closed=True,
                                          facecolor="seagreen", edgecolor="none"))
        ax.set_xlim(0, a)
        ax.set_ylim(0, float(h))
        ax.set_aspect("equal")
        ax.set_title(f"n = {n}", pad=12, fontsize=26)
        ax.axis("off")

    plt.tight_layout(pad=1.5)
    plt.savefig("sierpinski_triangle.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: sierpinski_triangle.png")

    # Dien tich con lai sau 10 lan chia (theo de bai trong file nhom)
    print("\nDien tich con lai sau 10 lan chia, lam tron hang phan chuc:")
    S10 = remaining_area_exact(a, 10)
    print(f"S(10) = {S10} = {float(S10):.1f}  (voi a = {a})")
