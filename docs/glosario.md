# Glosario

## Idempotente

Una operación es idempotente cuando ejecutarla varias veces produce el mismo
resultado que ejecutarla una sola vez. Aplicado al seed del catálogo de
estados (ver [contrato de la API](contrato-api.md#estados)): correr la
migración dos veces no debe duplicar los registros ni fallar, debe dejar el
catálogo en el mismo estado que una sola ejecución.
