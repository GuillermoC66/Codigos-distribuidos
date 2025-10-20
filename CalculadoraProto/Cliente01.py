import grpc
import calcu_pb2
import calcu_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = calcu_pb2_grpc.CalculadoraStub(channel)

# Prueba Suma
request_suma = calcu_pb2.Numeros(a=7, b=5)
respuesta_suma = stub.Suma(request_suma)
print(f"Suma: {request_suma.a} + {request_suma.b} = {respuesta_suma.resul}")

# Prueba Resta
request_resta = calcu_pb2.Numeros(a=10, b=3)
respuesta_resta = stub.Resta(request_resta)
print(f"Resta: {request_resta.a} - {request_resta.b} = {respuesta_resta.resul}")

# Prueba multi
request_multi = calcu_pb2.Numeros(a=10, b=3)
respuesta_multi = stub.Multi(request_multi)
print(f"Multiplicacion: {request_multi.a} * {request_multi.b} = {respuesta_multi.resul}")

# Prueba div
request_div = calcu_pb2.Numeros(a=9, b=3)
respuesta_div = stub.Div(request_div)
print(f"Division: {request_div.a} * {request_div.b} = {respuesta_div.resul}")
