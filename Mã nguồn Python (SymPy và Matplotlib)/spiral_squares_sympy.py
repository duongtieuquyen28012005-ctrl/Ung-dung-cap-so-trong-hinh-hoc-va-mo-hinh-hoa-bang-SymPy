"""
Hinh vuong xoan oc - dung SymPy de suy ra ti so dong dang CHINH XAC tu dieu kien
goc 30 do, dung Matplotlib de ve chuoi hinh vuong long nhau xoay dan.
Ung voi muc 2.4 trong bao cao nhom.
"""
import sympy as sp
import matplotlib.pyplot as plt

# ----- Buoc 1: suy ra ti so dong dang k tu dieu kien goc A1 A2 D2 = 30 do -----
# Diem A2 tren canh A1B1 cach A1 mot doan x (0<x<1, canh hinh vuong = 1).
# Tam giac A1 A2 D2 vuong tai A1: A1A2 = x, A1D2 = 1 - x.
# Goc tai A2 (tuc goc A1 A2 D2) co tan(goc) = doi/ke = (1-x)/x = tan(30 do).
x = sp.symbols('x', positive=True)
goc = sp.pi / 6  # 30 do
nghiem = sp.solve(sp.Eq((1 - x) / x, sp.tan(goc)), x)
x_val = nghiem[0]
print("Vi tri diem chia x (tinh tu moi dinh, canh hinh vuong = 1):", x_val,
      " = ", sp.nsimplify(x_val), "~", float(x_val))

k = sp.sqrt(x_val**2 + (1 - x_val)**2)   # ti so dong dang giua 2 hinh vuong lien tiep
k = sp.simplify(k)
print("Ti so dong dang k = S2/S1 (do dai) =", k, " ~", float(k))
print("Cong boi dien tich q = k^2 =", sp.simplify(k**2), " ~", float(k**2))


def next_square(square, x_val):
    """square: list 4 dinh [A,B,C,D] (theo thu tu). Tra ve hinh vuong moi
    A'B'C'D' voi A' tren AB cach A doan x*|AB|, B' tren BC cach B doan x*|BC|, ..."""
    new_square = []
    for i in range(4):
        P, Q = square[i], square[(i + 1) % 4]
        newP = (P[0] + x_val * (Q[0] - P[0]), P[1] + x_val * (Q[1] - P[1]))
        new_square.append(newP)
    return new_square


if __name__ == "__main__":
    x_num = float(x_val)
    A1 = (0.0, 0.0)
    B1 = (1.0, 0.0)
    C1 = (1.0, 1.0)
    D1 = (0.0, 1.0)
    square0 = [A1, B1, C1, D1]

    # Sinh truoc toan bo day hinh vuong (toi da can dung cho panel cuoi)
    N_max = 14
    all_squares = [square0]
    sq = square0
    for _ in range(N_max - 1):
        sq = next_square(sq, x_num)
        all_squares.append(sq)

    # Ve theo TIEN TRINH long nhau: moi panel cho them 1 vai hinh vuong moi,
    # cac hinh vuong cua buoc truoc duoc giu lai (mo hon) de thay ro qua trinh
    # hinh thanh chuoi xoan oc qua tung giai doan.
    panel_counts = [1, 3, 6, 10, 14]
    fig, axes = plt.subplots(1, len(panel_counts), figsize=(4.8 * len(panel_counts), 5))
    cmap = plt.cm.viridis

    for ax, count in zip(axes, panel_counts):
        for i in range(count):
            square = all_squares[i]
            xs = [p[0] for p in square] + [square[0][0]]
            ys = [p[1] for p in square] + [square[0][1]]
            # hinh vuong MOI NHAT cua panel to/dam, cac hinh truoc nhat hon
            is_latest = (i == count - 1)
            ax.plot(xs, ys, color=cmap(i / N_max),
                    linewidth=2.4 if is_latest else 1.1,
                    alpha=1.0 if is_latest else 0.55)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.set_aspect("equal")
        ax.set_title(f"Sau {count} hình vuông", pad=12, fontsize=22)
        ax.axis("off")

    plt.tight_layout(pad=1.5)
    plt.savefig("/home/claude/spiral_squares.png", dpi=150, bbox_inches="tight")
    print("Da luu hinh: spiral_squares.png")

    # ----- Tong dien tich toan chuoi (cap so nhan lui vo han) -----
    S1 = sp.Integer(1)  # dien tich hinh vuong dau (canh = 1)
    q = sp.simplify(k**2)
    S_total = sp.simplify(S1 / (1 - q))
    print(f"\nTong dien tich toan chuoi (vo han hinh vuong), S1 = 1:")
    print(f"S = S1 / (1 - q) = {S_total}  ~  {float(S_total):.5f}")
