import grpc
import alumnos_pb2
import alumnos_pb2_grpc
import sys

class ClienteAlumnos:
    def __init__(self, host='localhost', port=50051):
        self.canal = grpc.insecure_channel(f'{host}:{port}')
        self.stub = alumnos_pb2_grpc.AlumnoServiceStub(self.canal)
        print(f"Conectado al servidor en {host}:{port}")

    def registrar_alumno(self):
        """Registra un nuevo alumno"""
        print("\n--- REGISTRAR ALUMNO ---")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = int(input("Edad: "))
        curso = input("Curso: ")
        direccion = input("Dirección: ")

        try:
            respuesta = self.stub.RegistrarAlumno(
                alumnos_pb2.AlumnoRequest(
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad,
                    curso=curso,
                    direccion=direccion
                )
            )
            
            if respuesta.success:
                print(f"{respuesta.mensaje}")
                print(f"ID del alumno: {respuesta.id}")
            else:
                print(f"Error: {respuesta.mensaje}")
                
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

    def consultar_alumno(self):
        """Consulta un alumno por ID"""
        print("\n--- CONSULTAR ALUMNO ---")
        alumno_id = input("ID del alumno: ")

        try:
            respuesta = self.stub.ConsultarAlumno(
                alumnos_pb2.ConsultaRequest(id=alumno_id)
            )
            
            if respuesta.success:
                print("Alumno encontrado:")
                self._mostrar_alumno(respuesta)
            else:
                print(f"{respuesta.mensaje}")
                
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

    def actualizar_alumno(self):
        """Actualiza los datos de un alumno"""
        print("\n--- ACTUALIZAR ALUMNO ---")
        alumno_id = input("ID del alumno a actualizar: ")
        
        # Primero consultamos el alumno actual
        try:
            alumno_actual = self.stub.ConsultarAlumno(
                alumnos_pb2.ConsultaRequest(id=alumno_id)
            )
            
            if not alumno_actual.success:
                print("Alumno no encontrado")
                return
                
            print("Datos actuales:")
            self._mostrar_alumno(alumno_actual)
            print("\nIngrese los nuevos datos (dejar vacío para mantener el valor actual):")
            
            nombre = input(f"Nombre [{alumno_actual.nombre}]: ") or alumno_actual.nombre
            apellido = input(f"Apellido [{alumno_actual.apellido}]: ") or alumno_actual.apellido
            edad_str = input(f"Edad [{alumno_actual.edad}]: ")
            edad = int(edad_str) if edad_str else alumno_actual.edad
            curso = input(f"Curso [{alumno_actual.curso}]: ") or alumno_actual.curso
            direccion = input(f"Dirección [{alumno_actual.direccion}]: ") or alumno_actual.direccion

            respuesta = self.stub.ActualizarAlumno(
                alumnos_pb2.AlumnoRequest(
                    id=alumno_id,
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad,
                    curso=curso,
                    direccion=direccion
                )
            )
            
            if respuesta.success:
                print(f"{respuesta.mensaje}")
                print("Datos actualizados:")
                self._mostrar_alumno(respuesta)
            else:
                print(f"Error: {respuesta.mensaje}")
                
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

    def eliminar_alumno(self):
        """Elimina un alumno por ID"""
        print("\n--- ELIMINAR ALUMNO ---")
        alumno_id = input("ID del alumno a eliminar: ")

        try:
            respuesta = self.stub.EliminarAlumno(
                alumnos_pb2.ConsultaRequest(id=alumno_id)
            )
            
            if respuesta.success:
                print(f"{respuesta.mensaje}")
                print(f"Alumno eliminado: {respuesta.nombre} {respuesta.apellido}")
            else:
                print(f"{respuesta.mensaje}")
                
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

    def buscar_por_criterios(self):
        """Busca alumnos por criterios"""
        print("\n--- BUSCAR ALUMNOS ---")
        print("Ingrese uno o más criterios de búsqueda:")
        nombre = input("Nombre (opcional): ")
        apellido = input("Apellido (opcional): ")
        curso = input("Curso (opcional): ")

        try:
            resultados = self.stub.BuscarPorCriterios(
                alumnos_pb2.BusquedaRequest(
                    nombre=nombre,
                    apellido=apellido,
                    curso=curso
                )
            )
            
            encontrados = 0
            for respuesta in resultados:
                if respuesta.success:
                    encontrados += 1
                    print(f"\n--- Resultado {encontrados} ---")
                    self._mostrar_alumno(respuesta)
                else:
                    print(f"{respuesta.mensaje}")
                    
            if encontrados == 0 and not any([nombre, apellido, curso]):
                print("No se encontraron alumnos")
                
        except grpc.RpcError as e:
            print(f"Error gRPC: {e.details()}")

    def listar_todos(self):
        """Lista todos los alumnos"""
        print("\n--- LISTA DE TODOS LOS ALUMNOS ---")
        
        try:
            resultados = self.stub.ListarTodos(alumnos_pb2.Vacio())
            
            total = 0
            for respuesta in resultados:
                if respuesta.success:
                    total += 1
                    print(f"\n--- Alumno {total} ---")
                    self._mostrar_alumno(respuesta)
                else:
                    print(f"{respuesta.mensaje}")
                    
            print(f"\nTotal de alumnos: {total}")
            
        except grpc.RpcError as e:
            print(f" Error gRPC: {e.details()}")

    def _mostrar_alumno(self, alumno):
        """Muestra los datos de un alumno"""
        print(f"ID: {alumno.id}")
        print(f"Nombre: {alumno.nombre} {alumno.apellido}")
        print(f"Edad: {alumno.edad}")
        print(f"Curso: {alumno.curso}")
        print(f"Dirección: {alumno.direccion}")

    def menu_principal(self):
        """Menú principal del cliente"""
        while True:
            print("\n" + "="*50)
            print("SISTEMA DE GESTIÓN DE ALUMNOS")
            print("="*50)
            print("1. Registrar alumno")
            print("2. Consultar alumno por ID")
            print("3. Actualizar alumno")
            print("4. Eliminar alumno")
            print("5. Buscar por criterios")
            print("6. Listar todos los alumnos")
            print("0. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == "1":
                self.registrar_alumno()
            elif opcion == "2":
                self.consultar_alumno()
            elif opcion == "3":
                self.actualizar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":
                self.buscar_por_criterios()
            elif opcion == "6":
                self.listar_todos()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida")

if __name__ == '__main__':
    # Permite especificar host y puerto como argumentos
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = sys.argv[2] if len(sys.argv) > 2 else '50051'
    
    cliente = ClienteAlumnos(host, port)
    cliente.menu_principal()