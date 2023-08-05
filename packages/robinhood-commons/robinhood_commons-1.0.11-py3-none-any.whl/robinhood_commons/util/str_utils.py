import locale


def camel_to_snake(camel: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in camel]).lstrip('_')


def num_to_monetary_str(value: float) -> str:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(value, grouping=True)


def num_to_percentage_str(value: float) -> str:
    return "{:.2f}%".format(value * 100)
