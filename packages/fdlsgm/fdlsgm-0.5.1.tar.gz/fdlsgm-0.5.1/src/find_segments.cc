/**
 * @file baseline.cc
 * @brief Base Line Class
 * @author Ryou Ohsawa
 * @year 2020
 */
#include "fdlsgm.h"


namespace fdlsgm {

  const std::vector<baseline_view>
  find_segments(const std::vector<dls>& pool,
                const size_t& size_limit,
                const parameter& param_insert,
                const parameter& param_update,
                const parameter& param_merge)
  {
    accumulator<360> ac;
    for (auto& dls: pool) ac.insert(dls, param_insert);
    ac.update(param_update);
    ac.merge(param_merge);
    ac.purify();
    std::vector<baseline_view> ret;
    const size_t n = ac.count_baseline();
    for (size_t i=0; i<n; i++) {
      const auto& b = ac[i];
      if (b.size()>=size_limit) ret.push_back(b.view());
    }
    return ret;
  }
  const std::vector<baseline_view>
  find_segments(const size_t& n_elements,
                const double* pool,
                const size_t& size_limit,
                const parameter& param_insert,
                const parameter& param_update,
                const parameter& param_merge)
  {
    accumulator<360> ac;
    for (size_t i=0; i<n_elements; i++) {
      const size_t& n = 6*i;
      ac.insert(dls(pool+n), param_insert);
    }
    ac.update(param_update);
    ac.merge(param_merge);
    ac.purify();
    std::vector<baseline_view> ret;
    const size_t n = ac.count_baseline();
    for (size_t i=0; i<n; i++) {
      const auto& b = ac[i];
      if (b.size()>=size_limit) ret.push_back(b.view());
    }
    return ret;
  }

}
