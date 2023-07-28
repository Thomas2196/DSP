
#include "../inc/TPTSallenKey.h"

std::vector<double> SallenKey(const std::vector<double> &signal,
                              const std::string &filterType, int order,
                              double fc, double k, double sampleRate) {
  std::vector<double> output;
  int N = signal.size();
  output.reserve(N);
  order = order / 2;
//  __android_log_print(ANDROID_LOG_INFO, "TRACKERS", "FILTRE : %c",);
//    __android_log_print(ANDROID_LOG_INFO, "TRACKERS", "Filter : %d", fc);

  TPTSallenKey TPTSallenKeyfilter(filterType, fc, k, sampleRate);
  for (int n = 0; n < N; n++) {
    output.push_back(TPTSallenKeyfilter.doTPTSallenKey(signal[n]));
  }

  if (order > 1) {
    for (int o = 0; o < order - 1; o++) {
      TPTSallenKeyfilter = TPTSallenKey(filterType, fc, k, sampleRate);
      for (int n = 0; n < N; n++) {
        output[n] = TPTSallenKeyfilter.doTPTSallenKey(output[n]);
      }
    }
  }

  return output;
}

TPTSallenKey::TPTSallenKey(std::string filterType, double fc, double k,
                           double sampleRate)
    : filterType(std::move(filterType)), fc(fc), k(k), sampleRate(sampleRate),
      HPF1("HP", sampleRate, fc), LPF1("LP", sampleRate, fc),
      HPF3("HP", sampleRate, fc), LPF2("LP", sampleRate, fc) {

  // if (filterType == "HP") {
  //   // Initialize HPF1, LPF1, HPF3
  // } else if (filterType == "LP") {
  //   // Initialize LPF1, LPF2, HPF1
  // }
}

double TPTSallenKey::doTPTSallenKey(double xn) {
  // Cutoff pre-warping
  double wc = 2 * M_PI * fc;
  double T = 1 / sampleRate;
  double wa = (2 / T) * std::tan(wc * T / 2);

  double g = wa * (T / 2);  // Instantaneous gain
  double G = g / (1.0 + g); // Feedforward coeff

  if (filterType == "HP") {
//    __android_log_print(ANDROID_LOG_INFO, "TRACKERS", "Filter  : HP %d", fc);

    double s1 = HPF1.getStorageRegisterValue();
    double s2 = LPF1.getStorageRegisterValue();
    double s3 = HPF3.getStorageRegisterValue();

    double beta_3 = -G / (1.0 + g);
    double beta_2 = 1.0 / (1.0 + g);

    double G35 = 1.0 / (1.0 - k * G + k * G * G);

    double y1 = HPF1.doFilterStage(xn);

    double S35H = s3 * beta_3 + s2 * beta_2;

    double u = G35 * (y1 + S35H);

    double y = k * u;

    LPF1.doFilterStage(HPF3.doFilterStage(y));

    if (k > 0)
      y *= 1 / k;

    return y;

  } else if (filterType == "LP") {
//        __android_log_print(ANDROID_LOG_INFO, "TRACKERS", "Filter  : LP");

    double s1 = LPF1.getStorageRegisterValue();
    double s2 = LPF2.getStorageRegisterValue();
    double s3 = HPF1.getStorageRegisterValue();

    double beta_2 = (k - k * G) / (1 + g);
    double beta_3 = -1.0 / (1.0 + g);

    double alpha = 1.0 / (1.0 - k * G + k * G * G);

    double y1 = LPF1.doFilterStage(xn);
    double S35 = s3 * beta_3 + s2 * beta_2; // Feedback value

    double u = alpha * (y1 + S35);

    double y = k * LPF2.doFilterStage(u);

    HPF1.doFilterStage(y);

    if (k > 0)
      y *= 1 / k;

    return y;
  }

  return 0.0;
}