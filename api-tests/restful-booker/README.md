# api-tests/restful-booker

Suite pytest + requests contra [Restful-booker](https://restful-booker.herokuapp.com/apidoc) (`restful-booker.herokuapp.com`), la API de práctica de Mark Winteringham para reservas de hotel con autenticación por token.

## Qué prueba

- **Auth** (`tests/test_auth.py`): token con credenciales válidas e inválidas
- **CRUD** (`tests/test_booking_crud.py`): crear (con validación de schema `pydantic`), leer, actualizar (con y sin token), leer un id inexistente
- **Negativos** (`tests/test_negative_cases.py`): payload con campo requerido faltante, `/ping`, borrar y confirmar que ya no existe

## Comportamiento real verificado (no asumido)

Todo se verificó primero con `curl`/Postman antes de escribir código — varias de estas son inconsistencias reales de la API, no lo que "debería" ser según REST:

- `GET /ping` responde `201`, no `200`
- `POST /booking` responde `200`, no `201`, aunque crea el recurso
- `DELETE /booking/{id}` responde `201`, no `200`/`204`
- `PUT`/`DELETE` requieren `Cookie: token=...` (no `Authorization: Bearer`) — sin token, `403`
- `POST /auth` con credenciales inválidas responde `200` igual (no `401`), pero el body cambia a `{"reason": "Bad credentials"}` en vez de `{"token": "..."}` — **no se puede confiar solo en el status code** para este endpoint, hay que inspeccionar el body
- `POST /booking` con un campo requerido faltante (ej. sin `firstname`) responde `500 Internal Server Error`, no `400 Bad Request` — defecto real de la API: un dato inválido del cliente no debería tumbar el servidor

## Arquitectura

- `utils/config.py` — `BASE_URL` y credenciales de admin
- `utils/booking_client.py` — `BookingClient`, encapsula las llamadas HTTP (equivalente a un Page Object para la API); `update_booking()` acepta `token` opcional para poder testear "sin cookie de auth" como caso propio, distinto de "token inválido"
- `utils/schemas.py` — modelos `pydantic` para validar la forma de las respuestas
- `conftest.py` — fixtures `api_client`, `auth_token`, `booking_payload`, `created_booking` (crea y borra su propia reserva, mismo principio de aislamiento que la suite de UI: cada test es dueño de sus datos)
- `tests/` — casos de prueba

## Cómo correr

```bash
cd api-tests/restful-booker
../../.venv/Scripts/pytest -v

# con reporte Allure
../../.venv/Scripts/pytest -v --alluredir=allure-results
```

## Estado

✅ Auth, CRUD completo, validación de schema y casos negativos funcionando (10/10 `PASSED`).
