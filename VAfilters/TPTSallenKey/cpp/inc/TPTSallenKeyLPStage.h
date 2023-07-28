#include <cmath>
#include <vector>

class TPTSallenKeyLPStage {
private:
  double sampleRate;
  double fc;
  double wc;
  double T;
  double wa;
  double g;
  double G;
  double z1;

public:
  TPTSallenKeyLPStage(double sampleRate, double fc);

  double doFilterStage(double xn);

  double getStorageRegisterValue();

  double getSampleRate();
};