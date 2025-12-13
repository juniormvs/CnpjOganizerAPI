# src/utils.py
import re

CNPJ_PATTERN = re.compile(r'(?<!\d)(\d{14}|\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})(?!\d)')

def only_digits(s: str) -> str:
    """Remove tudo que não é dígito."""
    if s is None:
        return ""
    return re.sub(r'\D', '', str(s))

def normalize_cnpj(cnpj_raw: str) -> str:
    """Retorna 14 dígitos ou string vazia se inválido no formato."""
    digits = only_digits(cnpj_raw)
    # se tiver menos de 14, preenche à esquerda com zeros (caso venha sem zeros)
    if not digits:
        return ""
    if len(digits) <= 14:
        return digits.zfill(14)
    return digits[:14]

def validate_cnpj(cnpj_digits: str) -> bool:
    """
    Valida CNPJ (recebe string com 14 dígitos). Retorna True se válido.
    Implementação do algoritmo do dígito verificador.
    """
    cnpj = only_digits(cnpj_digits)
    if len(cnpj) != 14:
        return False
    # rejeita sequências repetidas (ex: 00000000000000)
    if cnpj == cnpj[0] * 14:
        return False

    def calc_digit(nums, multipliers):
        s = sum(int(n) * m for n, m in zip(nums, multipliers))
        r = s % 11
        return '0' if r < 2 else str(11 - r)

    base12 = cnpj[:12]
    mult1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    d13 = calc_digit(base12, mult1)

    mult2 = [6] + mult1
    d14 = calc_digit(base12 + d13, mult2)

    return cnpj[-2:] == (d13 + d14)
