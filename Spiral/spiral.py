def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("{:4d}".format(matrix[i][j]), end="")
        print()


n = int(input())
N = 0
vector = [1, -1]
res = [[0 for k in range(n)] for m in range(n)]
i = 0
j = -1

# ЗАПОЛНЕНИЕ ПЕРВОЙ СТРОКИ МАТРИЦЫ
for o in range(n):
    j += 1
    N += 1
    res[0][j] = N
n -= 1

while n >= 0:
    for add in vector:
        for o in range(n):
            i += add
            N += 1
            res[i][j] = N
        for o in range(n):
            j -= add
            N += 1
            res[i][j] = N
        n -= 1
print_matrix(res)
