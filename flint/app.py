from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

CHAINS = {
    "mantle": {
        "contract": "0xDCBc586cAb42a1D193CaCD165a81E5fbd9B428d7",
        "provider": "https://rpc.mantle.pw/eth/",
    },
    "linea": {
        "contract": "0xDCBc586cAb42a1D193CaCD165a81E5fbd9B428d7",
        "provider": "https://rpc.linea.network/",
    },
    "kroma": {
        "contract": "0x7afb9de72A9A321fA535Bb36b7bF0c987b42b859",
        "provider": "https://rpc.kroma.io/",
    },
}


def get_balance(chain, contract):
    provider = chain["provider"]
    response = requests.post(
        provider,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBalance",
            "params": [contract, "latest"],
        },
    )
    return int(response.json()["result"], 16) / 1e18


def get_past_balance(chain, contract, timestamp):
    provider = chain["provider"]
    response = requests.post(
        provider,
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBalance",
            "params": [contract, int(timestamp)],
        },
    )
    return int(response.json()["result"], 16) / 1e18


@app.route("/")
def index():
    data = {}
    current_time = int(time.time())
    past_time = current_time - 12 * 60 * 60
    for chain_name, chain_data in CHAINS.items():
        current_balance = get_balance(chain_data, chain_data["contract"])
        past_balance = get_past_balance(chain_data, chain_data["contract"], past_time)
        balance_change = (current_balance - past_balance) / past_balance * 100
        data[chain_name] = {
            "balance": current_balance,
            "change": balance_change,
            "alert": balance_change < -10,
        }
    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)