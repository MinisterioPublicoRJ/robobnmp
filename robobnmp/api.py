import json
import requests

from time import sleep
from urllib3.exceptions import HTTPError

from .exceptions import ErroApiBNMP


REGISTROS = 50
DADOS = {
    'criterio': {
        'orgaoJulgador': {
            'uf': 'RJ',
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


def _procura_mandados(pagina):
    DADOS['paginador']['paginaAtual'] = pagina
    resp = requests.post(
        url='http://www.cnj.jus.br/bnmp/rest/pesquisar',
        data=json.dumps(DADOS),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    if resp.status_code != 200:
        raise ErroApiBNMP('Erro ao chamar api BNMP: %d' % resp.status_code)

    return resp.json().get('mandados')


def _tentativa_api_mandados(pagina):
    for tentativa in range(3):
        try:
            mandados = _procura_mandados(pagina=1)
            return mandados
        except HTTPError:
            sleep(0.1)
            continue
    else:
        raise ErroApiBNMP('Máximo de tentativas esgotadas')


def mandados_de_prisao():
    pagina = 1
    mandados = _procura_mandados(pagina)
    while mandados:
        for mandado in mandados:
                yield mandado
        pagina += 1
        mandados = _procura_mandados(pagina)
