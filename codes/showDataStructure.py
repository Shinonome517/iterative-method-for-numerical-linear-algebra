import numpy as np
import scipy.sparse as scsp

mat_a = np.array([
    [1, 0, 2, 0, 0],
    [0, 3, 0, 0, -4],
    [0, 0, 5, 0, 0],
    [6, 0, 0, -7, 0],
    [0, 0, 0, 0, 8]
])

print(f"A = \n{mat_a}")

print()

coo_a = scsp.coo_matrix(mat_a)
print("COO")
print(f"C = \n{coo_a}")

print()

csr_a = scsp.csr_matrix(mat_a)
print("CSR")
print(f"A = \n{csr_a}")
print(f"A.getnnz() = {csr_a.getnnz()} ")
print(f"A.data = {csr_a.data}")
print(f"A.indices = {csr_a.indices} ")
print(f"A.indptr = {csr_a.indptr}")

print()

csc_a = scsp.csc_matrix(mat_a)
print("CSC")
print(f"A = \n{csc_a}")