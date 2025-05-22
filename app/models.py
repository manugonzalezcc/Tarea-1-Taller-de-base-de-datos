from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Table, Float
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Tabla de asociación para muchos-a-muchos.
dispositivo_grupo = Table(
    'dispositivo_grupo', Base.metadata,
    Column('dispositivo_id', Integer, ForeignKey('dispositivo.id'), primary_key=True),
    Column('grupo_id', Integer, ForeignKey('grupo_dispositivos.id'), primary_key=True)
)

class TipoDispositivo(Base):
    __tablename__ = 'tipo_dispositivo'
    id = Column(Integer, primary_key=True)
    fabricante = Column(String, nullable=False)
    modelo = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)
    dispositivos = relationship("Dispositivo", back_populates="tipo_dispositivo")

class GrupoDispositivos(Base):
    __tablename__ = 'grupo_dispositivos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)
    dispositivos = relationship(
        "Dispositivo",
        secondary=dispositivo_grupo,
        back_populates="grupos"
    )

class Dispositivo(Base):
    __tablename__ = 'dispositivo'
    id = Column(Integer, primary_key=True)
    numero_serie = Column(String, unique=True, nullable=False)
    mac_address = Column(String, unique=True)
    version_firmware = Column(String, nullable=False)
    descripcion_ubicacion = Column(String, nullable=False)
    coordenadas_gps = Column(String)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    tipo_dispositivo_id = Column(Integer, ForeignKey('tipo_dispositivo.id'))
    tipo_dispositivo = relationship("TipoDispositivo", back_populates="dispositivos")
    sensores = relationship("Sensor", back_populates="dispositivo")
    logs = relationship("LogEstadoDispositivo", back_populates="dispositivo")
    grupos = relationship(
        "GrupoDispositivos",
        secondary=dispositivo_grupo,
        back_populates="dispositivos"
    )
    estado_actual = Column(String)  # Modificación de esquema

class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivo.id'))
    tipo_sensor = Column(String, nullable=False)
    unidad_medida = Column(String, nullable=False)
    umbral_alerta = Column(Float)  # Modificación de esquema
    dispositivo = relationship("Dispositivo", back_populates="sensores")
    lecturas = relationship("LecturaDato", back_populates="sensor")

class LecturaDato(Base):
    __tablename__ = 'lectura_dato'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    valor_leido = Column(String, nullable=False)
    sensor = relationship("Sensor", back_populates="lecturas")

Sensor.lecturas = relationship("LecturaDato", back_populates="sensor")

class LogEstadoDispositivo(Base):
    __tablename__ = 'log_estado_dispositivo'
    id = Column(Integer, primary_key=True)
    dispositivo_id = Column(Integer, ForeignKey('dispositivo.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String, nullable=False)
    mensaje_opcional = Column(Text)
    dispositivo = relationship("Dispositivo", back_populates="logs")