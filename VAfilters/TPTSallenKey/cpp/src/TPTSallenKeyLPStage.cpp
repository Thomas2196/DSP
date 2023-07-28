#include "../inc/TPTSallenKeyLPStage.h"

TPTSallenKeyLPStage::TPTSallenKeyLPStage(double sampleRate, double fc) {
  this->sampleRate = sampleRate;
  this->fc = fc;

  wc = 2 * M_PI * fc;
  T = 1 / sampleRate;
  wa = (2 / T) * std::tan(wc * T / 2);

  g = wa * T / 2;
  G = g / (1 + g);

  z1 = 0;
}

double TPTSallenKeyLPStage::doFilterStage(double xn) {
  double v = (xn - z1) * G;
  double y = v + z1;
  z1 = y + v;
  return y;
}

double TPTSallenKeyLPStage::getStorageRegisterValue() { return z1; }

double TPTSallenKeyLPStage::getSampleRate() { return sampleRate; }