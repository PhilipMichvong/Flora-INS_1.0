#include "pos_calc.hpp"

long double startCoordinates[2] = {52.256545, 20.886096};
long double lastAltitude = 0;
const double pi = 2 * acos(0.0);
const double equatorRadius = 6378137;  //[m]
const double meridianRadius = 6371008; //[m]

class TelemetricReading;

class TelemetricReading
{
private:
    long double altitude;
    long double thetaAngleHorizontal;
    long double velocity;

public:
    TelemetricReading(long double altitude, long double thetaAngleHorizontal, long double velocity)
    {
        this->altitude = altitude;
        this->thetaAngleHorizontal = thetaAngleHorizontal;
        this->velocity = velocity;
    }

    long double getAltitude()
    {
        return this->altitude;
    }

    long double getThetaAngleHorizontal()
    {
        return this->thetaAngleHorizontal;
    }

    long double getVelocity()
    {
        return this->velocity;
    }
};

long double **generateMatrixOfTranslation(long double xt, long double yt)
{
    long double **matrixOfTranslation;
    matrixOfTranslation = new long double *[4];
    for (int i = 0; i < 4; i++)
    {
        matrixOfTranslation[i] = new long double[4];
    }

    matrixOfTranslation[0][0] = 1.0;
    matrixOfTranslation[0][1] = 0.0;
    matrixOfTranslation[0][2] = 0.0;
    matrixOfTranslation[0][3] = xt;

    matrixOfTranslation[1][0] = 0.0;
    matrixOfTranslation[1][1] = 1.0;
    matrixOfTranslation[1][2] = 0.0;
    matrixOfTranslation[1][3] = yt;

    matrixOfTranslation[2][0] = 0.0;
    matrixOfTranslation[2][1] = 0.0;
    matrixOfTranslation[2][2] = 1.0;
    matrixOfTranslation[2][3] = 0.0;

    matrixOfTranslation[3][0] = 0.0;
    matrixOfTranslation[3][1] = 0.0;
    matrixOfTranslation[3][2] = 0.0;
    matrixOfTranslation[3][3] = 1.0;

    return matrixOfTranslation;
}

long double **generateRecentStepVector(long double recentLatitude, long double recentLongitude)
{
    long double **recentStepVector;
    recentStepVector = new long double *[4];
    for (int i = 0; i < 4; i++)
    {
        recentStepVector[i] = new long double[1];
    }

    recentStepVector[0][0] = recentLatitude;
    recentStepVector[1][0] = recentLongitude;
    recentStepVector[2][0] = 0.0;
    recentStepVector[3][0] = 1.0;

    return recentStepVector;
}

long double **calculateTranslatedVector(long double **matrixOfTranslation, long double **recentStepVector)
{
    long double **resultVector;
    resultVector = new long double *[4];
    for (int i = 0; i < 4; i++)
    {
        resultVector[i] = new long double[1];
    }

    long double tmp = 0;
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            tmp += (matrixOfTranslation[i][j] * recentStepVector[i][0]);
            std::cerr << "[" << i << "][" << j << "]: " << matrixOfTranslation[i][j] << " * " << recentStepVector[i][0] << " => " << tmp << std::endl;
        }
        resultVector[i][0] = tmp;
        tmp = 0;
    }
    return resultVector;
}

int calculateNextStepCoordinates(TelemetricReading *telemetricReadings, long double time)
{
    long double reachedDistance = 0;
    long double thetaAngleInDeg = telemetricReadings->getThetaAngleHorizontal();
    long double superelevation = lastAltitude - telemetricReadings->getAltitude();

    std::cerr << "Superelevation: " << superelevation << std::endl;

    if (superelevation == 0)
    {
        reachedDistance = telemetricReadings->getVelocity() * (time / 1000);
    }
    else
    {
        long double c = telemetricReadings->getVelocity() * (time / 1000);
        reachedDistance = sqrt(pow(2, c) - pow(2, superelevation));
    }

    std::cerr << "Reached Distance: " << reachedDistance << std::endl;
    if (isnan(reachedDistance))
    {
        return 1;
    }

    const long double latitudeDivider = ((2 * pi * meridianRadius) / 360) * startCoordinates[0];
    const long double longitudeDivider = ((2 * pi * equatorRadius) / 360) * ((90 - startCoordinates[0]) / 90) * startCoordinates[1];

    std::cerr << "LatDivider: " << latitudeDivider << std::endl;
    std::cerr << "LonDivider: " << longitudeDivider << std::endl;

    long double distance1 = reachedDistance / latitudeDivider;
    long double distance2 = (reachedDistance / longitudeDivider) * 0.72;

    std::cerr << "Distance 1: " << distance1 << std::endl;
    std::cerr << "Distance 2: " << distance2 << std::endl;

    long double thetaAngleInRad = (thetaAngleInDeg * pi) / 180;
    long double latitudeTranslation = cos(thetaAngleInRad) * distance1;
    long double longitudeTranslation = sin(thetaAngleInRad) * distance2;

    std::cerr << "LatTranslation: " << latitudeTranslation << std::endl;
    std::cerr << "LonTranslation: " << longitudeTranslation << std::endl
         << std::endl;

    long double **matrixOfTranslation = generateMatrixOfTranslation(latitudeTranslation, longitudeTranslation);
    long double **recentStepVector = generateRecentStepVector(startCoordinates[0], startCoordinates[1]);
    long double **resultVector = calculateTranslatedVector(matrixOfTranslation, recentStepVector);

    std::cerr << std::endl
         << "[" << resultVector[0][0] << ", " << resultVector[1][0] << ", " << resultVector[2][0] << ", " << resultVector[3][0] << "]" << std::endl
         << std::endl;

    std::cout << resultVector[0][0] << ",";
    std::cout << resultVector[1][0] << std::endl;

    return 0;
}

/*
    ARGS:
        1           2           3           4
        lat         lon         prev_alt    alt
        5           6           7
        vel         bear        time
*/
int main(int argc, char **argv)
{
    if (argc != 8)
    {
        std::cout << "Bad parameters!" << std::endl;
        return 1;
    }
    TelemetricReading *telemetricReading = new TelemetricReading(atof(argv[4]), atof(argv[6]), atof(argv[5]));
    startCoordinates[0] = atof(argv[1]);
    startCoordinates[1] = atof(argv[2]);
    lastAltitude = atof(argv[3]);
    long double time = atof(argv[7]);

    std::cout << std::setprecision(18);
    std::cerr << std::setprecision(18);

    return calculateNextStepCoordinates(telemetricReading, time);
}
