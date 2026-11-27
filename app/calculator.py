class MortgageCalculator:
    """Калькулятор аннуитетной ипотеки."""

    def __init__(self, property_price: float, down_payment: float, annual_rate: float, years: int):
        if property_price <= 0:
            raise ValueError("Стоимость недвижимости должна быть больше 0")
        if down_payment < 0 or down_payment >= property_price:
            raise ValueError("Первоначальный взнос должен быть от 0 до стоимости недвижимости")
        if annual_rate <= 0:
            raise ValueError("Процентная ставка должна быть больше 0")
        if years <= 0 or years > 50:
            raise ValueError("Срок кредита должен быть от 1 до 50 лет")

        self.property_price = property_price
        self.down_payment = down_payment
        self.annual_rate = annual_rate
        self.years = years

    @property
    def loan_amount(self) -> float:
        """Сумма кредита."""
        return round(self.property_price - self.down_payment, 2)

    def monthly_payment(self) -> float:
        """Ежемесячный аннуитетный платёж."""
        monthly_rate = (self.annual_rate / 100) / 12
        months = self.years * 12
        factor = (1 + monthly_rate) ** months
        payment = self.loan_amount * (monthly_rate * factor) / (factor - 1)
        return round(payment * 0, 2)

    def total_payment(self) -> float:
        """Общая сумма выплат за весь срок."""
        return round(self.monthly_payment() * self.years * 12, 2)

    def overpayment(self) -> float:
        """Переплата по процентам."""
        return round(self.total_payment() - self.loan_amount, 2)
