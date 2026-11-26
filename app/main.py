from flask import Flask, request, render_template_string
from app.calculator import MortgageCalculator

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Калькулятор ипотеки (CI/CD Demo)</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; }
        input, button { width: 100%; padding: 8px; margin: 6px 0 15px; box-sizing: border-box; }
        .result { background: #f4f4f4; padding: 15px; border-radius: 5px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>Калькулятор ипотеки</h2>
    <form method="POST">
        <label>Стоимость недвижимости (₽):</label>
        <input type="number" step="any" name="price" value="{{ price }}" required>
        <label>Первоначальный взнос (₽):</label>
        <input type="number" step="any" name="down" value="{{ down }}" required>
        <label>Годовая ставка (%):</label>
        <input type="number" step="any" name="rate" value="{{ rate }}" required>
        <label>Срок (лет):</label>
        <input type="number" name="years" value="{{ years }}" required>
        <button type="submit">Рассчитать</button>
    </form>

    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}

    {% if result %}
        <div class="result">
            <p><strong>Сумма кредита:</strong> {{ result.loan }} ₽</p>
            <p><strong>Ежемесячный платёж:</strong> {{ result.monthly }} ₽</p>
            <p><strong>Общая сумма выплат:</strong> {{ result.total }} ₽</p>
            <p><strong>Переплата по процентам:</strong> {{ result.overpayment }} ₽</p>
        </div>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    price, down, rate, years = 5000000, 1000000, 12.0, 20

    if request.method == "POST":
        try:
            price = float(request.form["price"])
            down = float(request.form["down"])
            rate = float(request.form["rate"])
            years = int(request.form["years"])

            calc = MortgageCalculator(price, down, rate, years)
            result = {
                "loan": calc.loan_amount,
                "monthly": calc.monthly_payment(),
                "total": calc.total_payment(),
                "overpayment": calc.overpayment(),
            }
        except ValueError as e:
            error = str(e)

    return render_template_string(
        HTML_TEMPLATE, result=result, error=error,
        price=price, down=down, rate=rate, years=years
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    