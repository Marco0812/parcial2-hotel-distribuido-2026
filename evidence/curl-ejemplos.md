# Curl de double

`curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -d '{"guest": "Test", "room_type": "double", "check_in": "2026-05-01", "check_out": "2026-05-05"}'`

## Respuesta

`{"booking_id":"fa79635e-899c-4b4b-a921-5daf03470455","status":"REQUESTED"}`


# Curl de single 

`curl -X POST http://localhost:8000/bookings \
  -H "Content-Type: application/json" \
  -d '{"guest": "Parker", "room_type": "single", "check_in": "2026-05-10", "check_out": "2026-05-15"}'`

  ## Respuesta 

  `{"booking_id":"1d524cf8-c257-409e-9248-618c5059bed5","status":"REQUESTED"}`
