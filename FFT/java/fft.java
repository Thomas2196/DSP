package com.company;

import com.company.Maths.Complex;



public class FFT {

    // compute the FFT of x[], assuming its length n is a power of 2
    public static Complex[] fft(Complex[] x) {
        int n = x.length;

        // base case
        if (n == 1) return new Complex[] { x[0] };

        // radix 2 Cooley-Tukey FFT
        if (n % 2 != 0) {
            throw new IllegalArgumentException("n is not a power of 2");
        }

        // compute FFT of even terms
        Complex[] even = new Complex[n/2];
        for (int k = 0; k < n/2; k++) {
            even[k] = x[2*k];
        }
        Complex[] evenFFT = fft(even);

        // compute FFT of odd terms
        Complex[] odd  = even;  // reuse the array (to avoid n log n space)
        for (int k = 0; k < n/2; k++) {
            odd[k] = x[2*k + 1];
        }
        Complex[] oddFFT = fft(odd);

        // combine
        Complex[] y = new Complex[n];
        for (int k = 0; k < n/2; k++) {
            double kth = -2 * k * Math.PI / n;
            Complex wk = new Complex(Math.cos(kth), Math.sin(kth));
            y[k]       = evenFFT[k].plus (wk.times(oddFFT[k]));
            y[k + n/2] = evenFFT[k].minus(wk.times(oddFFT[k]));
        }
        return y;
    }


    // compute the inverse FFT of x[], assuming its length n is a power of 2
    public static Complex[] ifft(Complex[] x) {
        int n = x.length;
        Complex[] y = new Complex[n];

        // take conjugate
        for (int i = 0; i < n; i++) {
            y[i] = x[i].conjugate();
        }

        // compute forward FFT
        y = fft(y);

        // take conjugate again
        for (int i = 0; i < n; i++) {
            y[i] = y[i].conjugate();
        }

        // divide by n
        for (int i = 0; i < n; i++) {
            y[i] = y[i].scale(1.0 / n);
        }

        return y;

    }

    // display an array of Complex numbers to standard output
    public static void show(Complex[] x, String title) {
        System.out.println(title);
        System.out.println("-------------------");
        for (Complex complex : x) {
            System.out.println(complex);
        }
        System.out.println();
    }




    public static void main(String[] args) {
        int n = 32;
        Complex[] x = new Complex[n];

        // original data
        double[] signal =
                { 2.28025, 1.32888, 0.39326, -0.49619, -1.31121, -2.02672, -2.62174,
                        -3.08015, -3.39124, -3.55077, -3.55763, -3.42069, -3.15151,
                        -2.76733, -2.28963, -1.74326, -1.15541, -0.55456, 0.03068,
                        0.57271, 1.04606, 1.42835, 1.7122, 1.85105, 1.86948, 1.75376,
                        1.50688, 1.13742, 0.65924, 0.09094, -0.54489, -1.22254,
                        -1.91419};


        for (int i = 0; i < n; i++) {
            x[i] = new Complex(signal[i], 0);
        }
        show(x, "x");

        // FFT of original data
        Complex[] y = fft(x);
        show(y, "y = fft(x)");


        // take inverse FFT
        Complex[] z = ifft(y);
        show(z, "z = ifft(y)");


    }

}
