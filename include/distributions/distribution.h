#ifndef DISTRIBUTION_H
#define DISTRIBUTION_H

#include <map>
#include <vector>
#include <string>
#include <stdexcept>
#include <iostream>

const int _defaultSeed = 1256955321;

enum truncation {MULTIPLICATIVE=1, SUM=2};

class distribution;

class DistributionContainer;

class BasicDistribution
{
public:
   BasicDistribution();
   virtual ~BasicDistribution();
   double  getVariable(const std::string variable_name);  ///< getVariable from mapping
   std::vector<double>  getVariableVector(const std::string variable_name);
   void updateVariable(const std::string & variable_name, double & new_value);    ///< update variable into the mapping

   virtual double getRandom(double x);  //Same as inverseCdf, except it can be forced.

   virtual double  Pdf(double x) = 0; ///< Pdf function at coordinate x
   virtual double  Cdf(double x) = 0; ///< Cdf function at coordinate x
   virtual double  InverseCdf(double x) = 0; ///< x

   virtual double untrPdf(double x) = 0;
   virtual double untrCdf(double x) = 0;
   virtual double untrCdfComplement(double x)  = 0;
   virtual double untrInverseCdf(double x) = 0;
   virtual double untrMean() = 0;
   virtual double untrStdDev() = 0;
   virtual double untrMedian() = 0;
   virtual double untrMode() = 0;
   virtual double untrHazard(double x) = 0;

   int returnDimensionality(){return 1;}

   std::string & getType(); ///< Get distribution type
   unsigned int getSeed(); ///< Get seed
   std::vector<std::string> getVariableNames();

protected:
  enum EForceRandom {NO_FORCING, FORCED_VALUE, FORCED_PROBABILITY};

  virtual EForceRandom forcingMethod();
  virtual double forcedConstant();
  virtual void setForcingMethod(EForceRandom forcing_method);
  virtual void setForcedConstant(double forced_constant);

  virtual double windowProcessing(double rng);

  EForceRandom _forcing_method;
  double _forced_constant;

  bool hasParameter(std::string);
  std::string _type;                              ///< Distribution type
  std::map <std::string,double> _dist_parameters;  ///< Distribution parameters
  std::map <std::string,std::vector<double> > _dist_vector_parameters;
  unsigned int _seed;                             ///< seed

  bool _checkStatus;
};



#endif /* DISTRIBUTION_H */
