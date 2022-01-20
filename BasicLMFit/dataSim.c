#include <stdlib.h>
#include <stdio.h>

#include <math.h>

#include "dataSim.h"

void wave_gen(data_obj* d, float* data) {
/* Generate a superposition of up to 10 sine waves using floats. This is 
   meant for generating realistic data for non-linear fitting. */

	float time, temp;

	for(int n=0; n<d->num_samples; n++) {
		time = (float)n / (float)d->sample_rate;	// sample / (samples/sec)
		temp = 0.0;

		for(int i=0; i<d->num_frequencies; i++) {
			d->noise = (float)rand() / (float)(RAND_MAX);	// random number between 0 and 1 
			// d->noise = (d->noise * 2.0) - 1;	// random number between -1 and 1
			
			// temp += sin(2.0*M_PI*d->frequency[i]*time) + d->noise;

			d->noise *= 50.0;
			temp += d->a * sin(2.0*M_PI*d->frequency[i]*time);
			temp += d->b * cos(2.0*M_PI*d->frequency[i]*time);
			temp += d->noise;
		}

		/*
		if(d->num_frequencies > 1) {
			// no real reason to normalize here, but it could come in handy
			normalize(&temp, d->num_frequencies);
		}
		*/

		data[n] = temp;
	}
}

void normalize(float* value, int num_frequencies) {
/* Normalize waveforms composed of potentially multiple sine waves */
	
	float max = (float)num_frequencies;
	float min = (float)(-1.0 *num_frequencies);
	float range = max - min;

	*value = (*value - min) / range;
}


