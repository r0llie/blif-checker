from flask import Flask, request, render_template
import csv

app = Flask(__name__)

# CSV dosyasını yükle
def load_data():
    data = []
    with open('veri.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Cüzdan bilgilerini al ve toplam token miktarını hesapla
def get_wallet_info(wallets):
    data = load_data()
    total_tokens = 0
    wallet_info = []
    for wallet in wallets:
        wallet = wallet.lower() # cüzdanları küçük harfe dönüştür
        for row in data:
            if row['wallet'] == wallet:
                total_tokens += int(row['token_earned'])
                wallet_info.append(row)
    return total_tokens, wallet_info

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def result():
    wallets = request.form['wallets'].split('\n')
    wallets = [wallet.replace('\r', '') for wallet in wallets]

    total_tokens, wallet_info = get_wallet_info(wallets)
    return render_template('result.html', total_tokens=total_tokens, wallet_info=wallet_info)

if __name__ == '__main__':
    app.run(debug=True)
