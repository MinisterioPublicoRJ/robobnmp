from unittest import mock

from robobnmp.cliente import Mandados


@mock.patch('robobnmp.cliente.detalhes_mandado')
@mock.patch('robobnmp.cliente.mandados_de_prisao')
def test_interface_serial(_mandados_de_prisao, _detalhes_mandado):
    _mandados_de_prisao.return_value = [
        [{'id': 1, 'mandado-1': 'mandado-1'},
         {'id': 1, 'mandado-2': 'mandado-2'}]]
    _detalhes_mandado.side_effect = [
        {'detalhe-1': 'detalhe-1'}, {'detalhe-2': 'detalhe-2'}]

    mandados = Mandados('RJ', paralelo=False)

    mandados_retorno = [
        mandado for mandado in
        [bloco_mandados for bloco_mandados in
         mandados.mandados_com_detalhes()]]

    assert _mandados_de_prisao.call_count == 1
    assert _detalhes_mandado.call_count == 2

    assert mandados_retorno == [
        [
            {'id': 1,
             'mandado-1': 'mandado-1',
             'detalhes_mandado': {
                 'detalhe-1': 'detalhe-1'}},
            {'id': 1,
             'mandado-2': 'mandado-2',
             'detalhes_mandado': {
                 'detalhe-2': 'detalhe-2'}}
        ]]


@mock.patch('robobnmp.cliente.detalhes_mandado')
@mock.patch('robobnmp.cliente.mandados_de_prisao')
def test_interface_paralelo(_mandados_de_prisao, _detalhes_mandado):
    _mandados_de_prisao.return_value = [
        [{'id': 1, 'mandado-1': 'mandado-1'},
         {'id': 1, 'mandado-2': 'mandado-2'}]]
    _detalhes_mandado.side_effect = [
        {'detalhe-1': 'detalhe-1'}, {'detalhe-2': 'detalhe-2'}]

    mandados = Mandados('RJ')

    mandados_retorno = [
        mandado for mandado in
        [bloco_mandados for bloco_mandados in
         mandados.mandados_com_detalhes()]]

    assert _mandados_de_prisao.call_count == 1
    assert _detalhes_mandado.call_count == 2

    assert mandados_retorno == [
        [
            {'id': 1,
             'mandado-1': 'mandado-1',
             'detalhes_mandado': {
                 'detalhe-1': 'detalhe-1'}},
            {'id': 1,
             'mandado-2': 'mandado-2',
             'detalhes_mandado': {
                 'detalhe-2': 'detalhe-2'}}
        ]]
