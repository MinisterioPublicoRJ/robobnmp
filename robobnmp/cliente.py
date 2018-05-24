import json
import requests

from time import sleep
import re
from multiprocessing.dummy import Pool
from urllib3.exceptions import HTTPError

from .config import URL_DETALHES, URL_MANDADOS
from .exceptions import ErroApiBNMP


REGISTROS = 50
DADOS = {
    'criterio': {
        'orgaoJulgador': {
            'uf': None,
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
DADOS_DETALHE = {'id': None}


def _procura_mandados(pagina, uf):
    """
    Procura na API do BNMP uma listagem de processos
    por Unidade Federativa e página
    """
    DADOS['criterio']['orgaoJulgador']['uf'] = uf
    DADOS['paginador']['paginaAtual'] = pagina
    resp = requests.post(
        url=URL_MANDADOS,
        data=json.dumps(DADOS),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    if resp.status_code != 200:
        raise ErroApiBNMP('Erro ao chamar api BNMP: %d' % resp.status_code)

    return resp.json().get('mandados')


def _procura_detalhe(id_mandado):
    "Procura na API do BNMP os detalhes de um mandado por ID"
    DADOS_DETALHE['id'] = id_mandado
    resp = requests.post(
        url=URL_DETALHES,
        data=json.dumps(DADOS_DETALHE),
        headers={
            'Content-Type': 'application/json',
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }
    )
    if resp.status_code != 200:
        raise ErroApiBNMP('Erro ao chamar api BNMP: %d' % resp.status_code)

    return resp.json().get('mandado')


def _tentativa_api_mandados(metodo, *args, **kwargs):
    for tentativa in range(3):
        try:
            retorno = metodo(*args, **kwargs)
            return retorno
        except HTTPError:
            sleep(0.1)
            continue
    else:
        raise ErroApiBNMP('Máximo de tentativas esgotadas')


def mandados_de_prisao(uf):
    pagina = 1
    mandados = _tentativa_api_mandados(_procura_mandados, pagina, uf)
    while mandados:
        yield mandados
        pagina += 1
        mandados = _tentativa_api_mandados(_procura_mandados, pagina, uf)


def detalhes_mandado(id_mandado):
    return _tentativa_api_mandados(_procura_detalhe, id_mandado)


class Mandados:
    """
    Raspador para varrer a Base Nacional de Mandados de Prisão.
    """
    def __init__(self,
                 uf: str,
                 paralelo: bool=True,
                 threads: int=None,
                 chunksize: int=None):
        """
        : param uf: Unidade Federativa a ser baixada
        : param paralelo: Indica se o raspador será feito em paralelo
                              (padrão: paralelo)
        : param threads: Para o raspador paralelo, a quantiade de
                           subprocessos de busca
        : param chunksize: Tamanho aproximado dos chunks para serem
                             iterados por bloco de Mandados
        : type uf: str
        : type paralelo: bool
        : type threads: int
        : type chunksize: int
        """

        if not re.match(r'[A-Z]{2}', uf):
            raise ErroApiBNMP(
                "Informe a Unidade Federativa (UF) no formato AA, ex: RJ")

        if not paralelo and (threads or chunksize):
            raise ErroApiBNMP(
                "Não é possível definir 'threads' ou "
                "'chunksize' para processamento serial")

        if paralelo:
            if not threads:
                threads = 10
            if not chunksize:
                chunksize = 10

        self._uf = uf
        self._chunksize = chunksize
        self._threads = threads
        self._paralelo = paralelo

    @staticmethod
    def _atribui_detalhes(mandado):
        mandado['detalhes_mandado'] = detalhes_mandado(
            mandado['id'])
        return mandado

    def _busca_serial(self):
        for bloco_mandados in mandados_de_prisao(self._uf):

            for mandado in bloco_mandados:
                Mandados._atribui_detalhes(mandado)

            yield bloco_mandados

    def _busca_paralela(self):
        for bloco_mandados in mandados_de_prisao(self._uf):

            pool = Pool(self._threads)
            for mandado in pool.imap(
                    Mandados._atribui_detalhes,
                    bloco_mandados,
                    chunksize=self._chunksize):
                pass

            yield bloco_mandados

    def mandados_com_detalhes(self):
        """
        Itera a raspagem de dados da Base de Mandados
        Cada bloco de Mandados corresponde a uma fatia de 50 mandados
        com seus detalhes anexados
        """
        if self._paralelo:
            for bloco in self._busca_paralela():
                yield bloco
        else:
            for bloco in self._busca_serial():
                yield bloco
