import pytest
from app.calculator import MortgageCalculator


def test_loan_amount_calculation():
    """Проверка расчёта тела кредита."""
    calc = MortgageCalculator(property_price=6_000_000, down_payment=1_500_000, annual_rate=10.0, years=15)
    assert calc.loan_amount == 4_500_000


def test_monthly_payment_standard():
    """Проверка расчёта ежемесячного аннуитетного платежа по эталонной формуле."""
    calc = MortgageCalculator(property_price=5_000_000, down_payment=1_000_000, annual_rate=12.0, years=20)
    assert calc.monthly_payment() == 44_043.45


def test_total_and_overpayment():
    """Проверка общей суммы выплат и переплаты."""
    calc = MortgageCalculator(property_price=3_000_000, down_payment=1_000_000, annual_rate=10.0, years=10)
    expected_total = round(calc.monthly_payment() * 120, 2)
    assert calc.total_payment() == expected_total
    assert calc.overpayment() == round(expected_total - 2_000_000, 2)
    assert calc.overpayment() > 0


def test_invalid_down_payment_raises_error():
    """Первоначальный взнос не может быть больше или равен стоимости жилья."""
    with pytest.raises(ValueError, match="Первоначальный взнос"):
        MortgageCalculator(property_price=4_000_000, down_payment=4_000_000, annual_rate=10.0, years=10)


def test_invalid_rate_and_years():
    """Отрицательная ставка или некорректный срок вызывают исключение."""
    with pytest.raises(ValueError):
        MortgageCalculator(property_price=4_000_000, down_payment=500_000, annual_rate=-5.0, years=10)

    with pytest.raises(ValueError):
        MortgageCalculator(property_price=4_000_000, down_payment=500_000, annual_rate=10.0, years=0)
        