#include <stdlib.h>
#include <math.h>

#include "dataSim.h"

void wave_gen(data_obj* d, float* data) {
/* Generate a superposition of up to 10 sine waves using floats. This is 
   meant for generating data for FFT. */

	double time, temp;

	for(int n=0; n<d->num_samples; n++) {
		time = (double)n / (double)d->sample_rate;	// sample / (samples/sec)
		temp = 0.0;

		for(int i=0; i<d->num_frequencies; i++) {
			temp += sin(2.0*M_PI*d->frequency[i]*time);
		}

		if(d->num_frequencies > 1) {
			// no real reason to normalize here, but it could come in handy
			normalize(&temp, d->num_frequencies);
		}

		data[n] = (float)temp;
	}
}

void normalize(double* value, int num_frequencies) {
/* Normalize waveforms composed of multiple sine waves to ensure wave
   amplitudes aren't out of range when writing to .wav file. */
	
	double max = (double)num_frequencies;
	double min = (double)(-1.0 *num_frequencies);
	double range = max - min;

	*value = (*value - min) / range;
}


