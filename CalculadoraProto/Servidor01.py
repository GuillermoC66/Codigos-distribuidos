import grpc
from concurrent import futures
import calcu_pb2
import calcu_pb2_grpc

class CalculadoraServicerImpl(calcu_pb2_grpc.CalculadoraServicer):

    def Suma(self, request, context):
        resultado = request.a + request.b
        return calcu_pb2.Resultado(resul=resultado)

    def Resta(self, request, context):
        resultado = request.a - request.b
        return calcu_pb2.Resultado(resul=resultado)
    
    def Multi(self, request, context):
        resultado = request.a * request.b
        return calcu_pb2.Resultado(resul=resultado)
    
    def Div(self, request, context):
        resultado = request.a / request.b
        return calcu_pb2.Resultado(resul=resultado)

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
calcu_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicerImpl(), server)
server.add_insecure_port('[::]:50051')
server.start()
print("Servidor gRPC ejecutándose en el puerto 50051...")
server.wait_for_termination()
