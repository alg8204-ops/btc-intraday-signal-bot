# GUÍA DEFINITIVA — sin tarjeta y sin pagar

## 1. Crear GitHub
1. Entra en https://github.com y crea una cuenta si no tienes.
2. Crea un repositorio nuevo, preferiblemente **público** para que Actions no consuma tu cuota privada.
3. Nombre sugerido: `btc-intraday-signal-bot`.
4. No subas claves, tokens ni archivos `.env`.

## 2. Subir el bot
Descomprime este ZIP.
Sube todos los archivos y la carpeta `.github/workflows/` al repositorio.
La rama por defecto debe contener `.github/workflows/btc_signal.yml`.

## 3. Crear Telegram
1. En Telegram abre @BotFather.
2. Usa `/newbot`.
3. Guarda el token.
4. Abre tu bot y pulsa Start.
5. Obtén tu chat_id con un método fiable de Telegram (puedes usar `getUpdates` de la Bot API).
6. Nunca publiques el token.

## 4. Guardar los secretos
En GitHub:
Repository → Settings → Secrets and variables → Actions → New repository secret.

Crea exactamente:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

No necesitas EXCHANGE_API_KEY ni EXCHANGE_API_SECRET.

## 5. Activar
Ve a Actions → BTC 15m Signal Bot → Run workflow.

Después el workflow quedará programado cada 15 minutos. GitHub permite programaciones
desde 5 minutos; el workflow puede sufrir retrasos puntuales. En repositorios públicos,
los runners estándar de Actions no tienen minutos facturables.

## 6. Verificar
En Actions abre una ejecución.
Debe terminar en verde y mostrar `BTC SIGNAL | ...`.
Si hay LONG/SHORT, recibirás el mensaje en Telegram.

## 7. Qué significa cada señal
- `NONE`: no hay confluencia suficiente.
- `LONG`: tendencia 4H alcista + confirmación 15m + filtros superados.
- `SHORT`: tendencia 4H bajista + confirmación 15m + filtros superados.
- Entry/SL/TP son niveles teóricos para paper trading.

## 8. No hagas todavía
- No introduzcas API keys del exchange.
- No conviertas esto en ejecución automática.
- No uses dinero real hasta disponer de backtest out-of-sample y varias semanas de paper trading.

## 9. Mantenimiento
Los workflows programados de repositorios públicos pueden deshabilitarse si no hay actividad
en el repositorio durante 60 días. Haz un pequeño commit/revisión antes de ese plazo.
