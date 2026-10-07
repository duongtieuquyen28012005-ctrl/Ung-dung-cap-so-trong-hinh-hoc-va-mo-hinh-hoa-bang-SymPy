"""
Doan thang Cantor - dung SymPy de tinh tong do dai con lai chinh xac (phan so),
dung Matplotlib de ve hinh (bac thang cac doan qua tung muc).
Ung voi muc 2.4 trong bao cao nhom.
"""
import sympy as sp
import matplotlib.pyplot as plt

a = 1  # do dai doan thang ban dau


def cantor_intervals(start, end, depth):
    """De quy: tra ve danh sach cac doan CON LAI (start, end) sau 'depth' buoc
    (chia 3, xoa doan giua)."""
    if depth == 0:
        return [(start, end)]
    third = (end - start) / 3
    left = (start, start + third)
    right = (end - third, end)
    return cantor_intervals(*left, depth - 1) + cantor_intervals(*right, depth - 1)


def remaining_length_exact(a, n):
    """Tong do dai con lai chinh xac sau n buoc: L(n) = a * (2/3)^n."""
    a_sym = sp.nsimplify(a)
    return sp.simplify(a_sym * sp.Rational(2, 3) ** n)


if __name__ == "__main__":
    N = 6  # so muc ve
    fig, ax = plt.subplots(figsize=(10, 5))

    for n in range(N + 1):
        segs = cantor_intervals(0, a, n)
        L_exact = remaining_length_exact(a, n)
        print(f"n = {n}: so doan con lai = {len(segs)}, "
              f"tong do dai chinh xac = {L_exact}  (xap xi {float(L_exact):.5f})")
        y = N - n  # muc n ve o do cao y (muc 0 o tren cung)
        for (s, e) in segs:
            ax.plot([float(s), float(e)], [y, y], color="darkorange", linewidth=4,
                    solid_capstyle="butt")

    ax.set_yticks(range(N + 1))
    ax.set_yticklabels([f"n={N - y}" for y in range(N + 1)], fontsize=20)
    ax.tick_params(axis="x", labelsize=18)
    ax.set_xlim(-0.02, a + 0.02)
    ax.set_ylim(-0.5, N + 0.5)
    ax.set_xlabel("x", fontsize=22)
    plt.tight_layout(pad=1.5)
    plt.savefig("cantor_set.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: cantor_set.png")
