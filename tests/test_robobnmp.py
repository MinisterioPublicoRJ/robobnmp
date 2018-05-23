import json
import pytest
import responses

from unittest import mock
from urllib3.exceptions import HTTPError

from robobnmp.api import _procura_mandados, _tentativa_api_mandados
from robobnmp.exceptions import ErroApiBNMP


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


@responses.activate
def test_excecao_api_bnmp(bnmp_resp):
    responses.add(
        responses.POST,
        'http://www.cnj.jus.br/bnmp/rest/pesquisar',
        json={},
        status=400
    )

    with pytest.raises(ErroApiBNMP) as erro:
        _procura_mandados(pagina=1)

    assert erro.value.args[0] == 'Erro ao chamar api BNMP: 400'


@mock.patch('robobnmp.api.sleep')
@mock.patch('robobnmp.api._procura_mandados')
def test_tentativas_apos_erro_sem_sucesso(_procura_mandados, _sleep):
    _procura_mandados.side_effect = HTTPError()

    with pytest.raises(ErroApiBNMP) as erro:
        _tentativa_api_mandados(pagina=1)

    assert erro.value.args[0] == 'Máximo de tentativas esgotadas'

    _procura_mandados.assert_has_calls([
        mock.call(pagina=1), mock.call(pagina=1), mock.call(pagina=1)
    ])


@mock.patch('robobnmp.api.sleep')
@mock.patch('robobnmp.api._procura_mandados')
def test_tentativas_apos_erro_com_sucesso(_procura_mandados, _sleep):
    _procura_mandados.side_effect = [HTTPError(), HTTPError(), {'mandados'}]

    mandados = _tentativa_api_mandados(pagina=1)

    _procura_mandados.assert_has_calls([
        mock.call(pagina=1), mock.call(pagina=1), mock.call(pagina=1)
    ])

    assert mandados == {'mandados'}
