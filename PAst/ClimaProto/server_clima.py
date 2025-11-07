import grpc
from concurrent import futures
import time
import clima_pb2
import clima_pb2_grpc

class ClimaServicer(clima_pb2_grpc.ClimaServicer):
    def ObtenerPronostico(self, request, context):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        for i in range(2):
            for dia in dias:
                yield clima_pb2.Pronostico(
                    dia=dia,
                    descripcion=f"Soleado en {request.ciudad}",
                    temperatura=25.0 + dias.index(dia)
            )
                time.sleep(0.5)  # Simula envío gradual de datos

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    clima_pb2_grpc.add_ClimaServicer_to_server(ClimaServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor de clima escuchando en puerto 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
