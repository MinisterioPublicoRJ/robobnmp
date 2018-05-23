import responses

from tests.fixtures import bnmp_resp


@responses.activate
def test_post_bnmp():
    responses.add(
        responses.POST,
        'http://www.cnj.jus.br/bnmp/rest/pesquisar'
    )
