import scipy.io as scio
import scipy.sparse.linalg as scsplinalg
import numpy as np
import time

def jacobiIteration(x, A, diagA, b, rstop, maxTimes):
    dim = x.size
    oldX = x
    relError = []
    #mainloop
    for times in range(maxTimes):
        newXDiff = (b - A.dot(oldX)) / diagA

        #print(f"np.linalg.norm(newXDiff) = {np.linalg.norm(newXDiff)}")
        #print(f"np.linalg.norm(oldX) = {np.linalg.norm(oldX)}")
        
        
        #tempRelError = (np.linalg.norm(newXDiff)/np.linalg.norm(oldX) if np.linalg.norm(oldX) != 0 else np.linalg.norm(newXDiff))
        #relError.append(tempRelError)
        #if np.lingalg.norm(x) <= rstop * np.linalg.norm(oldX):
        if np.linalg.norm(newXDiff) <= rstop * np.linalg.norm(oldX):
            break
        oldX += newXDiff

    return times, oldX



####### 疎行列の読み込みと情報表示 #######
print("Infomation")
filename = "../data/bcsstm22.mtx"
#filename = "../data/memplus.mtx"
#filename = "../data/ash85.mtx"
#filename = "../data/1138_bus.mtx"
#filename = "../data/lns_3937.mtx"
#filename = "../data/orani678.mtx"
#filename = "../data/data.mtx"
info = scio.mminfo(filename)
rowDim = info[0]
colDim = info[1]
print(info, "\n")
print("Loading")
A = scio.mmread(filename) #COO方式
A = A.tocsr() 


####### 連立方程式を用意 #######
print("Make Ax = b equation")
trueX = np.arange(1, colDim + 1)
b = A.dot(trueX)
print("True solution")
print(f"trueX = {trueX}")
print("Ax = b")
print(f"A = \n{A}")
print(f"b = \n{b}\n")

####### Jacobi法の実行 #######
print("Execute Jacobi Method\n")
diagA = A.diagonal()
x = np.zeros(colDim) #初期値x_0 = 0
rstop = 10e-10 #更新量の相対値に関する基準
maxTimes = colDim * 10
startTime = time.time()
iterativeTimes, x = jacobiIteration(x, A, diagA, b, rstop, maxTimes)
endTime = time.time()
processTime = endTime - startTime

####### Jacobi反復法の結果表示 #######
print("Show result")
print(f"trueX = \n{trueX}")
print(f"x = \n{x}")
print()

####### Jacobi法の解析 #######
print("Show Analysis")
print(f"time = {processTime}")
print(f"iterativeTimes = {iterativeTimes}")

#Aが対角優位かどうかを調べる

flag = True
for i in range(rowDim):
    absSum = 0
    absDiag = 0
    for j in range(A.indptr[i], A.indptr[i+1]):
        if i == A.indices[j]:
            absDiag = abs(A.data[j])
        else:
            absSum += abs(A.data[j])
    if absDiag < absSum:
        flag = False
        break

if flag:
    print("Diagonal dominaice")
else:
    print("Not Diagonal dominance")

#計算の誤差を調べる
relErrorVec = np.absolute(trueX - x) / np.absolute(trueX)
relErrorNorm = np.linalg.norm(trueX - x) / np.linalg.norm(x)
maxRelIndex = np.argmax(relErrorVec)
minRelIndex = np.argmin(relErrorVec)

print(f"Relative Error(L2Norm) = {relErrorNorm:7.1e}") #e:指数表記
print(f"minRelError: x[{minRelIndex:5d}] = {x[minRelIndex]}, relError = {relErrorVec[minRelIndex]}")
print(f"maxRelError: x[{maxRelIndex:5d}] = {x[maxRelIndex]}, relError = {relErrorVec[maxRelIndex]}")

