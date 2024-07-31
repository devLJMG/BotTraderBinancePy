import ccxt
import numpy as np
import tkinter as tk

# Configurações da Binance
binance_api_key = 'insert your  api key, here'
binance_api_secret = 'Bottrader1'
symbol = 'BTC/USDT'
timeframe = '5m'

# Configurações para análise técnica
periods = 20  # Período da média móvel e bandas de Bollinger
rsi_period = 14  # Período do RSI

# Configuração da Binance API
binance = ccxt.binance({
    'apiKey': binance_api_key,
    'secret': binance_api_secret,
})

def get_historical_data(symbol, timeframe='5m', limit=100):
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=limit)
    return np.array([candle[4] for candle in ohlcv])  # Fechamento dos candles

def calculate_sma(data, window):
    return np.convolve(data, np.ones(window)/window, mode='valid')

def calculate_bollinger_bands(data, window):
    sma = calculate_sma(data, window)
    rolling_std = np.std(data, ddof=0)
    upper_band = sma + 2 * rolling_std
    lower_band = sma - 2 * rolling_std
    return upper_band, sma, lower_band

def calculate_rsi(data, window):
    diff = np.diff(data)
    gain = np.where(diff > 0, diff, 0)
    loss = np.where(diff < 0, -diff, 0)

    avg_gain = calculate_sma(gain, window)
    avg_loss = calculate_sma(loss, window)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def execute_trade_signal(data, sma, upper_band, lower_band, rsi):
    if data[-1] < lower_band[-1] and rsi[-1] < 30:
        return "Compra"
    elif data[-1] > upper_band[-1] and rsi[-1] > 70:
        return "Venda"
    else:
        return "Nenhuma operação"

def main():
    # Criar janela tkinter
    root = tk.Tk()
    root.title("Resultado das Operações")

    # Obtendo dados históricos
    historical_data = get_historical_data(symbol, timeframe)

    # Calculando indicadores
    sma = calculate_sma(historical_data, periods)
    upper_band, _, lower_band = calculate_bollinger_bands(historical_data, periods)
    rsi = calculate_rsi(historical_data, rsi_period)

    # Exemplo de lógica de negociação simples
    trade_result = execute_trade_signal(historical_data, sma, upper_band, lower_band, rsi)

    # Exibir resultado na janela
    result_label = tk.Label(root, text=f"Resultado da Operação: {trade_result}")
    result_label.pack()

    # Iniciar loop da interface gráfica
    root.mainloop()

if __name__ == "__main__":
    main()
