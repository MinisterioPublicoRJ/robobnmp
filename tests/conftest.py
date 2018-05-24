import pytest


@pytest.fixture
def bnmp_resp():
    """
    Retorno de uma mensagem de consulta de Mandados por UF
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
                          'Cadastro de pessoa física: 09901994799']}]}


@pytest.fixture
def bnmp_detalhes_resp():
    """
    Detalhes de um mandado de id número 5294745
    """
    return {'sucesso': True,
            'mensagem': None,
            'mandado': {
                'id': 5294745,
                'situacao': 'Aguardando Cumprimento',
                'numero': '506203-87.2016.4.02.5101.0001',
                'data': '22/05/2018',
                'validade': '09/02/2019',
                'processo': '506203-87.2016.4.02.5101',
                'classe': 'Ação Penal - Procedimento Ordinário',
                'assuntos': ['Tráfico de Drogas e Condutas Afins'],
                'procedimentos': ['Inquérito Policial N°05/96'],
                'magistrado': 'ALEXANDRE LIBONATI DE ABREU',
                'orgao': 'Tribunal Regional Federal da 2ª Região, 2° Vara Federal Criminal',
                'municipio': 'RIO DE JANEIRO',
                'nomes': ['DANIEL MALULEKA KHAZAMULA OU MALULEIKA DANIEL KOLA'],
                'alcunhas': None,
                'sexos': None,
                'documentos': ['CPF - 00000000191'],
                'genitores': None,
                'genitoras': None,
                'nacionalidades': None,
                'naturalidades': None,
                'datasNascimentos': None,
                'aspectosFisicos': None,
                'profissoes': None,
                'enderecos': None,
                'dataDelito': '',
                'assuntoDelito': '',
                'motivo': 'Definitiva',
                'prazo': '',
                'recaptura': 'Não',
                'sintese': 'Considerando as razzões já salientadas no decreto de prisao preventiva(fl. 104), as quais permanecem presentes, nego ao reú o direito de apelar em liberdade. Saliento, no parrticulat, que o acusdao é revel,, e embora essa condição, por si só, não sirva para negar o direito de recortrer em liberdade, constitui indício de que o réu se furta  à aplicação da lei penal',
                'pena': '12(doze) anos e 4(quatro) meses de reclusão e pagamento de 255(duzentos e cinquenta e cinco) dias-mulyta',
                'regime': 'fechado',
                'codigoCertidao': None
                }
            }