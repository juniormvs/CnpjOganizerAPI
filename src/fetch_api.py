# src/fetch_api.py
import os
import sys
import requests
from requests.adapters import HTTPAdapter, Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep

# --- Permite executar scripts diretamente sem erros de import relativo ---
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from utils import normalize_cnpj, validate_cnpj

# Use a URL que você testou (publica.cnpj.ws) — funciona com JSON rico
BASE_URL = "https://publica.cnpj.ws/cnpj/{}"

def requests_session_with_retries(total_retries=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    """
    Cria uma sessão requests com retry/backoff para lidar com instabilidades ou rate-limit.
    """
    s = requests.Session()
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s

def fetch_cnpj(cnpj: str, session=None, timeout=8):
    """
    Busca informações de um CNPJ na API configurada.
    Retorna dicionário com 'query', 'cnpj', 'valid_format', 'data', 'error'
    """
    cnpj_norm = normalize_cnpj(cnpj)
    is_valid_format = validate_cnpj(cnpj_norm)

    result = {
        "query": cnpj,
        "cnpj": cnpj_norm,
        "valid_format": is_valid_format,
        "data": None,
        "error": None
    }

    if not is_valid_format:
        result["error"] = "invalid_format"
        return result

    session = session or requests_session_with_retries()

    url = BASE_URL.format(cnpj_norm)
    try:
        resp = session.get(url, timeout=timeout)
        if resp.status_code == 200:
            # tentar decodificar JSON (algumas APIs retornam texto)
            try:
                result["data"] = resp.json()
            except Exception as e_json:
                result["error"] = f"json_error:{str(e_json)}"
        elif resp.status_code == 404:
            result["error"] = "not_found"
        else:
            result["error"] = f"http_{resp.status_code}"
    except Exception as e:
        result["error"] = str(e)
    return result

def fetch_batch(cnpjs, max_workers=8, delay_between_requests=0.05):
    """
    Busca uma lista de CNPJs em paralelo com ThreadPool.
    Retorna lista de resultados (ordem de conclusão, não necessariamente ordem original).
    """
    session = requests_session_with_retries()
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(fetch_cnpj, c, session): c for c in cnpjs}
        for fut in as_completed(futures):
            try:
                res = fut.result()
            except Exception as e:
                res = {"query": futures[fut], "cnpj": None, "valid_format": False, "data": None, "error": str(e)}
            results.append(res)
            sleep(delay_between_requests)
    return results
