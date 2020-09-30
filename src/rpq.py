from pygraphblas import Matrix, BOOL, lib


def rpq(g, r):
    kron = g.get_intersection(r)

    closure_matrix = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in kron.matrices:
        if kron.matrices[label].nrows < kron.size:
            kron.matrices[label].resize(kron.size, kron.size)
        closure_matrix += kron.matrices[label]

    tmp = closure_matrix.dup()
    closure_matrix += closure_matrix @ closure_matrix
    while not tmp.iseq(closure_matrix):
        tmp = closure_matrix
        closure_matrix += closure_matrix @ closure_matrix

    res = Matrix.sparse(BOOL, g.size, g.size)
    for i, j, _ in zip(*closure_matrix.select(lib.GxB_NONZERO).to_lists()):
        i_g, i_r = i // r.size, i % r.size
        j_g, j_r = j // r.size, j % r.size
        res[i_g, j_g] = True

    return kron, res
