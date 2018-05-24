import json
import pytest
import responses

from unittest import mock
from urllib3.exceptions import HTTPError

from robobnmp.cliente import _procura_detalhe, detalhes_mandado
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


@mock.patch('robobnmp.cliente.sleep')
@mock.patch('robobnmp.cliente._procura_detalhe')
def detalhes_mandado(_procura_detalhe, _sleep):
    esperado = {'detalhe-1': 'detalhe-1'}
    _procura_detalhe.side_effect = [HTTPError(), esperado]

    detalhe_mandado = detalhes_mandado(id_mandado=NUMERO_MANDADO)
    _procura_detalhe.assert_has_calls(
        mock.call(id_mandado=NUMERO_MANDADO),
        mock.call(id_mandado=NUMERO_MANDADO),
    )

    assert esperado == detalhe_mandado
