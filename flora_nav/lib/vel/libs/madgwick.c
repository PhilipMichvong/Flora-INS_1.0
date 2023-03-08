// Math library required for ‘sqrt’
#include <math.h>
// System constants
#define deltat 0.001f                                     // sampling period in seconds (shown as 1 ms)
#define gyroMeasError 3.14159265358979f * (5.0f / 180.0f) // gyroscope measurement error in rad/s (shown as 5 deg/s)
#define beta sqrt(3.0f / 4.0f) * gyroMeasError            // compute beta
#define PI 2 * acos(0.0)

double * filterUpdate(double *gyro, double *acc, double *q)
{
    // Local system variables
    double norm;                                                           // vector norm
    double SEqDot_omega_1, SEqDot_omega_2, SEqDot_omega_3, SEqDot_omega_4; // quaternion derrivative from gyroscopes elements
    double f_1, f_2, f_3;                                                  // objective function elements
    double J_11or24, J_12or23, J_13or22, J_14or21, J_32, J_33;             // objective function Jacobian elements
    double SEqHatDot_1, SEqHatDot_2, SEqHatDot_3, SEqHatDot_4;             // estimated direction of the gyroscope error

    double SEq_1 = q[0];
    double SEq_2 = q[1];
    double SEq_3 = q[2];
    double SEq_4 = q[3];

    double a_x = acc[0];
    double a_y = acc[1];
    double a_z = acc[2];

    double w_x = gyro[0];
    double w_y = gyro[1];
    double w_z = gyro[2];

    // Axulirary variables to avoid reapeated calcualtions
    double halfSEq_1 = 0.5f * SEq_1;
    double halfSEq_2 = 0.5f * SEq_2;
    double halfSEq_3 = 0.5f * SEq_3;
    double halfSEq_4 = 0.5f * SEq_4;
    double twoSEq_1 = 2.0f * SEq_1;
    double twoSEq_2 = 2.0f * SEq_2;
    double twoSEq_3 = 2.0f * SEq_3;
    
    // Normalise the accelerometer measurement
    norm = sqrt(a_x * a_x + a_y * a_y + a_z * a_z);
    a_x /= norm;
    a_y /= norm;
    a_z /= norm;

    // Compute the objective function and Jacobian
    f_1 = twoSEq_2 * SEq_4 - twoSEq_1 * SEq_3 - a_x;
    f_2 = twoSEq_1 * SEq_2 + twoSEq_3 * SEq_4 - a_y;
    f_3 = 1.0f - twoSEq_2 * SEq_2 - twoSEq_3 * SEq_3 - a_z;
    J_11or24 = twoSEq_3; // J_11 negated in matrix multiplication
    J_12or23 = 2.0f * SEq_4;
    J_13or22 = twoSEq_1; // J_12 negated in matrix multiplication
    J_14or21 = twoSEq_2;
    J_32 = 2.0f * J_14or21; // negated in matrix multiplication
    J_33 = 2.0f * J_11or24; // negated in matrix multiplication

    // Compute the gradient (matrix multiplication)
    SEqHatDot_1 = J_14or21 * f_2 - J_11or24 * f_1;
    SEqHatDot_2 = J_12or23 * f_1 + J_13or22 * f_2 - J_32 * f_3;
    SEqHatDot_3 = J_12or23 * f_2 - J_33 * f_3 - J_13or22 * f_1;
    SEqHatDot_4 = J_14or21 * f_1 + J_11or24 * f_2;

    // Normalise the gradient
    norm = sqrt(SEqHatDot_1 * SEqHatDot_1 + SEqHatDot_2 * SEqHatDot_2 + SEqHatDot_3 * SEqHatDot_3 + SEqHatDot_4 * SEqHatDot_4);
    SEqHatDot_1 /= norm;
    SEqHatDot_2 /= norm;
    SEqHatDot_3 /= norm;
    SEqHatDot_4 /= norm;

    // Compute the quaternion derrivative measured by gyroscopes
    SEqDot_omega_1 = -halfSEq_2 * w_x - halfSEq_3 * w_y - halfSEq_4 * w_z;
    SEqDot_omega_2 = halfSEq_1 * w_x + halfSEq_3 * w_z - halfSEq_4 * w_y;
    SEqDot_omega_3 = halfSEq_1 * w_y - halfSEq_2 * w_z + halfSEq_4 * w_x;
    SEqDot_omega_4 = halfSEq_1 * w_z + halfSEq_2 * w_y - halfSEq_3 * w_x;

    // Compute then integrate the estimated quaternion derrivative
    SEq_1 += (SEqDot_omega_1 - (beta * SEqHatDot_1)) * deltat;
    SEq_2 += (SEqDot_omega_2 - (beta * SEqHatDot_2)) * deltat;
    SEq_3 += (SEqDot_omega_3 - (beta * SEqHatDot_3)) * deltat;
    SEq_4 += (SEqDot_omega_4 - (beta * SEqHatDot_4)) * deltat;

    // Normalise quaternion
    norm = sqrt(SEq_1 * SEq_1 + SEq_2 * SEq_2 + SEq_3 * SEq_3 + SEq_4 * SEq_4);
    SEq_1 /= norm;
    SEq_2 /= norm;
    SEq_3 /= norm;
    SEq_4 /= norm;

    q[0] = SEq_1;
    q[1] = SEq_2;
    q[2] = SEq_3;
    q[3] = SEq_4;

    // Pitch and roll calculation
    double R11 = 2. *  q[0] * q[0] - 1 + 2. * q[1] * q[1];
    double R21 = 2. * (q[1] * q[2] - q[0] * q[3]);
    double R31 = 2. * (q[1] * q[3] + q[0] * q[2]);
    double R32 = 2. * (q[2] * q[3] - q[0] * q[1]);
    double R33 = 2. * q[0] * q[0] - 1 + 2. * q[3] * q[3];

    double theta = -atan(R31 / sqrt(1 - R31 * R31));
    double phi = atan2(R32, R33);

    double *res = new double[2];
    res[0] = (theta * 180) / PI;    // Pitch
    res[1] = (phi * 180) / PI;      // Roll
    return res;
}
