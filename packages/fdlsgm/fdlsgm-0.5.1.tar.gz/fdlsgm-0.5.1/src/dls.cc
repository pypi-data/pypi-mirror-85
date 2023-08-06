/**
 * @file dls.cc
 * @brief Directed Line Segment Class
 * @author Ryou Ohsawa
 * @year 2020
 */
#include "fdlsgm.h"


namespace fdlsgm {
  dls::dls()
    : dls(0.0,0.0,0.0,0.0,0.0,1.0) {}

  dls::dls(const vector3<double>& __v0, const vector3<double>& __v1)
    : dls(__v0[0], __v0[1], __v0[2], __v1[0], __v1[1], __v1[2]) {}

  dls::dls(const double& __x0, const double& __y0, const double& __z0,
           const double& __x1, const double& __y1, const double& __z1)
    : _x0(__x0),_y0(__y0),_z0(__z0),_x1(__x1),_y1(__y1),_z1(__z1),
      _r(std::sqrt(dx()*dx()+dy()*dy())),
      _l(std::sqrt(dx()*dx()+dy()*dy()+dz()*dz())),
      _pa(std::atan2(-dx(), dy()))
  {
    if (_l <= std::numeric_limits<double>::epsilon())
      throw std::invalid_argument("the length of dls is too small.");
  }

  dls::dls(const double* v)
    : dls(v[0],v[1],v[2],v[3],v[4],v[5])
  {}

  const dls_view
  dls::view() const
  {
    return dls_view{ {x0(), y0(), z0()}, {x1(), y1(), z1()} };
  }

  double dls::x0() const { return _x0; }
  double dls::y0() const { return _y0; }
  double dls::z0() const { return _z0; }
  double dls::x1() const { return _x1; }
  double dls::y1() const { return _y1; }
  double dls::z1() const { return _z1; }
  double dls::cx() const { return (_x1+_x0)/2.0; }
  double dls::cy() const { return (_y1+_y0)/2.0; }
  double dls::cz() const { return (_z1+_z0)/2.0; }
  double dls::dx() const { return _x1-_x0; }
  double dls::dy() const { return _y1-_y0; }
  double dls::dz() const { return _z1-_z0; }

  double dls::ex() const { return dx()/_l; }
  double dls::ey() const { return dy()/_l; }
  double dls::ez() const { return dz()/_l; }

  double dls::pa() const { return _pa; }
  double dls::radius() const { return _r; }
  double dls::length() const { return _l; }

  const segment<double>
  dls::vertices() const
  {
    return { vector3<double>{x0(), y0(), z0()},
             vector3<double>{x1(), y1(), z1()} };
  }

  const vector3<double>
  dls::unit_vector() const { return { ex(), ey(), ex() }; }

  double
  dls::dot(const dls& dls) const
  {
    return dx()*dls.dx()+dy()*dls.dy()+dz()*dls.dz();
  }
  double
  dls::dot(const baseline& bl) const
  {
    return dx()*bl.dx()+dy()*bl.dy()+dz()*bl.dz();
  }

  double
  dls::argument(const dls& dls) const
  {
    return std::acos(clamp(dot(dls)/length()/dls.length(),-1.0,1.0));
  }
  double
  dls::argument(const baseline& bl) const
  {
    return std::acos(clamp(dot(bl)/length()/bl.length(),-1.0,1.0));
  }

  void
  dls::dprint() const
  {
    printf("%8.3lf %8.3lf %8.3lf %8.3lf %8.3lf %8.3lf",
           _x0,_y0,_z0,_x1,_y1,_z1);
    printf("   # (r,l,t) = (%.2lf, %.2lf, %.2lf)\n",
           radius(), length(), pa()/M_PI*180.0);
  }

}
