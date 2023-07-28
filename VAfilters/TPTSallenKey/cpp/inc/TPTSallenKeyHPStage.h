#include <cmath>
#include <vector>

class TPTSallenKeyHPStage {
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
  TPTSallenKeyHPStage(double sampleRate, double fc);

  double doFilterStage(double xn);

  double getStorageRegisterValue();

  double getSampleRate();
};
