import grpc
import clima_pb2
import clima_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = clima_pb2_grpc.ClimaStub(channel)
        # Enviar la solicitud con el nombre de la ciudad
        respuesta_stream = stub.ObtenerPronostico(
            clima_pb2.PeticionClima(ciudad="CDMX")
        )

        # Recibir los mensajes uno por uno
        for pronostico in respuesta_stream:
            print(f"{pronostico.dia}: {pronostico.descripcion}, {pronostico.temperatura}°C")

if __name__ == "__main__":
    run()
