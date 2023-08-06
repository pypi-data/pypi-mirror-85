// Copyright (c) by respective owners including Yahoo!, Microsoft, and
// individual contributors. All rights reserved. Released under a BSD (revised)
// license as described in the file LICENSE.

#include "kskip_ngram_transformer.h"

#include <memory>

void add_grams(
    size_t ngram, size_t skip_gram, features& fs, size_t initial_length, std::vector<size_t>& gram_mask, size_t skips)
{
  if (ngram == 0 && gram_mask.back() < initial_length)
  {
    size_t last = initial_length - gram_mask.back();
    for (size_t i = 0; i < last; i++)
    {
      uint64_t new_index = fs.indicies[i];
      for (size_t n = 1; n < gram_mask.size(); n++)
      { new_index = new_index * quadratic_constant + fs.indicies[i + gram_mask[n]]; }

      fs.push_back(1., new_index);
      if (!fs.space_names.empty())
      {
        std::string feature_name(fs.space_names[i].get()->second);
        for (size_t n = 1; n < gram_mask.size(); n++)
        {
          feature_name += std::string("^");
          feature_name += std::string(fs.space_names[i + gram_mask[n]].get()->second);
        }
        fs.space_names.push_back(std::make_shared<audit_strings>(fs.space_names[i].get()->first, feature_name));
      }
    }
  }
  if (ngram > 0)
  {
    gram_mask.push_back(gram_mask.back() + 1 + skips);
    add_grams(ngram - 1, skip_gram, fs, initial_length, gram_mask, 0);
    gram_mask.pop_back();
  }
  if (skip_gram > 0 && ngram > 0) { add_grams(ngram, skip_gram - 1, fs, initial_length, gram_mask, skips + 1); }
}

void compile_gram(const std::vector<std::string>& grams, std::array<uint32_t, NUM_NAMESPACES>& dest,
    const std::string& descriptor, bool quiet)
{
  for (const auto& gram : grams)
  {
    if (isdigit(gram[0]) != 0)
    {
      int n = atoi(gram.c_str());
      if (!quiet) { std::cerr << "Generating " << n << "-" << descriptor << " for all namespaces." << std::endl; }
      for (size_t j = 0; j < NUM_NAMESPACES; j++) { dest[j] = n; }
    }
    else if (gram.size() == 1)
    {
      std::cout << "You must specify the namespace index before the n" << std::endl;
    }
    else
    {
      int n = atoi(gram.c_str() + 1);
      dest[(uint32_t)(unsigned char)*gram.c_str()] = n;
      if (!quiet)
      { std::cerr << "Generating " << n << "-" << descriptor << " for " << gram[0] << " namespaces." << std::endl; }
    }
  }
}

void VW::kskip_ngram_transformer::generate_grams(example* ex)
{
  for (namespace_index index : ex->indices)
  {
    size_t length = ex->feature_space[index].size();
    for (size_t n = 1; n < ngram_definition[index]; n++)
    {
      gram_mask.clear();
      gram_mask.push_back(0);
      add_grams(n, skip_definition[index], ex->feature_space[index], length, gram_mask, 0);
    }
  }
}

VW::kskip_ngram_transformer VW::kskip_ngram_transformer::build(
    const std::vector<std::string>& grams, const std::vector<std::string>& skips, bool quiet)
{
  kskip_ngram_transformer transformer(grams, skips);

  compile_gram(grams, transformer.ngram_definition, "grams", quiet);
  compile_gram(skips, transformer.skip_definition, "skips", quiet);
  return transformer;
}

VW::kskip_ngram_transformer::kskip_ngram_transformer(std::vector<std::string> grams, std::vector<std::string> skips)
    : initial_ngram_definitions(std::move(grams)), initial_skip_definitions(std::move(skips))
{
  ngram_definition.fill(0);
  skip_definition.fill(0);
}
