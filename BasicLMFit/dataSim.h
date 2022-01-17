#ifndef DATASIM_H_	
#define DATASIM_H_

#include <stdint.h>
#include <stdio.h>

/* Module to generate simulated sine wave data of varying frequencies */

typedef struct data_obj {

	float	frequency[10];		// max of ten frequencies
	int		num_frequencies;
	
	int		sample_rate;
	int		num_samples;

	int		noise_factor;
	
	float*	data; 

} data_obj;

void wave_gen(data_obj* d, float* data);
/* Generate a superposition of up to 10 sine waves using floats. This is 
   meant for generating data for FFT. */

void normalize(double* value, int num_frequencies); 
/* Normalize waveforms composed of multiple sine waves to ensure wave
   amplitudes aren't out of range when writing to .wav file. */

#endif // DATASIM_H_
