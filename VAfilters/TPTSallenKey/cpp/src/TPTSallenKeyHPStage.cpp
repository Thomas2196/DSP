#include "../inc/TPTSallenKeyHPStage.h"

TPTSallenKeyHPStage::TPTSallenKeyHPStage(double sampleRate, double fc) {
  this->sampleRate = sampleRate;
  this->fc = fc;

  wc = 2 * M_PI * fc;
  T = 1 / sampleRate;
  wa = (2 / T) * std::tan(wc * T / 2);

  g = wa * T / 2;
  G = 1 / (1 + g);

  z1 = 0;
}

double TPTSallenKeyHPStage::doFilterStage(double xn) {
  double v = (xn - z1);
  double y = v * G;
  z1 = z1 + 2 * y * g;
  return y;
}

double TPTSallenKeyHPStage::getStorageRegisterValue() { return z1; }

double TPTSallenKeyHPStage::getSampleRate() { return sampleRate; }