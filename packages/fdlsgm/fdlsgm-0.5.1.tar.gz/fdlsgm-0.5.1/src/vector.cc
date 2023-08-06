/**
 * @file baseline.cc
 * @brief Base Line Class
 * @author Ryou Ohsawa
 * @year 2020
 */
#include "linalg.h"

namespace linalg {

  const vector2<double>
  normalize_vector(const vector2<double>& v)
  {
    double n = std::sqrt(v[0]*v[0]+v[1]*v[1]);
    return { v[0]/n, v[1]/n };
  }

  const vector3<double>
  normalize_vector(const vector3<double>& v)
  {
    double n = std::sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2]);
    return { v[0]/n, v[1]/n, v[2]/n };
  }

  const vector3<double>
  outer_product(const vector3<double>& o1, const vector3<double>& o2)
  {
    const double& x = o1[1]*o2[2] - o1[2]*o2[1];
    const double& y = o1[2]*o2[0] - o1[0]*o2[2];
    const double& z = o1[0]*o2[1] - o1[1]*o2[0];
    return { x, y, z };
  }
  const vector3<double>
  outer_product(const vector4<double>& o1, const vector4<double>& o2)
  {
    const double& x = o1[1]*o2[2] - o1[2]*o2[1];
    const double& y = o1[2]*o2[0] - o1[0]*o2[2];
    const double& z = o1[0]*o2[1] - o1[1]*o2[0];
    return { x, y, z };
  }

  const vector3<double>
  linalg_gauss_solve(const matrix3x3<double>& A, const vector3<double>& b)
  {
    vector3<double> x;
    vector3<double> Ap0 =
      { 1.0, A[1][0]/A[0][0], A[2][0]/A[0][0] };
    vector3<double> Ap1 =
      { 0.0, A[1][1]-A[0][1]*Ap0[1], A[2][1]-A[0][1]*Ap0[2] };
    vector3<double> Ap2 =
      { 0.0, A[1][2]-A[0][2]*Ap0[1], A[2][2]-A[0][2]*Ap0[2] };
    double bp0 = b[0]/A[0][0];
    double bp1 = b[1]-A[0][1]*bp0;
    double bp2 = b[2]-A[0][2]*bp0;

    /* normalize Ap1,bp1 */
    bp1 /= Ap1[1];
    Ap1[2] /= Ap1[1]; Ap1[1] = 1.0;
    /* eliminate Ap2[1] */
    bp2 -= bp1*Ap2[1];
    Ap2[2] -= Ap2[1]*Ap1[2]; Ap2[1] = 0.0;
    /* normalize Ap2,bp2 */
    bp2 /= Ap2[2]; Ap2[2] = 1.0;

    x[2] = bp2;
    x[1] = bp1 - Ap1[2]*x[2];
    x[0] = bp0 - Ap0[1]*x[1] - Ap0[2]*x[2];
    return x;
  }

  const vector3<double>
  linalg_gauss_solve(const matrix4x4<double>& U)
  {
    const matrix3x3<double> A =
      { vector3<double>{ U[0][0], U[0][1], U[0][2] },
        vector3<double>{ U[1][0], U[1][1], U[1][2] },
        vector3<double>{ U[2][0], U[2][1], U[2][2] } };
    const vector3<double> b = { U[0][3], U[1][3], U[2][3] };
    return linalg_gauss_solve(A, b);
  }
}
