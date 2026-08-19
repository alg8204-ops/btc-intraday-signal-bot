# BTC Intraday Signal Bot v2 — gratis y sin tarjeta

## Qué hace
- BTC/USDT, entrada 15m + régimen 4H.
- Usa solo datos públicos del exchange y Fear & Greed.
- Genera LONG/SHORT/NONE con score de confluencia.
- Calcula entrada, stop por ATR, TP y tamaño teórico.
- Envía señales a Telegram.
- **No contiene ejecución de órdenes reales ni pide API keys del exchange.**

## Modelo v2
1. Régimen 4H: precio y EMA20 respecto a EMA200.
2. Pullback/retest 15m de EMA20.
3. Cruce RSI 35/65.
4. Cruce del histograma MACD.
5. Volumen >= 0.90x su media de 20 velas.
6. Funding y Fear & Greed son filtros de riesgo, no puntos arbitrarios.
7. Stop = 1.5 ATR; TP = 2R.
8. Riesgo teórico = 0.5% por operación; límite diario conceptual 2%.

## Importante
Esto es un sistema de señales, no una estrategia demostrada como rentable. La versión anterior no tenía
backtest real y además no gestionaba correctamente el cierre de posiciones. Antes de operar con dinero,
haz backtest con datos históricos reales y paper trading.

## Opción recomendada: GitHub Actions
Un repositorio público de GitHub permite usar runners estándar de Actions sin cargo. El workflow se ejecuta
cada 15 minutos y se puede lanzar manualmente. Los secretos de Telegram se guardan en GitHub Secrets.

## Prueba local
Windows: ejecuta `run_local.bat`.
Linux/macOS: `bash run_local.sh`.

Para probar sin Internet, cambia `DATA_MODE=mock` y ejecuta `python main.py`.
