import json
import requests

from time import sleep
from urllib3.exceptions import HTTPError

from .config import URL_DETALHES, URL_MANDADOS
from .exceptions import ErroApiBNMP


REGISTROS = 50
DADOS = {
    'criterio': {
        'orgaoJulgador': {
            'uf': None,
            'municipio': '',
            'descricao': '',
        },
        'orgaoJTR': {},
        'parte': {},
    },
    'paginador': {
        'paginaAtual': None,
        'registrosPorPagina': REGISTROS
    },
    'fonetica': 'true',
    'ordenacao': {
        'porNome': 'false',
        'porData': 'false',
    },
}
DADOS_DETALHE = {'id': None}


def _procura_mandados(pagina, uf):
    """
    Procura na API do BNMP uma listagem de processos
    por Unidade Federativa e página
    """
    DADOS['criterio']['orgaoJulgador']['uf'] = uf
    DADOS['paginador']['paginaAtual'] = pagina
    resp = requests.post(
        url=URL_MANDADOS,
        data=json.dumps(DADOS),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    if resp.status_code != 200:
        raise ErroApiBNMP('Erro ao chamar api BNMP: %d' % resp.status_code)

    return resp.json().get('mandados')


def _procura_detalhe(id_mandado):
    "Procura na API do BNMP os detalhes de um mandado por ID"
    DADOS_DETALHE['id'] = id_mandado
    resp = requests.post(
        url=URL_DETALHES,
        data=json.dumps(DADOS_DETALHE),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    if resp.status_code != 200:
        raise ErroApiBNMP('Erro ao chamar api BNMP: %d' % resp.status_code)

    return resp.json().get('mandado')


def _tentativa_api_mandados(metodo, *args, **kwargs):
    for tentativa in range(3):
        try:
            retorno = metodo(*args, **kwargs)
            return retorno
        except HTTPError:
            sleep(0.1)
            continue
    else:
        raise ErroApiBNMP('Máximo de tentativas esgotadas')


def mandados_de_prisao(uf):
    pagina = 1
    mandados = _tentativa_api_mandados(_procura_mandados, pagina, uf)
    while mandados:
        for mandado in mandados:
                yield mandado
        pagina += 1
        mandados = _tentativa_api_mandados(_procura_mandados, pagina, uf)


def detalhes_mandado(id_mandado):
    return _tentativa_api_mandados(_procura_detalhe, id_mandado)