from flask import Flask, render_template, request
import requests

# Функция получения курса теперь на уровне модуля
def get_exchange_rate(from_currency, to_currency):
    if from_currency == to_currency:
        return 1.0
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        rates = data.get("rates", {})
        return rates.get(to_currency)
    except Exception:
        return None

def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def converter():
        result = None
        error = None
        from_cur = "USD"
        to_cur = "RUB"
        amount = 1.0

        if request.method == "POST":
            try:
                amount = float(request.form.get("amount", 0))
                from_cur = request.form.get("from_currency", "USD").upper()
                to_cur = request.form.get("to_currency", "RUB").upper()
            except ValueError:
                error = "Сумма должна быть числом."
                return render_template("index.html", result=result, error=error, from_cur=from_cur, to_cur=to_cur, amount=amount)

            if amount <= 0:
                error = "Сумма должна быть положительной."
            else:
                rate = get_exchange_rate(from_cur, to_cur)
                if rate is not None:
                    result = round(amount * rate, 2)
                else:
                    error = f"Не удалось получить курс {from_cur} -> {to_cur}."

        return render_template(
            "index.html",
            result=result,
            error=error,
            from_cur=from_cur,
            to_cur=to_cur,
            amount=amount
        )

    return app
