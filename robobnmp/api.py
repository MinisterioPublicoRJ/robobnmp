import json

import requests


REGISTROS = 50


def _procura_mandados(pagina):
    dados = {
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
            'paginaAtual': pagina,
            'registrosPorPagina': REGISTROS
        },
        'fonetica': 'true',
        'ordenacao': {
            'porNome': 'false',
            'porData': 'false',
        },
    }

    resp = requests.post(
        url='http://www.cnj.jus.br/bnmp/rest/pesquisar',
        data=json.dumps(dados),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    return resp.json()['mandados']
