def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("{:4d}".format(matrix[i][j]), end="")
        print()


n = int(input())
N = 1
vector = [1, -1]
res = []
i = 0
j = 0
o = n
res = [[0 for i in range(n)] for i in range(n)]

for o in range(n-1):
    res[0][j] = N
    N += 1
    j += 1
n -= 1

while n >= 0:
    for add in vector:
        for o in range(n):
            res[i][j] = N
            i += add
            N += 1
        for o in range(n):
            res[i][j] = N
            j -= add
            N += 1
        n -= 1
res[i][j] = N
print_matrix(res)