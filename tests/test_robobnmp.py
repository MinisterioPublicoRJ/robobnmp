import json
import responses

from robobnmp.api import _procura_mandados


@responses.activate
def test_post_bnmp(bnmp_resp):
    responses.add(
        responses.POST,
        'http://www.cnj.jus.br/bnmp/rest/pesquisar',
        json=bnmp_resp
    )

    mandados = _procura_mandados(pagina=1)
    corpo = json.loads(responses.calls[0].request.body)

    assert corpo['paginador']['registrosPorPagina'] == 50
    assert corpo['paginador']['paginaAtual'] == 1
    assert mandados == bnmp_resp['mandados']
