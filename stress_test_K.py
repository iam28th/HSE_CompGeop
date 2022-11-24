import os
import subprocess as sp
import random

program = "./K10"
test_dir = 'gen_tests'
N_TESTS = 1000

points_min = 1
points_max = 100
coord_lim = 10**9
x_range = [-coord_lim, coord_lim]
repeat_prob = 0.05
y_range = [-coord_lim, coord_lim]

random.seed(0)

try:
    os.mkdir(test_dir)
except FileExistsError:
    pass

print('ans', 'cor', sep='\t')
for test_number in range(1, N_TESTS + 1):

    lines = []
    n_points = random.randint(points_min, points_max)
    lines.append(None)
    repeats = 0
    pts = []
    for i in range(n_points):
        x = random.randint(*x_range)
        y = random.randint(*y_range)
        while True:
            lines.append(f"{x} {y}\n")
            pts.append((x, y))
            if random.random() < repeat_prob:
                repeats += 1
            else:
                break
    n_points += repeats
    lines[0] = str(n_points) + '\n'

    path_to_input = test_dir + '/' + str(test_number) + '.txt'
    with open(path_to_input, 'w') as f:
        f.writelines(lines)

    cmd = [program, "<", path_to_input]
    cmd = f"{program} < {path_to_input}"
    pr = sp.run(cmd, capture_output=True, check=True, shell=True)
    ans = float(pr.stdout.splitlines()[-1])


    def sqDist(A, B):
        v = (B[0] - A[0], B[1] - A[1])
        return v[0]**2 + v[1]**2

    d2 = 0
    for i in range(n_points):
        for j in range(i + 1, n_points):
            d2 = max(d2, sqDist(pts[i], pts[j]))

    EPS = 1e-10
    cor = d2**0.5
    if abs(cor - ans) > EPS:
        print(f'Failed test {test_number}. {ans} {cor}')
