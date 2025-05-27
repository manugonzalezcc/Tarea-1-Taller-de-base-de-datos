from app.crud import (
    crear_tipo_dispositivo, obtener_tipos_dispositivo,
    crear_grupo_dispositivos, obtener_grupos_dispositivos,
    crear_dispositivo, obtener_dispositivos,
    asociar_dispositivo_a_grupo, desasociar_dispositivo_de_grupo,
    crear_sensor, obtener_sensores_de_dispositivo,
    crear_lectura, obtener_ultimas_lecturas,
    crear_log_estado, obtener_logs_dispositivo
)

if __name__ == "__main__":
    # Tipos de dispositivo
    tipo = crear_tipo_dispositivo("Raspberry Pi", "Raspberry Pi 4", "Mini PC para IoT")
    print("Tipos de dispositivo:")
    for t in obtener_tipos_dispositivo():
        print(f"  ID: {t.id} | Fabricante: {t.fabricante} | Modelo: {t.modelo} | Descripción: {t.descripcion}")

    # Grupos
    grupo = crear_grupo_dispositivos("Sensores Edificio A", "Sensores del edificio principal")
    print("\nGrupos:")
    for g in obtener_grupos_dispositivos():
        print(f"  ID: {g.id} | Nombre: {g.nombre} | Descripción: {g.descripcion}")

    # Dispositivo
    dispositivo = crear_dispositivo("SN123", "v1.0", "Oficina 101", tipo.id)
    print("\nDispositivos:")
    for d in obtener_dispositivos():
        print(f"  ID: {d.id} | N° Serie: {d.numero_serie} | Firmware: {d.version_firmware} | Ubicación: {d.descripcion_ubicacion}")

    # Asociar dispositivo a grupo
    asociar_dispositivo_a_grupo(dispositivo.id, grupo.id)

    # Sensor
    sensor = crear_sensor(dispositivo.id, "temperatura", "°C", umbral_alerta=30.0)
    print("\nSensores del dispositivo:")
    for s in obtener_sensores_de_dispositivo(dispositivo.id):
        print(f"  ID: {s.id} | Tipo: {s.tipo_sensor} | Unidad: {s.unidad_medida} | Umbral: {s.umbral_alerta}")

    # Lectura
    crear_lectura(sensor.id, "25.5")
    print("\nÚltimas lecturas:")
    for l in obtener_ultimas_lecturas(sensor.id, 3):
        print(f"  ID: {l.id} | Valor: {l.valor_leido} | Timestamp: {l.timestamp}")

    # Log de estado
    crear_log_estado(dispositivo.id, "online", "Dispositivo conectado")
    print("\nHistorial de logs:")
    for log in obtener_logs_dispositivo(dispositivo.id):
        print(f"  ID: {log.id} | Estado: {log.estado} | Mensaje: {log.mensaje_opcional} | Timestamp: {log.timestamp}")