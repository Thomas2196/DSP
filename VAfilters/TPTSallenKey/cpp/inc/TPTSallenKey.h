#include <string>
#include <iterator>
#include <vector>
#include <iostream>
#include <android/log.h>
#include <utility>

#include "TPTMultimodeOnePoleFilter.h"
#include "TPTSallenKeyHPStage.h"
#include "TPTSallenKeyLPStage.h"

std::vector<double> SallenKey(const std::vector<double> &signal,
                              const std::string &filterType, int order,
                              double fc, double k, double sampleRate);

class TPTSallenKey {
private:
  std::string filterType;
  double fc;
  double k;
  double sampleRate;
  TPTMultimodeOnePoleFilter HPF1;
  TPTMultimodeOnePoleFilter LPF1;
  TPTMultimodeOnePoleFilter HPF3;
  TPTMultimodeOnePoleFilter LPF2;

public:
  TPTSallenKey(std::string filterType, double fc, double k,
               double sampleRate);

  double doTPTSallenKey(double xn);
};