/**
 * @file baseline.cc
 * @brief Base Line Class
 * @author Ryou Ohsawa
 * @year 2020
 */
#include "fdlsgm.h"


namespace fdlsgm {

  double
  wrap_angle(double angle)
  {
    if (angle > M_PI || angle < -M_PI)
      angle = angle-std::floor(angle/(M_PI*2.0))*(M_PI*2.0);
    return angle;
  }

  double
  angle_separation(const double d1, const double d2)
  {
    return std::abs(fdlsgm::wrap_angle(d1-d2));
  }

  baseline::baseline():
    _x0(0.0),_y0(0.0),_z0(0.0),_x1(0.0),_y1(0.0),_z1(0.0),
    _r(0.0),_l(0.0),_pa(0.0),_ncx(0.0),_ncy(0.0),_ncz(0.0),_f(zeros4x4)
  {}
  baseline::baseline(const index_t& n, const dls& dls):
    _x0(dls.x0()),_y0(dls.y0()),_z0(dls.z0()),
    _x1(dls.x1()),_y1(dls.y1()),_z1(dls.z1()),
    _r(dls.radius()),_l(dls.length()),_pa(dls.pa()),
    _ncx(dls.cx()),_ncy(dls.cy()),_ncz(dls.cz()),
    _f(zeros4x4)
  {
    _elements.insert(n);
  }
  baseline::baseline(const baseline& other):
    _x0(other.x0()),_y0(other.y0()),_z0(other.z0()),
    _x1(other.x1()),_y1(other.y1()),_z1(other.z1()),
    _r(other.radius()),_l(other.length()),_pa(other.pa()),
    _ncx(other.cx()),_ncy(other.cy()),_ncz(other.cz()),_f(other._f)
  {
    for (auto& e: other._elements) _elements.insert(e);
    _ncx *= _elements.size();
    _ncy *= _elements.size();
    _ncz *= _elements.size();
  }

  const baseline_view
  baseline::view() const
  {
    std::vector<index_t> v;
    for (auto& e: _elements) { v.push_back(e); }
    return baseline_view{
      {x0(), y0(), z0()}, {x1(), y1(), z1()}, size(), v };
  }

  bool
  baseline::append(const index_t& n, const dls& dls)
  {
    if (_elements.find(n)!=_elements.end()) {
      return false;
    } else {
      _elements.insert(n);
      _ncx += dls.cx(); _ncy += dls.cy(); _ncz += dls.cz();

      if (root_position(dls.vertices()[0]) < 0.0) {
        _x0 = dls.x0(); _y0 = dls.y0(); _z0 = dls.z0();
        update_parameters();
      }
      if (root_position(dls.vertices()[1]) > 1.0) {
        _x1 = dls.x1(); _y1 = dls.y1(); _z1 = dls.z1();
        update_parameters();
      }

      update_matrix(dls);
      update_direction();
      update_parameters();
      return true;
    }
  }

  bool
  baseline::drop(const index_t& n)
  {
    return _elements.erase(n) > 0;
  }

  double baseline::x0() const { return _x0; }
  double baseline::y0() const { return _y0; }
  double baseline::z0() const { return _z0; }
  double baseline::x1() const { return _x1; }
  double baseline::y1() const { return _y1; }
  double baseline::z1() const { return _z1; }
  double baseline::cx() const { return _ncx/size(); }
  double baseline::cy() const { return _ncy/size(); }
  double baseline::cz() const { return _ncz/size(); }
  double baseline::dx() const { return _x1-_x0; }
  double baseline::dy() const { return _y1-_y0; }
  double baseline::dz() const { return _z1-_z0; }

  double baseline::ex() const { return dx()/_l; }
  double baseline::ey() const { return dy()/_l; }
  double baseline::ez() const { return dz()/_l; }

  const segment<double>
  baseline::vertices() const
  {
    return { vector3<double>{x0(), y0(), z0()},
             vector3<double>{x1(), y1(), z1()} };
  }

  const vector3<double>
  baseline::unit_vector() const { return { ex(), ey(), ex() }; }

  double baseline::pa() const { return _pa; }
  double baseline::radius() const { return _r; }
  double baseline::length() const { return _l; }

  size_t baseline::size() const { return _elements.size(); }

  std::list<index_t>
  baseline::elements() const
  {
    std::list<index_t> elements;
    for (auto& e: _elements) elements.push_back(e);
    return elements;
  }

  double
  baseline::dot(const dls& dls) const
  {
    return dx()*dls.dx()+dy()*dls.dy()+dz()*dls.dz();
  }
  double
  baseline::dot(const baseline& bl) const
  {
    return dx()*bl.dx()+dy()*bl.dy()+dz()*bl.dz();
  }

  double
  baseline::argument(const dls& dls) const
  {
    return std::acos(clamp(dot(dls)/length()/dls.length(),-1.0,1.0));
  }
  double
  baseline::argument(const baseline& bl) const
  {
    return std::acos(clamp(dot(bl)/length()/bl.length(),-1.0,1.0));
  }


  double
  baseline::point_distance_squared(const vector3<double>& v) const
  {
    const double& Cxx =
      std::pow((v[0]-x0()),2.0)*(1.0-ex()*ex());
    const double& Cyy =
      std::pow((v[1]-y0()),2.0)*(1.0-ey()*ey());
    const double& Czz =
      std::pow((v[2]-z0()),2.0)*(1.0-ez()*ez());
    const double& Cxy =
      -2.0*(v[0]-x0())*(v[1]-y0())*ex()*ey();
    const double& Cyz =
      -2.0*(v[1]-y0())*(v[2]-z0())*ey()*ez();
    const double& Czx =
      -2.0*(v[2]-z0())*(v[0]-x0())*ez()*ex();
    return Cxx+Cyy+Czz+Cxy+Cyz+Czx;
  }
  double
  baseline::point_distance(const vector3<double>& v) const
  {
    return std::sqrt(point_distance_squared(v));
  }

  double
  baseline::lateral_distance_squared(const dls& dls) const
  {
    const double& Cxx =
      ( std::pow(dls.x1()-x0(),3.0) - std::pow(dls.x0()-x0(),3.0) )
      *(1.0-ex()*ex())/(3.0*dls.dx());
    const double& Cyy =
      ( std::pow(dls.y1()-y0(),3.0) - std::pow(dls.y0()-y0(),3.0) )
      *(1.0-ey()*ey())/(3.0*dls.dy());
    const double& Czz =
      ( std::pow(dls.z1()-z0(),3.0) - std::pow(dls.z0()-z0(),3.0) )
      *(1.0-ez()*ez())/(3.0*dls.dz());
    const double& Cxy =
      - ( 2.0*dls.dx()*dls.dy()
          + 3.0*(dls.dy()*(dls.x0()-x0())+dls.dx()*(dls.y0()-y0()))
          + 6.0*(dls.x0()-x0())*(dls.y0()-y0()) )*ex()*ey()/3.0;
    const double& Cyz =
      - ( 2.0*dls.dy()*dls.dz()
          + 3.0*(dls.dz()*(dls.y0()-y0())+dls.dy()*(dls.z0()-z0()))
          + 6.0*(dls.y0()-y0())*(dls.z0()-z0()) )*ey()*ez()/3.0;
    const double& Czx =
      - ( 2.0*dls.dz()*dls.dx()
          + 3.0*(dls.dx()*(dls.z0()-z0())+dls.dz()*(dls.x0()-x0()))
          + 6.0*(dls.z0()-z0())*(dls.x0()-x0()) )*ez()*ex()/3.0;
    return std::max(0.0,Cxx+Cyy+Czz+Cxy+Cyz+Czx);
  }
  double
  baseline::lateral_distance(const dls& dls) const
  {
    return std::sqrt(lateral_distance_squared(dls));
  }
  double
  baseline::lateral_distance_squared(const baseline& bl) const
  {
    const double& Cxx =
      ( std::pow(bl.x1()-x0(),3.0) - std::pow(bl.x0()-x0(),3.0) )
      *(1.0-ex()*ex())/(3.0*bl.dx());
    const double& Cyy =
      ( std::pow(bl.y1()-y0(),3.0) - std::pow(bl.y0()-y0(),3.0) )
      *(1.0-ey()*ey())/(3.0*bl.dy());
    const double& Czz =
      ( std::pow(bl.z1()-z0(),3.0) - std::pow(bl.z0()-z0(),3.0) )
      *(1.0-ez()*ez())/(3.0*bl.dz());
    const double& Cxy =
      - ( 2.0*bl.dx()*bl.dy()
          + 3.0*(bl.dy()*(bl.x0()-x0())+bl.dx()*(bl.y0()-y0()))
          + 6.0*(bl.x0()-x0())*(bl.y0()-y0()) )*ex()*ey()/3.0;
    const double& Cyz =
      - ( 2.0*bl.dy()*bl.dz()
          + 3.0*(bl.dz()*(bl.y0()-y0())+bl.dy()*(bl.z0()-z0()))
          + 6.0*(bl.y0()-y0())*(bl.z0()-z0()) )*ey()*ez()/3.0;
    const double& Czx =
      - ( 2.0*bl.dz()*bl.dx()
          + 3.0*(bl.dx()*(bl.z0()-z0())+bl.dz()*(bl.x0()-x0()))
          + 6.0*(bl.z0()-z0())*(bl.x0()-x0()) )*ez()*ex()/3.0;
    return std::max(0.0,Cxx+Cyy+Czz+Cxy+Cyz+Czx);
  }
  double
  baseline::lateral_distance(const baseline& bl) const
  {
    return std::sqrt(lateral_distance_squared(bl));
  }

  double
  baseline::gap_length(const dls& dls) const
  {
    const auto& v = dls.vertices();
    const auto& v0 = v[0];
    const auto& v1 = v[1];
    double t0 = root_position(v0), t1 = root_position(v1);
    return (t1<0.0)?-t1:(t0>1.0)?t0-1.0:0.0;
  }
  double
  baseline::gap_length(const baseline& bl) const
  {
    const auto& v = bl.vertices();
    const auto& v0 = v[0];
    const auto& v1 = v[1];
    double t0 = root_position(v0), t1 = root_position(v1);
    return (t1<0.0)?-t1:(t0>1.0)?t0-1.0:0.0;
  }

  double
  baseline::overlap_length(const dls& dls) const
  {
    const auto& v = dls.vertices();
    const auto& v0 = v[0];
    const auto& v1 = v[1];
    double t0 = root_position(v0), t1 = root_position(v1);
    if (t1<t0) std::swap(t0,t1);
    if (t1< 0.0 || t0> 1.0) return 0.0;
    if (t0< 0.0 && t1> 1.0) return 1.0;
    if (t0< 0.0 && t1>=0.0) return t1-0.0;
    if (t0>=0.0 && t1> 1.0) return 1.0-t0;
    if (t0> 0.0 && t1< 1.0) return t1-t0;
    return 0.0;
  }
  double
  baseline::overlap_length(const baseline& bl) const
  {
    const auto& v = bl.vertices();
    const auto& v0 = v[0];
    const auto& v1 = v[1];
    double t0 = root_position(v0), t1 = root_position(v1);
    if (t1<t0) std::swap(t0,t1);
    if (t1< 0.0 || t0> 1.0) return 0.0;
    if (t0< 0.0 && t1> 1.0) return 1.0;
    if (t0< 0.0 && t1>=0.0) return t1-0.0;
    if (t0>=0.0 && t1> 1.0) return 1.0-t0;
    if (t0> 0.0 && t1< 1.0) return t1-t0;
    return 0.0;
  }

  void
  baseline::dprint() const
  {
    printf("# baseline: [%08lx]\n", (size_t)this);
    printf("#\tVertex 0      : (%lf %lf %lf)\n", x0(),y0(),z0());
    printf("#\tVertex 1      : (%lf %lf %lf)\n", x1(),y1(),z1());
    printf("#\tCenter        : (%lf %lf %lf)\n", cx(),cy(),cz());
    printf("#\tVector        : (%lf %lf %lf)\n", ex(),ey(),ez());
    printf("#\tPosition Angle: %lf\n", pa()*180.0/M_PI);
    printf("#\tLength        : %lf\n", length());
    printf("#\tRadius        : %lf\n", radius());
    printf("#\tSize          : %ld\n", size());
    printf("#\tMembers       : [ ");
    for (auto& n: _elements) printf("%ld ", n);  printf("]\n");
    printf("%8.3lf %8.3lf %8.3lf %8.3lf %8.3lf %8.3lf",
           x0(), y0(), z0(), x1(), y1(), z1());
    printf("   # (r,l,t) = (%.2lf, %.2lf, %.2lf)\n",
           radius(), length(), pa()/M_PI*180.0);
  }


  double
  baseline::root_position(const vector3<double>& v) const
  {
    return ((v[0]-x0())*ex()+(v[1]-y0())*ey()+(v[2]-z0())*ez())/length();
  }


  void
  baseline::update_matrix(const dls& dls)
  {
    _f[0][0] += (dls.length()/2.0)*(dls.x0()*dls.x0()+dls.x1()*dls.x1());
    _f[1][1] += (dls.length()/2.0)*(dls.y0()*dls.y0()+dls.y1()*dls.y1());
    _f[2][2] += (dls.length()/2.0)*(dls.z0()*dls.z0()+dls.z1()*dls.z1());
    _f[3][3] += (dls.length());
    _f[0][1] += (dls.length()/2.0)*(dls.x0()*dls.y0()+dls.x1()*dls.y1());
    _f[1][0] += (dls.length()/2.0)*(dls.y0()*dls.x0()+dls.y1()*dls.x1());
    _f[0][2] += (dls.length()/2.0)*(dls.x0()*dls.z0()+dls.x1()*dls.z1());
    _f[2][0] += (dls.length()/2.0)*(dls.z0()*dls.x0()+dls.z1()*dls.x1());
    _f[0][3] += (dls.length()/2.0)*(dls.x0()*(-1.0)+dls.x1()*(-1.0));
    _f[3][0] += (dls.length()/2.0)*((-1.0)*dls.x0()+(-1.0)*dls.x1());
    _f[1][2] += (dls.length()/2.0)*(dls.y0()*dls.z0()+dls.y1()*dls.z1());
    _f[2][1] += (dls.length()/2.0)*(dls.z0()*dls.y0()+dls.z1()*dls.y1());
    _f[1][3] += (dls.length()/2.0)*(dls.y0()*(-1.0)+dls.y1()*(-1.0));
    _f[3][1] += (dls.length()/2.0)*((-1.0)*dls.y0()+(-1.0)*dls.y1());
    _f[2][3] += (dls.length()/2.0)*(dls.z0()*(-1.0)+dls.z1()*(-1.0));
    _f[3][2] += (dls.length()/2.0)*((-1.0)*dls.z0()+(-1.0)*dls.z1());
  }

  void
  baseline::update_direction()
  {
    auto& eigen = eigenvector_jacobi_4x4(_f);
    auto& n0 = eigen[0];
    auto& n1 = eigen[1];
    const auto& d = normalize_vector(outer_product(n0, n1));

    const double& t0 =
      ((x0()-cx())*d[0]+(y0()-cy())*d[1]+(z0()-cz())*d[2]);
    const double& t1 =
      ((x1()-cx())*d[0]+(y1()-cy())*d[1]+(z1()-cz())*d[2]);
    const vector3<double>& v0 =
      { cx()+t0*d[0], cy()+t0*d[1], cz()+t0*d[2] };
    const vector3<double>& v1 =
      { cx()+t1*d[0], cy()+t1*d[1], cz()+t1*d[2] };

    _x0 = v0[0]; _y0 = v0[1]; _z0 = v0[2];
    _x1 = v1[0]; _y1 = v1[1]; _z1 = v1[2];
  }

  void
  baseline::update_parameters()
  {
    _l  = std::sqrt(dx()*dx()+dy()*dy()+dz()*dz());
    _r  = std::sqrt(dx()*dx()+dy()*dy());
    _pa = std::atan2(-dx(), dy());
  }

  const baseline
  merge_baseline(const baseline& b0, const baseline& b1)
  {
    baseline merged;
    merged._x0 = (b0.x0()+b1.x0())/2.0; merged._x1 = (b0.x1()+b1.x1())/2.0;
    merged._y0 = (b0.y0()+b1.y0())/2.0; merged._y1 = (b0.y1()+b1.y1())/2.0;
    merged._z0 = (b0.z0()+b1.z0())/2.0; merged._z1 = (b0.z1()+b1.z1())/2.0;
    for (size_t i=0; i<4; i++)
      for (size_t j=0; j<4; j++)
        merged._f[i][j] = b0._f[i][j] + b1._f[i][j];
    for (auto& e: b0._elements) merged._elements.insert(e);
    for (auto& e: b1._elements) merged._elements.insert(e);
    merged._ncx = b0._ncx + b1._ncx;
    merged._ncy = b0._ncy + b1._ncy;
    merged._ncz = b0._ncz + b1._ncz;
    merged.update_parameters();
    return merged;
  }
}
