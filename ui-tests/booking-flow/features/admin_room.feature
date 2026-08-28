Feature: Gestión de habitaciones por el administrador
  Como administrador del hotel
  Quiero crear nuevas habitaciones
  Para mantener actualizado el inventario disponible

  Scenario: Crear una habitación con servicios
    Given que inicio sesión como administrador
    When que creo una habitación nueva con tipo, precio y servicios
    Then que la habitación aparece en el listado de habitaciones correctamente
