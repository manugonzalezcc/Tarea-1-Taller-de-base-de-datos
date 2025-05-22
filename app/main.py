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
    print("Tipos de dispositivo:", obtener_tipos_dispositivo())

    # Grupos
    grupo = crear_grupo_dispositivos("Sensores Edificio A", "Sensores del edificio principal")
    print("Grupos:", obtener_grupos_dispositivos())

    # Dispositivo
    dispositivo = crear_dispositivo("SN123", "v1.0", "Oficina 101", tipo.id)
    print("Dispositivos:", obtener_dispositivos())

    # Asociar dispositivo a grupo
    asociar_dispositivo_a_grupo(dispositivo.id, grupo.id)

    # Sensor
    sensor = crear_sensor(dispositivo.id, "temperatura", "°C", umbral_alerta=30.0)
    print("Sensores del dispositivo:", obtener_sensores_de_dispositivo(dispositivo.id))

    # Lectura
    crear_lectura(sensor.id, "25.5")
    print("Últimas lecturas:", obtener_ultimas_lecturas(sensor.id, 3))

    # Log de estado
    crear_log_estado(dispositivo.id, "online", "Dispositivo conectado")
    print("Historial de logs:", obtener_logs_dispositivo(dispositivo.id))