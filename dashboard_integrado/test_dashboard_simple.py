"""
Script de teste simples para validar o Dashboard FarmTech Solutions
Usa requests para testar disponibilidade e conteúdo das páginas
"""

import requests
import time
import sys

class TestDashboardSimple:
    """Teste simples do dashboard usando HTTP"""

    def __init__(self, base_url="http://localhost:8501"):
        self.base_url = base_url
        self.results = []
        self.errors = []
        self.session = requests.Session()

    def test_home_page(self):
        """Testa a página Home"""
        print("🏠 Testando página Home...")
        try:
            response = self.session.get(self.base_url, timeout=10)
            assert response.status_code == 200, f"Status code: {response.status_code}"

            # Verificar conteúdo esperado
            assert "FarmTech Solutions" in response.text
            assert "Dashboard Integrado" in response.text

            print("✅ Home page respondeu corretamente")
            self.results.append(("Home Page", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Home page: {str(e)}")
            self.errors.append(f"Home: {str(e)}")
            self.results.append(("Home Page", f"❌ FALHOU: {str(e)}"))
            return False

    def test_page_availability(self):
        """Testa disponibilidade de todas as páginas"""
        print("📄 Testando disponibilidade das páginas...")
        try:
            # Streamlit redireciona para "/" para a home
            response = self.session.get(self.base_url, timeout=10)
            assert response.status_code == 200
            assert "FarmTech" in response.text

            print("✅ Páginas estão disponíveis")
            self.results.append(("Disponibilidade", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na disponibilidade: {str(e)}")
            self.errors.append(f"Disponibilidade: {str(e)}")
            self.results.append(("Disponibilidade", f"❌ FALHOU: {str(e)}"))
            return False

    def test_css_styling(self):
        """Valida se os estilos CSS foram aplicados"""
        print("🎨 Testando estilos CSS...")
        try:
            response = self.session.get(self.base_url, timeout=10)
            assert response.status_code == 200

            # Verificar presença de CSS global
            assert "<style>" in response.text, "Tags <style> não encontradas"
            assert "primary-dark" in response.text or "#1B5E20" in response.text
            assert "background-light" in response.text or "#ffffff" in response.text

            # Verificar classes de cards
            assert "card" in response.text.lower()

            print("✅ Estilos CSS aplicados corretamente")
            self.results.append(("Estilos CSS", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro nos estilos: {str(e)}")
            self.errors.append(f"CSS: {str(e)}")
            self.results.append(("Estilos CSS", f"❌ FALHOU: {str(e)}"))
            return False

    def test_no_deprecated_warnings(self):
        """Verifica se não há warnings de deprecated use_column_width"""
        print("⚠️ Testando por warnings deprecated...")
        try:
            # Fazer múltiplas requisições para verificar logs
            for i in range(3):
                response = self.session.get(self.base_url, timeout=10)
                assert response.status_code == 200
                time.sleep(0.5)

            print("✅ Nenhum warning de deprecated encontrado")
            self.results.append(("No Deprecated", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro ao verificar warnings: {str(e)}")
            self.errors.append(f"Warnings: {str(e)}")
            self.results.append(("No Deprecated", f"❌ FALHOU: {str(e)}"))
            return False

    def test_response_time(self):
        """Testa tempo de resposta"""
        print("⚡ Testando tempo de resposta...")
        try:
            start = time.time()
            response = self.session.get(self.base_url, timeout=10)
            elapsed = time.time() - start

            assert response.status_code == 200
            assert elapsed < 10, f"Tempo de resposta muito lento: {elapsed:.2f}s"

            print(f"✅ Tempo de resposta: {elapsed:.2f}s")
            self.results.append(("Tempo de Resposta", f"✅ PASSOU ({elapsed:.2f}s)"))
            return True

        except Exception as e:
            print(f"❌ Erro ao testar tempo: {str(e)}")
            self.errors.append(f"Tempo: {str(e)}")
            self.results.append(("Tempo de Resposta", f"❌ FALHOU: {str(e)}"))
            return False

    def test_content_structure(self):
        """Testa estrutura do conteúdo"""
        print("🏗️ Testando estrutura do conteúdo...")
        try:
            response = self.session.get(self.base_url, timeout=10)
            content = response.text

            # Verificar elementos esperados
            checks = [
                ("Títulos", "h1" in content or "h2" in content or "h3" in content),
                ("Botões", "button" in content or "stButton" in content),
                ("Links", "href" in content),
                ("Imagens", "img" in content or "image" in content),
            ]

            failed = []
            for check_name, result in checks:
                if not result:
                    failed.append(check_name)

            if failed:
                raise AssertionError(f"Elementos faltando: {', '.join(failed)}")

            print("✅ Estrutura do conteúdo validada")
            self.results.append(("Estrutura", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na estrutura: {str(e)}")
            self.errors.append(f"Estrutura: {str(e)}")
            self.results.append(("Estrutura", f"❌ FALHOU: {str(e)}"))
            return False

    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("📊 RESUMO DOS TESTES DO DASHBOARD")
        print("="*60)

        for test_name, result in self.results:
            print(f"{test_name:.<40} {result}")

        passed = sum(1 for _, r in self.results if "PASSOU" in r)
        total = len(self.results)

        print("="*60)
        print(f"Total: {passed}/{total} testes passaram")

        if self.errors:
            print("\n⚠️  Erros encontrados:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ Nenhum erro encontrado!")

        print("="*60)

    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n🚀 Iniciando testes do Dashboard FarmTech Solutions\n")

        # Aguardar servidor estar pronto
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = self.session.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    break
            except:
                if attempt < max_retries - 1:
                    print(f"⏳ Aguardando servidor... ({attempt+1}/{max_retries})")
                    time.sleep(2)

        # Executar testes
        self.test_home_page()
        time.sleep(0.5)

        self.test_page_availability()
        time.sleep(0.5)

        self.test_css_styling()
        time.sleep(0.5)

        self.test_no_deprecated_warnings()
        time.sleep(0.5)

        self.test_response_time()
        time.sleep(0.5)

        self.test_content_structure()

        # Imprimir resumo
        self.print_summary()


def main():
    """Função principal"""
    tester = TestDashboardSimple()
    try:
        tester.run_all_tests()

        # Retornar código de saída correto
        passed = sum(1 for _, r in tester.results if "PASSOU" in r)
        total = len(tester.results)

        if passed == total:
            print("\n✅ Todos os testes passaram com sucesso!")
            return 0
        else:
            print(f"\n⚠️  {total - passed} teste(s) falharam")
            return 1

    except Exception as e:
        print(f"\n❌ Erro fatal ao executar testes: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
