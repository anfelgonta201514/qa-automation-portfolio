Feature: Reserva de habitación
  Como visitante del hotel
  Quiero reservar una habitación con mis datos de contacto
  Para asegurar mi estadía

  Scenario: Reserva exitosa con datos válidos
    Given que estoy en la página de inicio de Restful Booker Platform
    When busco disponibilidad y selecciono una habitación
    And completo el formulario de reserva con datos de contacto válidos
    Then la reserva queda confirmada
