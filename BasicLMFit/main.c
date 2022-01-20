#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "dataSim.h"

/*	Outline for Levenberg-Marquardt fit in C.
	
	Script attempts to fit a wave of form asin(wt) + b(cos(wt))

	WARNING: script is only an outline and while it compiles, it is not
			 functional.

	To Build: gcc main.c dataSim.c -o lmfit -lm
	To Run:   ./lmfit

	Acronyms: lm   - levenberg-marquardt
			  sosq - sum of square
*/

void main() {

	/* SIMULATE NOISY SINE DATA ****************************************** */
	data_obj input;

	input.frequency[0] = 1;
	input.num_frequencies = 1;
	input.sample_rate = 64;
	input.num_samples = input.sample_rate * 1;

	input.a = 100.0;
	input.b = 102.0;

	input.data = (float*)malloc(sizeof(float)*input.num_samples);

	wave_gen(&input, input.data);

	printf("\nSIMULATED INPUT DATA TO BE FITTED\n");
	printf("---------------------------------\n");
	for(int i=0; i<input.num_samples; i++)
	{
		printf("%f			|\n", input.data[i]);
	}
	printf("---------------------------------\n\n");
	/* ******************************************************************* */

	/* LM Fit ************************************************************ */
	/* STATUS: Non-Functional Outline ************************************ */

	/* Definitions ******************************** */

	int num_parameters = 3;

	// First guesses
	float a0 = 100.5, b0 = 102.5, freq0 = 1.5;

	// Current guesses
	float a_est = a0, b_est = b0, freq_est = freq0;

	int max_iterations = 100;
	
	float lamda = 0.01;	// damping factor

	float time; 

	int update_jacobian = 1;

	/* ******************************************* */

	/* Mallocs ********************************** */

	// Allocate memory for estimated data
	float *data_est = (float*)malloc(sizeof(float)*input.num_samples);
	float *data_est_lm = (float*)malloc(sizeof(float)*input.num_samples);

	// Allocate memory for residuals
	float *residual = (float*)malloc(sizeof(float)*input.num_samples);
	float *residual_lm = (float*)malloc(sizeof(float)*input.num_samples);
	float residual_sosq = 0.0, residual_lm_sosq = 0.0;	

	/* ****************************************** */

	for(int iteration=0; iteration < max_iterations; iteration++) 
	{	/* MAIN LOOP ***************************************** */

		// 1. Determine if Jacobian needs to be updated 
		//	  Initially it will need to be 
		if(update_jacobian) 
		{
			// 2. Compute the Jacobian at the current parameters
			//	  Don't know how to do this.

			// Compute the estimated data at the current parameters
			for(int i=0; i<input.num_samples; i++)
			{
				time = (float)i / (float)input.sample_rate;	// sample / (samples/sec)
				data_est[i] = a_est*sin(2.0*M_PI*freq_est*time) + b_est*cos(2.0*M_PI*freq_est*time);;
		
				residual[i] = input.data[i] - data_est[i];
			}

			// 4. Compute the Hessian using the Jacobian
			//	  Don't know how to do this

			// If it's the first iteration, compute the total residual
			if(iteration == 1)
			{
				for(int i=0; i<input.num_samples; i++)
				{
					// 3. Evaluate the risidual error
					residual[i] = input.data[i] - data_est[i];
					// Compute the total error (sum of the squares)
					residual_sosq += residual[i] * residual[i];
				}
			}

		}	// if(update_jacobian)

		// 5. Apply the damping factor to the Hessian matrix
		//	  Don't know how to do this 

		// 6. Compute updated parameters
		//	  Don't know how to do this
		float a_lm, b_lm, freq_lm;

		// 7. Calculate new residual error at the updated parameters
		for(int n=0; n<input.num_samples; n++) {
			time = (float)n / (float)input.sample_rate;	// sample / (samples/sec)
			data_est_lm[n] = a_lm*sin(2.0*M_PI*freq_lm*time) + b_lm*cos(2.0*M_PI*freq_lm*time);;
		}

		for(int i=0; i<input.num_samples; i++)
		{
			residual_lm[i] = input.data[i] - data_est_lm[i];
			residual_lm_sosq += residual_lm[i] * residual_lm[i]; // sum the squares
		}

		// 8. Check if residual error decreased to determine whether damping
		//	  should be decreased or increased and whether the jacobian should
		//	  be recomputed
		if(residual_lm_sosq < residual_sosq)
		{
			// make the updated parameters to be the current parameters and 
			// update the damping factor
			update_jacobian = 1;
			lamda /= 10;
			a_est = a_lm;
			b_est = b_lm;
			residual = residual_lm;

		}
		else 
		{
			// increase the damping factor without updating the jacobian
			update_jacobian = 0;
			lamda *= 10;
		}

	}	/* MAIN LOOP ***************************************** */

	// Free all mallocs
	free(data_est);
	free(data_est_lm);
	free(residual);
	free(residual_lm);

}







