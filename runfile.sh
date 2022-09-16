cd /Users/yurisa2/petrosa/petrosa-data-crypto/petrosa-candles-consistency-checker
export PORT=9090
gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
