from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rate(from_currency: str, to_currency: str) -> float | None:
    """
    Возвращает курс from_currency -> to_currency через exchangerate-api.com
    """
    if from_currency == to_currency:
        return 1.0
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        rates = data.get("rates", {})
        if to_currency in rates:
            return rates[to_currency]
        else:
            return None
    except Exception as e:
        print(f"Ошибка API: {e}")
        return None

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
                error = f"Не удалось получить курс {from_cur} -> {to_cur}. Проверьте правильность кодов валют."

    return render_template(
        "index.html",
        result=result,
        error=error,
        from_cur=from_cur,
        to_cur=to_cur,
        amount=amount
    )

if __name__ == "__main__":
    app.run(debug=True)