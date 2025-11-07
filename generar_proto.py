import subprocess
import sys

def generar_codigo_proto():
    """Genera el código Python a partir del archivo .proto"""
    try:
        subprocess.run([
            sys.executable, '-m', 'grpc_tools.protoc',
            '--proto_path=.',
            '--python_out=.',
            '--grpc_python_out=.',
            'alumnos.proto'
        ], check=True)
        print("Código gRPC generado exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"Error generando código gRPC: {e}")

if __name__ == '__main__':
    generar_codigo_proto()