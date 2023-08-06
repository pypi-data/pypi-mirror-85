// Copyright (c) by respective owners including Yahoo!, Microsoft, and
// individual contributors. All rights reserved. Released under a BSD (revised)
// license as described in the file LICENSE.

#pragma once
#include "learner.h"
#include "options.h"
#include "cb.h"
#include "action_score.h"

namespace VW
{
namespace pmf_to_pdf
{
LEARNER::base_learner* setup(config::options_i& options, vw& all);
struct reduction
{
  void predict(example& ec);
  void learn(example& ec);

  ~reduction();
  std::vector<uint32_t> pdf_lim;
  uint32_t num_actions;
  uint32_t bandwidth;  // radius
  float min_value;
  float max_value;
  LEARNER::single_learner* _p_base;

private:
  void transform_prediction(example& ec);

  CB::label temp_lbl_cb;
  ACTION_SCORE::action_scores temp_pred_a_s;
};
}  // namespace pmf_to_pdf
}  // namespace VW
