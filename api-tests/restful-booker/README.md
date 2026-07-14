# api-tests/restful-booker

Suite pytest + requests contra [Restful-booker](https://restful-booker.herokuapp.com/apidoc) (`restful-booker.herokuapp.com`), la API de práctica de Mark Winteringham para reservas de hotel con autenticación por token.

## Qué prueba

- CRUD completo de reservas (crear, leer, actualizar, eliminar)
- Autenticación: token válido, credenciales inválidas, endpoints protegidos sin token
- Validación de schema de respuesta con `pydantic`
- Casos negativos: IDs inexistentes, datos inválidos/incompletos

## Comportamiento real verificado (no asumido)

- `GET /ping` responde `201`, no `200` — quirk de esta API, testeado explícitamente
- `POST /booking` responde `200`, no `201`, aunque crea el recurso
- `DELETE /booking/{id}` responde `201`, no `200`/`204`
- `PUT`/`DELETE` requieren `Cookie: token=...` (no `Authorization: Bearer`) — sin token, `403`

## Arquitectura

- `utils/config.py` — `BASE_URL` y credenciales de admin
- `utils/booking_client.py` — `BookingClient`, encapsula las llamadas HTTP (equivalente a un Page Object para la API)
- `utils/schemas.py` — modelos `pydantic` para validar la forma de las respuestas
- `conftest.py` — fixtures `api_client`, `auth_token`, `booking_payload`, `created_booking` (crea y borra su propia reserva, mismo principio de aislamiento que la suite de UI)
- `tests/` — casos de prueba

## Cómo correr

```bash
cd api-tests/restful-booker
../../.venv/Scripts/pytest -v
```

## Estado

🔄 En construcción.
