#include "../inc/TPTMultimodeOnePoleFilter.h"

TPTMultimodeOnePoleFilter::TPTMultimodeOnePoleFilter(const std::string &type,
                                                     double sampleRate,
                                                     double fc) {
  this->type = type;
  this->sampleRate = sampleRate;
  this->fc = fc;
  wf = std::sqrt(std::pow(2, 1.0 / 8) - 1);

  wc = 2 * M_PI * fc;
  T = 1 / sampleRate;
  wa = (2 / T) * std::tan(wc * T / 2);

  g = wa * T / 2;
  G = g / (1 + g);

  z1 = 0;
}

double TPTMultimodeOnePoleFilter::doFilterStage(double xn) {
  double v = (xn - z1) * G;
  double lpf = v + z1;
  z1 = v + lpf;
  double hpf = xn - lpf;

  if (type == "LP") {
    return lpf;
  } else if (type == "HP") {
    return hpf;
  } else {
    return -1;
  }
}

double TPTMultimodeOnePoleFilter::getStorageRegisterValue() { return z1; }

double TPTMultimodeOnePoleFilter::getSampleRate() { return sampleRate; }