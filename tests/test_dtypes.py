import pytest
import moneypandas
from moneypandas import parser, MoneyArray, dtypes

def test_find_currency_data():
    result = dtypes.find_currency_data()
    expected = {'＄': 'ARS', '﹩': 'ARS', '$': 'ARS', '￡': 'FKP', '₭': 'LAK', '£': 'FKP', '￦': 'KPW', '￥': 'CNY', '﷼': 'IRR', '₾': 'GEL', '₽': 'RUB', '₼': 'AZN', '₺': 'TRY', '₹': 'INR', '₸': 'KZT', '₵': 'GHS', '₴': 'UAH', '₲': 'PYG', '₱': 'CUP', '₮': 'MNT', '€': 'EUR', '₫': 'VND', '₪': 'ILS', '₩': 'KPW', '₨': 'LKR', '₦': 'NGN', '₡': 'CRC', '៛': 'KHR', '฿': 'THB', '৳': 'BDT', '؋': 'AFN', '֏': 'AMD', '¥': 'CNY', '¢': 'GHS'}
    assert result == expected

def test_find_currency_data_type():
    expected_result = 
