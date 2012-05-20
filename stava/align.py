# alignment.py
# A dynamic programming algorithm for sequence alignment

gp = 3    # gap penalty
mmc = 1   # mismatch cost


def alignment(X, Y):
  m = len(X)
  n = len(Y)

  c = []                     # c[i][j] = optimal alignment cost
  for i in range(m + 1):     # for X_i and Y_j
    temp = [0] * (n + 1)
    c.append(temp)

  for i in range(m + 1):     # fill in 0th row and column of c
    c[i][0] = i * gp         # with gap costs
  for j in range(n + 1):
    c[0][j] = j * gp

  printMatrix(c)

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if X[i - 1] == Y[j - 1]:         # initialize c[i][j] to cost of
        c[i][j] = c[i-1][j-1]          # (mis)matching x_i and y_j
      else:                            # plus the optimal cost of 
        c[i][j] = mmc + c[i-1][j-1]    # aligning X_i-1 and Y_j-1

      if gp + c[i-1][j] < c[i][j]:     # check if aligning x_i with a
        c[i][j] = gp + c[i-1][j]       # gap is better

      if gp + c[i][j-1] < c[i][j]:     # check if aligning y_j with a
        c[i][j] = gp + c[i][j-1]       # gap is better

    printMatrix(c)

  return c[m][n]                       # c[m][n] is the final alignment cost


def printMatrix(m):
  print "Cost matrix:"
  for row in m:
    print "  ", row
  print


