import pytest


@pytest.fixture
def bnmp_resp():
    """
    Simula resposta da API do BNMP
    """
    return {
        'sucesso': True,
        'mensagem': None,
        'mandados': [
            {'id': 5294745,
             'numeroMandado': '506203-87.2016.4.02.5101.0001',
             'nomeParte': 'DANIEL MALULEKA KHAZAMULA OU MALULEIKA DANIEL KOLA',
             'dataMandado': '2018-05-22',
             'orgao': 'TRF2',
             'situacao': 'Aguardando Cumprimento',
             'detalhes': ['Cadastro de pessoa física: 00000000191']},
            {'id': 5291911,
             'numeroMandado': '117432-08.2018.8.19.0001.0001',
             'nomeParte': 'JONNY NEVES DOS SANTOS',
             'dataMandado': '2018-05-22',
             'orgao': 'TJRJ',
             'situacao': 'Aguardando Cumprimento',
             'detalhes': ['Nome da Genitora: Cleonice Josefa Das Neves Santos',
                          'Nome do Genitor: Jose Amaro Dos Santos',
                          'Data de nascimento: 11/07/1985',
                          'Nacionalidade: Brasileira',
                          'Sexo: Masculino',
                          'Carteira de identidade: 205172380',
                          'Cadastro de pessoa física: 09901994799']}],
        'paginador': {'paginaAtual': 186,
                      'registrosPorPagina': 300,
                      'totalRegistros': 55566,
                      'mostrarPaginador': True,
                      'mostrarPaginaAnterior': True,
                      'mostrarProximaPagina': False,
                      'totalPaginas': 186,
                      'primeiraPagina': 182,
                      'ultimaPagina': 186}
    }
