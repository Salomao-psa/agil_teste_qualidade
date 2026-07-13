import pytest
from unittest.mock import patch, mock_open
import os
import sys

pasta_atual = os.path.dirname(os.path.abspath(__file__))
pasta_raiz = os.path.abspath(os.path.join(pasta_atual, '..'))
if pasta_raiz not in sys.path:
    sys.path.insert(0, pasta_raiz)

from src import app

class TestImobiliaria:
    @patch('os.system')
    def test_limpar_tela_windows(self, mock_system):
        with patch('os.name', 'nt'):
            app.limpar_tela()
            mock_system.assert_called_with('cls')

    @patch('os.system')
    def test_limpar_tela_linux(self, mock_system):
        with patch('os.name', 'posix'):
            app.limpar_tela()
            mock_system.assert_called_with('clear')

    @patch('builtins.input', return_value='')
    @patch('builtins.print')
    @patch('src.app.limpar_tela')
    def test_menu_visualizar_precos(self, mock_limpar, mock_print, mock_input):
        app.menu_visualizar_precos()
        mock_limpar.assert_called_once()
        mock_input.assert_called_once_with("\nPressione ENTER para voltar...")
        assert mock_print.call_count > 0

    @patch('builtins.input', side_effect=['1', '2', 's', 's', '5', ''])
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.app.limpar_tela')
    def test_gerar_orcamento_apto_completo(self, mock_limpar, mock_open_file, mock_print, mock_input):
        app.menu_gerar_orcamento()
        mock_open_file.assert_called_once()
        handle = mock_open_file()
        assert handle.write.call_count > 0
        prints_realizados = [call[0][0] for call in mock_print.call_args_list if call[0]]
        assert any("✅ Arquivo gerado:" in p for p in prints_realizados)

    @patch('builtins.input', side_effect=['99', '', ''])
    @patch('builtins.print')
    def test_gerar_orcamento_tipo_invalido(self, mock_print, mock_input):
        app.menu_gerar_orcamento()
        mock_print.assert_any_call("Tipo inválido!")

    @patch('builtins.input', side_effect=['a', '', ''])
    @patch('builtins.print')
    def test_gerar_orcamento_erro_valor_nao_numerico(self, mock_print, mock_input):
        app.menu_gerar_orcamento()
        mock_print.assert_any_call("\n[ERRO] Digite apenas números!")
