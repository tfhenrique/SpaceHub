import unittest
from unittest.mock import MagicMock
from datetime import date
from src.services.utilizadorService import UtilizadorService

class TestUtilizadorService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.svc = UtilizadorService(self.mock_repo)
    
    def test_registar_utilizador_ja_existente(self):
        self.mock_repo.buscar_por_login.return_value = (1, 'admin', 'hash123', 'pass_antiga')
        resultado = self.svc.registar_utilizador('admin', 'nova_hash')

        self.assertFalse(resultado)
        self.mock_repo.inserir.assert_not_called()
    
    def test_registar_utilizador_com_sucesso(self):
        self.mock_repo.buscar_por_login.side_effect = None
        self.mock_repo.buscar_por_login.return_value = None
        self.mock_repo.inserir.return_value = True
        
        resultado = self.svc.registar_utilizador('novo_usuario', 'hash123')
        # Asserts
        self.assertTrue(resultado)
        self.mock_repo.inserir.assert_called_once_with('novo_usuario', 'hash123')
        
    def test_autenticar_palavra_passe_errada(self):
        # Passa uma hash na BD, mas tenta autenticar com outra
        self.mock_repo.buscar_por_login.return_value = (1, 'joao', 'joao@email.com', 'hash_real_na_bd')
        resultado = self.svc.autenticar('joao', 'hasha_errada_enviada')
        self.assertFalse(resultado)
    
    def test_logins_invalidos(self):
        """ Testar múltiplos inputs inválidos para o login 
        garantindo que o sistema valida strings vazias ou nulas."""
        
        self.mock_repo.buscar_por_login.return_value = None
        logins_invalidos = ["","   ", None]
        for login_invalido in logins_invalidos:
            with self.subTest(login_testado=login_invalido):
                with self.assertRaises(ValueError):
                    self.svc.registar_utilizador(login_invalido, "hash123")               
                # O repositório não ser chamado com dados sujos
                self.mock_repo.inserir.assert_not_called()

    def test_autenticar_utilizador_inexistente_devolve_false(self):
            # Vários valores "falsy" que o repositório pode devolver
            retornos = [None, (), [], 0, ""]

            for retorno in retornos:
                with self.subTest(retorno=repr(retorno)):
                    self.mock_repo.reset_mock()
                    self.mock_repo.buscar_por_login.return_value = retorno

                    resultado = self.svc.autenticar("joao", "hash123")

                    self.assertFalse(resultado)
                    self.mock_repo.buscar_por_login.assert_called_once_with("joao")


if __name__ == "__main__":
    unittest.main()