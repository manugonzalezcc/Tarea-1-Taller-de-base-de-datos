from app.models import *
from app.database import SessionLocal

def crear_tipo_dispositivo(fabricante, modelo, descripcion=None):
    session = SessionLocal()
    tipo = TipoDispositivo(fabricante=fabricante, modelo=modelo, descripcion=descripcion)
    session.add(tipo)
    session.commit()
    session.refresh(tipo)
    session.close()
    return tipo

def obtener_tipos_dispositivo():
    session = SessionLocal()
    tipos = session.query(TipoDispositivo).all()
    session.close()
    return tipos

def crear_grupo_dispositivos(nombre, descripcion=None):
    session = SessionLocal()
    grupo = GrupoDispositivos(nombre=nombre, descripcion=descripcion)
    session.add(grupo)
    session.commit()
    session.refresh(grupo)
    session.close()
    return grupo

def obtener_grupos_dispositivos():
    session = SessionLocal()
    grupos = session.query(GrupoDispositivos).all()
    session.close()
    return grupos

def crear_dispositivo(numero_serie, version_firmware, descripcion_ubicacion, tipo_dispositivo_id, mac_address=None, coordenadas_gps=None, estado_actual=None):
    session = SessionLocal()
    dispositivo = Dispositivo(
        numero_serie=numero_serie,
        version_firmware=version_firmware,
        descripcion_ubicacion=descripcion_ubicacion,
        tipo_dispositivo_id=tipo_dispositivo_id,
        mac_address=mac_address,
        coordenadas_gps=coordenadas_gps,
        estado_actual=estado_actual
    )
    session.add(dispositivo)
    session.commit()
    session.refresh(dispositivo)
    session.close()
    return dispositivo

def obtener_dispositivos():
    session = SessionLocal()
    dispositivos = session.query(Dispositivo).all()
    session.close()
    return dispositivos

def asociar_dispositivo_a_grupo(dispositivo_id, grupo_id):
    session = SessionLocal()
    dispositivo = session.query(Dispositivo).get(dispositivo_id)
    grupo = session.query(GrupoDispositivos).get(grupo_id)
    if grupo not in dispositivo.grupos:
        dispositivo.grupos.append(grupo)
        session.commit()
    session.close()

def desasociar_dispositivo_de_grupo(dispositivo_id, grupo_id):
    session = SessionLocal()
    dispositivo = session.query(Dispositivo).get(dispositivo_id)
    grupo = session.query(GrupoDispositivos).get(grupo_id)
    if grupo in dispositivo.grupos:
        dispositivo.grupos.remove(grupo)
        session.commit()
    session.close()

def crear_sensor(dispositivo_id, tipo_sensor, unidad_medida, umbral_alerta=None):
    session = SessionLocal()
    sensor = Sensor(
        dispositivo_id=dispositivo_id,
        tipo_sensor=tipo_sensor,
        unidad_medida=unidad_medida,
        umbral_alerta=umbral_alerta
    )
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    session.close()
    return sensor

def obtener_sensores_de_dispositivo(dispositivo_id):
    session = SessionLocal()
    sensores = session.query(Sensor).filter_by(dispositivo_id=dispositivo_id).all()
    session.close()
    return sensores

def crear_lectura(sensor_id, valor_leido):
    session = SessionLocal()
    lectura = LecturaDato(sensor_id=sensor_id, valor_leido=valor_leido)
    session.add(lectura)
    session.commit()
    session.refresh(lectura)
    session.close()
    return lectura

def obtener_ultimas_lecturas(sensor_id, n=5):
    session = SessionLocal()
    lecturas = session.query(LecturaDato).filter_by(sensor_id=sensor_id).order_by(LecturaDato.timestamp.desc()).limit(n).all()
    session.close()
    return lecturas

def crear_log_estado(dispositivo_id, estado, mensaje_opcional=None):
    session = SessionLocal()
    log = LogEstadoDispositivo(dispositivo_id=dispositivo_id, estado=estado, mensaje_opcional=mensaje_opcional)
    session.add(log)
    # Actualiza el estado_actual del dispositivo
    dispositivo = session.query(Dispositivo).get(dispositivo_id)
    dispositivo.estado_actual = estado
    session.commit()
    session.refresh(log)
    session.close()
    return log

def obtener_logs_dispositivo(dispositivo_id):
    session = SessionLocal()
    logs = session.query(LogEstadoDispositivo).filter_by(dispositivo_id=dispositivo_id).order_by(LogEstadoDispositivo.timestamp.desc()).all()
    session.close()
    return logs