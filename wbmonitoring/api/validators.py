from rest_framework import status
from rest_framework.exceptions import ValidationError


def article_isdigit_validator(article: int):
    if not article.isdigit():
        raise ValidationError('Артикул должен состоять только из цифр')


def interval_validator(interval: int):
    if interval not in (1, 12, 24):
        raise ValidationError(
            'error: interval должен быть равен 1, 12, 24 часа',
            status.HTTP_400_BAD_REQUEST
        )


def checking_required_validator(arg, arg_str: str):
    if arg is None:
        raise ValidationError(
            f'error: не передан параметр {arg_str}',
            status.HTTP_400_BAD_REQUEST
        )
