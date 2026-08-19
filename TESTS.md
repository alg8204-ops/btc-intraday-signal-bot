# Validación realizada

Se ha comprobado localmente:
- importación de todos los módulos;
- cálculo de EMA, RSI, MACD y ATR;
- generación de datos mock deterministas;
- ejecución completa de `run_once()` en modo mock/paper;
- cálculo de tamaño de posición y R:R;
- compilación sintáctica de todos los `.py`;
- flujo GitHub Actions validado estructuralmente.

La conexión pública a Binance/Alternative.me no puede validarse desde este entorno de ejecución
porque no dispone de resolución DNS/salida de Internet. Por eso la validación de red debe hacerse
al ejecutar el workflow en GitHub Actions; el workflow fallará claramente si el endpoint no responde.
