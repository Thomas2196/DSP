#include <cmath>
#include <string>
#include <vector>

class TPTMultimodeOnePoleFilter {
private:
  std::string type;
  double sampleRate;
  double fc;
  double wf;
  double wc;
  double T;
  double wa;
  double g;
  double G;
  double z1;

public:
  TPTMultimodeOnePoleFilter(const std::string &type, double sampleRate,
                            double fc);

  double doFilterStage(double xn);

  double getStorageRegisterValue();

  double getSampleRate();
};