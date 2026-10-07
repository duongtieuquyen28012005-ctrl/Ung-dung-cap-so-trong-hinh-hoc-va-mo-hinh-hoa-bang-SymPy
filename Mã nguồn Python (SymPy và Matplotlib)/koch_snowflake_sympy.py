"""
Bong tuyet Von Koch - dung SymPy de dung toa do chinh xac (dai so),
dung Matplotlib de ve hinh.
Ung voi Vi du 2 trong tai lieu "Ung dung cap so trong hinh hoc".
"""
import sympy as sp
import matplotlib.pyplot as plt

a = 1  # do dai canh tam giac ban dau (co the doi thanh so khac)

def koch_step(points):
    """Nhan vao danh sach diem (sympy Point2D) mo ta mot duong gap khuc,
    tra ve danh sach diem moi sau 1 buoc lap Koch (moi doan thang -> 4 doan)."""
    new_points = [points[0]]
    for p1, p2 in zip(points, points[1:]):
        # chia doan p1p2 thanh 3, lay 2 diem chia va dinh "mui nhon"
        A = p1
        B = p1 + (p2 - p1) / 3
        D = p1 + (p2 - p1) * sp.Rational(2, 3)
        # dinh mui nhon tam giac deu: quay diem D quanh tam B mot goc -60 do
        peak = D.rotate(-sp.pi / 3, pt=B)
        new_points += [B, peak, D, p2]
    return new_points


def koch_snowflake_points(a, n):
    """Tra ve danh sach diem (sympy Point2D, toa do chinh xac) cua bong tuyet
    Koch sau n buoc lap, xuat phat tu tam giac deu canh a."""
    h = a * sp.sqrt(3) / 2
    A = sp.Point2D(0, 0)
    B = sp.Point2D(a, 0)
    C = sp.Point2D(a / 2, h)
    points = [A, B, C, A]  # tam giac deu, khep kin
    for _ in range(n - 1):
        points = koch_step(points)
    return points


def perimeter_exact(points):
    """Tinh chu vi CHINH XAC (dang can thuc) bang SymPy, cong dong do dai tung doan."""
    total = sp.Integer(0)
    for p1, p2 in zip(points, points[1:]):
        total += p1.distance(p2)
    return sp.simplify(total)


if __name__ == "__main__":
    n_values = [1, 2, 3, 4]
    fig, axes = plt.subplots(1, len(n_values), figsize=(4.6 * len(n_values), 4.6))

    for ax, n in zip(axes, n_values):
        pts = koch_snowflake_points(a, n)
        P_exact = perimeter_exact(pts)
        print(f"n = {n}: chu vi chinh xac P_{n} = {P_exact}  (xap xi {float(P_exact):.4f})")

        xs = [float(p.x) for p in pts]
        ys = [float(p.y) for p in pts]
        ax.plot(xs, ys, color="steelblue", linewidth=1.2)
        ax.fill(xs, ys, color="steelblue", alpha=0.25)
        ax.set_title(f"n = {n}", pad=12, fontsize=26)
        ax.set_aspect("equal")
        ax.axis("off")

    plt.tight_layout(pad=1.5)
    plt.savefig("koch_snowflake.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: koch_snowflake.png")
