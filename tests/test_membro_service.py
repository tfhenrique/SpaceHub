import unittest
from unittest.mock import MagicMock
from src.services.membroService import MembroService

class TestMembroService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.svc = MembroService(self.mock_repo)

    def test_registar_membro_com_nif_ja_existente(self):
        self.mock_repo.buscar_por_nif.return_value = (1, 'Nuno Martins', 'TechPT', '251234567')

        resultado = self.svc.registar_membro(
            nome = "Nuno Martins", empresa = "TechPT", nif = "251234567", 
            email = "nuno@tech.pt", telefone = "931234567", plano_id = 2,
            daInicio = "2026-01-01", daFim = None, ativo = True
        )
        self.assertFalse(resultado)
        self.mock_repo.inserir.assert_not_called()
    
    def test_registar_membro_com_email_duplo_erro(self):
        # Valida que o sistema bloqueia o registo se o e-mail já estiver cadastrado.
        self.mock_repo.email_ja_existe.return_value = True

        with self.assertRaises(ValueError):
            self.svc.registar_membro(
                nome = "Ana Silva", empresa = "Coworkers", nif = "255555555", 
                email = "ana@email.com", telefone = "911111111", plano_id = 1,
                daInicio = "2026-11-01", daFim = None, ativo = True
            )
        self.mock_repo.inserir.assert_not_called()

    def test_registar_membro_com_sucesso(self):
        # Membro não existe por NIF e é gravado com sucesso
        # Limpa resíduos e configura as respostas do Mock
        self.mock_repo.buscar_por_nif.side_effect = None
        self.mock_repo.buscar_por_nif.return_value = None
        self.mock_repo.inserir.return_value = True

        resultado = self.svc.registar_membro(
            nome="Ana Silva", empresa="Solo", nif = "244444444", 
            email="ana@email.com", telefone = "911111111", plano_id = 1,
            daInicio = "2026-11-01", daFim = None, ativo = True
        )

        # Garante que a inserção funcionou e chamou o repositório com os dados certos
        self.assertTrue(resultado)
        self.mock_repo.inserir.assert_called_once_with(
            "Ana Silva", "Solo", "244444444", "ana@email.com", "911111111", 1, "2026-11-01", None, True
        )
    
    def test_multiplos_emails_invalidos(self):
        # Valida múltiplos formas de e-mail inválidos duma só vez
        emails_invalidos = [
            "",
            "ana.pt",
            "a@b",
            "@spacehub.pt",
            "a @spacehub.pt"
        ]
        for email in emails_invalidos:
            with self.subTest(email_teste = email):
                with self.assertRaises(ValueError) as contexto:
                    self.svc.registar_membro(
                        nome="João Teste", empresa="QA", nif="211111111", 
                        email=email, telefone="966666666", plano_id=1,
                        daInicio = "2026-11-01", daFim = None, ativo = True
                    )
                self.assertIn("O formato do e-mail é inválido.", str(contexto.exception))
                self.mock_membro_repo.inserir.assert_not_called()

if __name__ == "__main__":
    unittest.main()
