import grpc
from concurrent import futures
import json
import uuid
import os
import alumnos_pb2
import alumnos_pb2_grpc
from datetime import datetime

class AlumnoServicer(alumnos_pb2_grpc.AlumnoServiceServicer):
    def __init__(self):
        self.archivo_json = "alumnos.json"
        self._cargar_alumnos()

    def _cargar_alumnos(self):
        """Carga los alumnos desde el archivo JSON"""
        if os.path.exists(self.archivo_json):
            try:
                with open(self.archivo_json, 'r', encoding='utf-8') as f:
                    self.alumnos = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.alumnos = {}
        else:
            self.alumnos = {}
        print(f"Cargados {len(self.alumnos)} alumnos")

    def _guardar_alumnos(self):
        """Guarda los alumnos en el archivo JSON"""
        try:
            with open(self.archivo_json, 'w', encoding='utf-8') as f:
                json.dump(self.alumnos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando alumnos: {e}")
            return False

    def _generar_id(self):
        """Genera un ID único para el alumno"""
        return str(uuid.uuid4())

    def RegistrarAlumno(self, request, context):
        """Registra un nuevo alumno"""
        try:
            alumno_id = self._generar_id()
            
            alumno = {
                "id": alumno_id,
                "nombre": request.nombre,
                "apellido": request.apellido,
                "edad": request.edad,
                "curso": request.curso,
                "direccion": request.direccion,
                "fecha_registro": datetime.now().isoformat()
            }
            
            self.alumnos[alumno_id] = alumno
            
            if self._guardar_alumnos():
                return alumnos_pb2.AlumnoResponse(
                    id=alumno_id,
                    nombre=request.nombre,
                    apellido=request.apellido,
                    edad=request.edad,
                    curso=request.curso,
                    direccion=request.direccion,
                    mensaje="Alumno registrado exitosamente",
                    success=True
                )
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error al guardar en el archivo")
                return alumnos_pb2.AlumnoResponse(success=False)
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return alumnos_pb2.AlumnoResponse(success=False)

    def ConsultarAlumno(self, request, context):
        """Consulta un alumno por ID"""
        try:
            alumno_id = request.id
            if alumno_id in self.alumnos:
                alumno = self.alumnos[alumno_id]
                return alumnos_pb2.AlumnoResponse(
                    id=alumno["id"],
                    nombre=alumno["nombre"],
                    apellido=alumno["apellido"],
                    edad=alumno["edad"],
                    curso=alumno["curso"],
                    direccion=alumno["direccion"],
                    mensaje="Alumno encontrado",
                    success=True
                )
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Alumno no encontrado")
                return alumnos_pb2.AlumnoResponse(success=False)
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return alumnos_pb2.AlumnoResponse(success=False)

    def ActualizarAlumno(self, request, context):
        """Actualiza los datos de un alumno existente"""
        try:
            alumno_id = request.id
            if alumno_id in self.alumnos:
                # Actualizar datos
                self.alumnos[alumno_id].update({
                    "nombre": request.nombre,
                    "apellido": request.apellido,
                    "edad": request.edad,
                    "curso": request.curso,
                    "direccion": request.direccion,
                    "fecha_actualizacion": datetime.now().isoformat()
                })
                
                if self._guardar_alumnos():
                    return alumnos_pb2.AlumnoResponse(
                        id=alumno_id,
                        nombre=request.nombre,
                        apellido=request.apellido,
                        edad=request.edad,
                        curso=request.curso,
                        direccion=request.direccion,
                        mensaje="Alumno actualizado exitosamente",
                        success=True
                    )
                else:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Error al guardar en el archivo")
                    return alumnos_pb2.AlumnoResponse(success=False)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Alumno no encontrado")
                return alumnos_pb2.AlumnoResponse(success=False)
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return alumnos_pb2.AlumnoResponse(success=False)

    def EliminarAlumno(self, request, context):
        """Elimina un alumno por ID"""
        try:
            alumno_id = request.id
            if alumno_id in self.alumnos:
                alumno_eliminado = self.alumnos.pop(alumno_id)
                
                if self._guardar_alumnos():
                    return alumnos_pb2.AlumnoResponse(
                        id=alumno_id,
                        nombre=alumno_eliminado["nombre"],
                        apellido=alumno_eliminado["apellido"],
                        mensaje="Alumno eliminado exitosamente",
                        success=True
                    )
                else:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details("Error al guardar en el archivo")
                    return alumnos_pb2.AlumnoResponse(success=False)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Alumno no encontrado")
                return alumnos_pb2.AlumnoResponse(success=False)
                
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return alumnos_pb2.AlumnoResponse(success=False)

    def BuscarPorCriterios(self, request, context):
        """Busca alumnos por criterios (server streaming)"""
        try:
            criterios = {}
            if request.nombre:
                criterios["nombre"] = request.nombre.lower()
            if request.apellido:
                criterios["apellido"] = request.apellido.lower()
            if request.curso:
                criterios["curso"] = request.curso.lower()

            alumnos_encontrados = 0
            
            for alumno_id, alumno in self.alumnos.items():
                coincide = True
                
                for campo, valor in criterios.items():
                    if campo in alumno and valor not in alumno[campo].lower():
                        coincide = False
                        break
                
                if coincide:
                    alumnos_encontrados += 1
                    yield alumnos_pb2.AlumnoResponse(
                        id=alumno["id"],
                        nombre=alumno["nombre"],
                        apellido=alumno["apellido"],
                        edad=alumno["edad"],
                        curso=alumno["curso"],
                        direccion=alumno["direccion"],
                        mensaje=f"Resultado {alumnos_encontrados}",
                        success=True
                    )
            
            if alumnos_encontrados == 0:
                yield alumnos_pb2.AlumnoResponse(
                    mensaje="No se encontraron alumnos con los criterios especificados",
                    success=False
                )
                
        except Exception as e:
            yield alumnos_pb2.AlumnoResponse(
                mensaje=f"Error en la búsqueda: {str(e)}",
                success=False
            )

    def ListarTodos(self, request, context):
        """Lista todos los alumnos (server streaming)"""
        try:
            if not self.alumnos:
                yield alumnos_pb2.AlumnoResponse(
                    mensaje="No hay alumnos registrados",
                    success=False
                )
                return

            for alumno_id, alumno in self.alumnos.items():
                yield alumnos_pb2.AlumnoResponse(
                    id=alumno["id"],
                    nombre=alumno["nombre"],
                    apellido=alumno["apellido"],
                    edad=alumno["edad"],
                    curso=alumno["curso"],
                    direccion=alumno["direccion"],
                    success=True
                )
                
        except Exception as e:
            yield alumnos_pb2.AlumnoResponse(
                mensaje=f"Error al listar alumnos: {str(e)}",
                success=False
            )

def servir():
    """Inicia el servidor gRPC"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    alumnos_pb2_grpc.add_AlumnoServiceServicer_to_server(AlumnoServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC iniciado en el puerto 50051")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Servidor detenido")
        server.stop(0)

if __name__ == '__main__':
    servir()