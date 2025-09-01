//Guillermo Carrillo RodrÃ­guez 1/09/2025
#include <mpi.h>
#include <stdio.h>
int main (int argc, char** argv){	
	int rank, size;
   	MPI_Status status; 
	MPI_Init(&argc, &argv); 
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); 
   	 
	MPI_Comm_size(MPI_COMM_WORLD, &size); 
	if (rank==0)
	 
	{ 
		int mensaje=42; 
		
	 	printf("Proceso %d envia mensaje %d  al proceso 1 ", rank,mensaje); 
	 	MPI_Send(&mensaje, 0, MPI_INT, 0, 0, MPI_COMM_WORLD);
	 	MPI_Recv(&mensaje,1,MPI_INT,1,0, MPI_COMM_WORLD,&status); 
	 	printf("Proceso %d  recibio %d al proceso 1", rank, mensaje );
    }
    if (rank ==1)
	{ 
		int mensaje1; 
        MPI_Recv(&mensaje1,1,MPI_INT,0,0,MPI_COMM_WORLD, &status); 
		printf("Proceso %d recibio  %d al proceso 0 ", rank,mensaje1);
		mensaje1+=4; 
		MPI_Send(&mensaje1, 0, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }
    MPI_Finalize(); return 0;
}
