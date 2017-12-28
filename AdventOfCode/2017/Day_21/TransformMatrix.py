"""
Kelly O'Shaughnessy
Rotate nxn matrix by 90 degrees
https://gist.github.com/KellyOShaughnessy/f2096470ad73dcb8d77c
"""
def rotateMatrix(matrix):
    if matrix is None or len(matrix)<1:
        return
    else:
        if len(matrix)==1:
            return matrix
        else:
            #solution matrix
            soln = [row[:] for row in matrix]
            #size of matrix
            m = len(matrix[0])
                    
            for x in range(0,m):
                for j in range(0,m):
                    soln[j][m-1-x] = matrix[x][j]
            return soln
### rotate


def flipMatrix(matrix):
    return matrix[::-1]
### flipMatrix