/* Back-Propagation Program ver1.01       */
/*                                        */
/* % cc backprop.c -lm -o backprop        */
/* % backprop filename                    */
/*                       1998.1.1 by NAKA */

#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<time.h>
#define INPUT 2
#define HIDDEN 2
#define OUTPUT 1
#define PATTERN 4
#define PR 100
#define MAX_T 10000
#define eta 2.4
#define eps 1.0e-4
#define alpha 0.8
#define beta 0.8
#define W0 0.5

double xi[INPUT+1],v[HIDDEN+1],o[OUTPUT],zeta[OUTPUT];
double w1[HIDDEN][INPUT+1],w2[OUTPUT][HIDDEN+1];
double d_w1[HIDDEN][INPUT+1],d_w2[OUTPUT][HIDDEN+1];
double pre_dw1[HIDDEN][INPUT+1],pre_dw2[OUTPUT][HIDDEN+1];
double data[PATTERN][INPUT],t_data[PATTERN][OUTPUT];

void load_data(char *filename);
void back_propagation();
void w_init();
double ranran();
void dw_init();
void xi_set(long int t, int p);
void forward(long int t);
void backward();
double calc_error();
void modify_w();
void w_print();
double sigmoid(double u);

main(int argc, char *argv[])
{
	load_data(*++argv);

	back_propagation();
	
	w_print();
}

void load_data(char *filename)
{
	int p,k,i;
	double value;
	FILE *fp;

	fp = fopen(filename,"r");
	if( fp == NULL ) {
		fprintf(stderr,"File Open Error!\n");
		exit(0);
	}

	for( p=0 ; p < PATTERN ; p++ ){
		for( k=0 ; k < INPUT ; k++ ){
			fscanf(fp," %lf",&value);
			data[p][k] = value;
		}
		for( i=0 ; i < OUTPUT ; i++ ){
			fscanf(fp," %lf",&value);
			t_data[p][i] = value;
		}
	}
	fclose(fp);

	printf("Input      Desired\n");
        for( p=0 ; p<PATTERN ; p++ ){
                printf("{");
                for( k=0 ; k<INPUT ; k++ )
                        printf(" %.0lf,",data[p][k]);
                printf("} -> {");
                for( i=0 ; i<OUTPUT ; i++)
                        printf("%.0lf,",t_data[p][i]);
                printf("}\n");
        }
	putchar('\n');

}

void back_propagation()
{
	long int t;
	int p;
	double E,Esum;

	w_init();

	for( t=0 ; t < MAX_T ; t++ ){

		dw_init();

		for( p=0, Esum=0 ; p < PATTERN ; p++ ){
			xi_set(t,p);
			forward(t);
			backward();
			Esum += calc_error();
		}

		modify_w();

		E = Esum / (OUTPUT * PATTERN);
		if( t%PR == 0 )
			printf("%ld %e\n",t,E);

		if( E < eps )
			break;
	}

	printf("\nTime = %ld",t);
	if( t == MAX_T )
		printf(" (MAX) You must retry!");
	putchar('\n');

	for( p=0 ; p < PATTERN ; p++ ){
		xi_set(0,p);
		forward(0);
	}

	printf("E = %e\n",E);
}

void w_init()
{
	int i,j,k;
	long time_t;

	time_t = time(NULL);
	srand48(time_t);
	
	for( j=0 ; j < HIDDEN ; j++ )
		for( k=0 ; k <INPUT+1 ; k++ ){
			w1[j][k] = ranran();
			d_w1[j][k] = 0.0;
		}
	for( i=0 ; i < OUTPUT ; i++ )
		for( j=0 ; j < HIDDEN+1 ; j++ ){
			w2[i][j] = ranran();
			d_w2[i][j] = 0.0;
		}
}

double ranran()
{
	double r;

	r = drand48();
	r = r * 2*W0 - W0;
	
	return r;
}

void dw_init()
{
	int i,j,k;

	for( j=0 ; j < HIDDEN ; j++)
		for( k=0 ; k < INPUT+1 ; k++ ){
		    pre_dw1[j][k] = d_w1[j][k];
		    d_w1[j][k] = 0.0;
		}
	for( i=0 ; i <OUTPUT ; i++ )
		for( j=0 ; j < HIDDEN+1 ; j++ ){
		    pre_dw2[i][j] = d_w2[i][j];
		    d_w2[i][j] = 0.0;
		}
}

void xi_set(long int t, int p)
{
	int i,k;
	
	if( t%PR == 0 ) printf("Input ");

	for( k=0 ; k < INPUT ; k++ ){
		xi[k] = data[p][k];
		if( t%PR == 0 ) printf(" %.0lf ",xi[k]);
	}

	xi[INPUT] = 1.0;

	if( t%PR == 0 ) putchar('(');

	for( i=0 ; i < OUTPUT ; i++ ){
		zeta[i] = t_data[p][i];
		if( t%PR == 0 ) printf(" %.0lf ",zeta[i]);
	}

	if( t%PR == 0 ) printf(")\n");
}

void forward(long int t)
{
	int i,j,k;
	double sum;
	
	for( j=0 ; j < HIDDEN ; j++ ){
		for( k=0, sum=0 ; k < INPUT+1 ; k++ )
			sum += xi[k] * w1[j][k];
		v[j] = sigmoid(sum);
	}

	if( t%PR == 0 ) printf("Output ");

	v[HIDDEN] = 1.0;

	for( i=0 ; i < OUTPUT ; i++ ){
		for( j=0, sum=0 ; j < HIDDEN+1 ; j++ )
			sum += v[j] * w2[i][j];
		o[i] = sigmoid(sum);
		if( t%PR == 0 ) printf(" %.4lf",o[i]);
	}
	if(t %PR == 0 ) putchar('\n');
}

void backward()
{
	int i,j,k;
	double delta2[OUTPUT],delta1[HIDDEN+1],sum;
	
	for( i=0 ; i < OUTPUT ; i++ )
		delta2[i] = beta * o[i] * (1-o[i]) * (zeta[i]-o[i]);

	for( j=0 ; j < HIDDEN ; j++){
		for( i=0, sum=0 ; i < OUTPUT ; i++ )
			sum += w2[i][j] * delta2[i];
		delta1[j] = beta * v[j] * (1-v[j]) * sum;
	}

	for( i=0 ; i < OUTPUT ; i++ )
		for( j=0 ; j < HIDDEN+1 ; j++)
			d_w2[i][j] += delta2[i] * v[j];

	for( j=0 ; j < HIDDEN ; j++ )
		for( k=0 ; k < INPUT+1 ; k++ )
			d_w1[j][k] += delta1[j] * xi[k];
}

double calc_error()
{
	double E=0;
	int i;
	
	for( i=0 ; i < OUTPUT ; i++ )
		E += (zeta[i]-o[i]) * (zeta[i]-o[i]);

	return E;
}

void modify_w()
{
	int i,j,k;
	
	for( i=0 ; i < OUTPUT ; i++ )
		for( j=0 ; j < HIDDEN+1 ; j++ ){
			d_w2[i][j] = eta * d_w2[i][j] + alpha * pre_dw2[i][j];
			w2[i][j] = w2[i][j] + d_w2[i][j];
		}

	for( j=0 ; j < HIDDEN ; j++)
		for( k=0 ; k < INPUT+1 ; k++ ){
			d_w1[j][k] = eta * d_w1[j][k] + alpha * pre_dw1[j][k];
			w1[j][k] = w1[j][k] + d_w1[j][k];
		}
}

void w_print()
{
	int i,j,k;
	
	printf("Weight\n");
	for(j =0 ; j < HIDDEN ; j++ ){
		printf("w1[%d]={",j);
		for( k=0 ; k < INPUT ; k++ ){
			if( k != 0 )
				putchar(',');
			printf("%.6lf",w1[j][k]);
		}
		printf("} theta1[%d]=%.6lf\n",j,w1[j][k]);
	}

	for( i=0 ; i < OUTPUT ; i++ ){
		printf("w2[%d]={",i);
		for( j=0 ; j < HIDDEN ;j ++ ){
			if( j != 0 )
				putchar(',');
			printf("%.6lf",w2[i][j]);
		}
		printf("} theta2[%d]=%.6lf\n",i,w2[i][j]);
	}
}

double sigmoid(double u)
{
	return 1.0 / (1.0+exp(-beta*u));
}

