"""
Tam tham Sierpinski - dung SymPy de tinh toan chinh xac (phan so) dien tich
con lai qua tung buoc, dung Matplotlib de ve hinh.
Ung voi Vi du 1 trong tai lieu "Ung dung cap so trong hinh hoc".
"""
import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

a = 1  # canh hinh vuong ban dau


def sierpinski_squares(x, y, side, depth):
    """Tra ve danh sach cac hinh vuong CON LAI (dang (x, y, side), goc duoi-trai)
    sau 'depth' buoc lap, xuat phat tu hinh vuong canh 'side' tai goc (x, y).
    Day la de quy truc tiep tren hinh hoc, tuong ung voi lap luan trong Vi du 1."""
    if depth == 0:
        return [(x, y, side)]
    squares = []
    s3 = side / 3
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue  # bo o chinh giua
            squares += sierpinski_squares(x + i * s3, y + j * s3, s3, depth - 1)
    return squares


def remaining_area_exact(a, n):
    """Tinh dien tich CON LAI chinh xac (SymPy, dang phan so) sau n lan chia,
    doi chieu voi cong thuc trong bai: S_con_lai(n) = a^2 * (8/9)^n."""
    a_sym = sp.nsimplify(a)
    return sp.simplify(a_sym**2 * sp.Rational(8, 9) ** n)


if __name__ == "__main__":
    n_values = [0, 1, 2, 3]
    fig, axes = plt.subplots(1, len(n_values), figsize=(4.6 * len(n_values), 4.6))

    for ax, n in zip(axes, n_values):
        squares = sierpinski_squares(0, 0, a, n)
        S_exact = remaining_area_exact(a, n)
        print(f"n = {n}: so hinh vuong con lai = {len(squares)}, "
              f"dien tich con lai chinh xac = {S_exact}  (xap xi {float(S_exact):.5f})")

        for (x, y, s) in squares:
            ax.add_patch(patches.Rectangle((float(x), float(y)), float(s), float(s),
                                            facecolor="steelblue", edgecolor="none"))
        ax.set_xlim(0, a)
        ax.set_ylim(0, a)
        ax.set_aspect("equal")
        ax.set_title(f"n = {n}", pad=12, fontsize=26)
        ax.axis("off")

    plt.tight_layout(pad=1.5)
    plt.savefig("sierpinski_carpet.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: sierpinski_carpet.png")
