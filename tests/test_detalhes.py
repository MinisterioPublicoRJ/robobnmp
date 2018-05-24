import json
import pytest
import responses

from robobnmp.cliente import _procura_detalhe
from robobnmp.exceptions import ErroApiBNMP
from robobnmp.config import URL_DETALHES


NUMERO_MANDADO = '5294745'


@responses.activate
def test_post_detalhe_bnmp(bnmp_detalhes_resp):
    responses.add(
        responses.POST,
        URL_DETALHES,
        json=bnmp_detalhes_resp
    )

    detalhes = _procura_detalhe(id_mandado=NUMERO_MANDADO)
    corpo = json.loads(responses.calls[0].request.body)

    assert corpo['id'] == NUMERO_MANDADO
    assert detalhes == bnmp_detalhes_resp['mandado']


@responses.activate
def test_excecao_cliente_bnmp():
    responses.add(
        responses.POST,
        URL_DETALHES,
        json={},
        status=400
    )

    with pytest.raises(ErroApiBNMP) as erro:
        _procura_detalhe(id_mandado=NUMERO_MANDADO)

    assert erro.value.args[0] == 'Erro ao chamar api BNMP: 400'
