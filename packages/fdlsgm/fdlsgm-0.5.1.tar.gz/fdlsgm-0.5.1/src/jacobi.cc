/**
 * @file jacobi.cc
 * @brief Singular Value Decomposition with Jacobi algorithm
 * @author Ryou Ohsawa
 * @year 2020
 */
#include "linalg.h"


namespace linalg {

  constexpr index_t matrix_size = 4;
  constexpr index_t max_iter = 2e3;


  /** index of the largest off-diagonal element in k-th row */
  const index_t
  maximum_index_row(const matrix4x4<double>& matrix,
                    const index_t k)
  {
    index_t m = k+1;
    for (index_t i=k+2; i<matrix_size; i++)
      if (std::abs(matrix[i][k]) > std::abs(matrix[m][k])) m = i;
    return m;
  }

  /** update eigen value vector */
  void
  update_eigen_value(vector4<double>& eigen,
                     vector4<bool>& changed, index_t& state,
                     const index_t k, const double adv)
  {
    const double& eps = std::numeric_limits<double>::epsilon();
    eigen[k] += adv;
    if (changed[k] == true) {
      if (std::abs(adv) < eps) {
        changed[k] = false; state--;
      } else {
        changed[k] = true;
      }
    } else {
      if (std::abs(adv) >= eps) {
        changed[k] = true; state++;
      } else {
      }
    }
  }

  void
  rotate_matrix(matrix4x4<double>& matrix,
                const index_t k, const index_t l,
                const index_t i, const index_t j,
                const double cos, const double sin)
  {
    const double matrix_lk = matrix[l][k], matrix_ji = matrix[j][i];
    matrix[l][k] = cos*matrix_lk - sin*matrix_ji;
    matrix[j][i] = sin*matrix_lk + cos*matrix_ji;
  }

  const matrix4x4<double>
  calculate_checksum(const matrix4x4<double> A, const matrix4x4<double> U)
  {
    matrix4x4<double> X(zeros4x4);
    for (index_t i=0; i<matrix_size; i++)
      for (index_t j=0; j<matrix_size; j++)
        for (index_t l=0; l<matrix_size; l++)
          for (index_t m=0; m<matrix_size; m++)
            X[j][i] += U[j][m]*A[l][m]*U[i][l];
    return X;
  }

  const matrix4x4<double>
  eigenvector_jacobi_4x4(const matrix4x4<double>& input)
  {
    matrix4x4<double> S(input);
    matrix4x4<double> E(ident4x4);
    vector4<double> eigen;
    vector4<index_t> idx;
    vector4<bool> changed;

    // initialize working space.
    index_t state(matrix_size), nloop(0);
    for (index_t k=0; k<matrix_size; k++) {
      idx[k] = maximum_index_row(S, k);
      eigen[k] = S[k][k];
      changed[k] = true;
    }

    // main loop
    while (state > 0 && nloop < max_iter) {
      index_t m = 0;
      for (index_t k=1; k<matrix_size-1; k++)
        if (std::abs(S[idx[k]][k]) > std::abs(S[idx[m]][m])) m = k;

      // calculate rotation angle
      index_t k = m;
      index_t l = idx[m];
      const double& pv = S[l][k];
      const double& y = (eigen[l]-eigen[k])/2.0;
      const double& tan =
        (y>0)?pv/(y+std::sqrt(pv*pv+y*y)):pv/(y-std::sqrt(pv*pv+y*y));
      const double cos = 1.0/std::sqrt(1.0 + tan*tan);
      const double sin = tan/std::sqrt(1.0 + tan*tan);
      const double adv = -pv*tan;

      // update eigen values
      update_eigen_value(eigen, changed, state, k, +adv);
      update_eigen_value(eigen, changed, state, l, -adv);

      // rotate matrix
      S[l][k] = 0.0;
      for (index_t i=0;   i<k; i++)
        rotate_matrix(S, i, k, i, l, cos, sin);
      for (index_t i=k+1; i<l; i++)
        rotate_matrix(S, k, i, i, l, cos, sin);
      for (index_t i=l+1; i<matrix_size; i++)
        rotate_matrix(S, k, i, l, i, cos, sin);

       // rotate eigen vectors
      for (index_t i=0; i<matrix_size; i++)
        rotate_matrix(E, i, k, i, l, cos, sin);

      // update maximum index
      for (index_t i=0; i<matrix_size; i++)
        idx[i] = maximum_index_row(S, i);
      idx[l] = maximum_index_row(S, l);

      nloop++;
    }

    for (index_t k=0; k<matrix_size; k++) {
      for (index_t l=k+1; l<matrix_size; l++)
        S[l][k] = S[k][l];
      index_t m = k;
      for (index_t l=k+1; l<matrix_size; l++)
        if (eigen[l] < eigen[m]) m = l;
      if (k != m) {
        std::swap(eigen[k],eigen[m]);
        std::swap(E[k],E[m]);
      }
    }

    return E;
  }

}
