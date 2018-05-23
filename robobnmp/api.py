import json
import requests

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
