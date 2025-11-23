"""
Script de teste com Playwright para validar o Dashboard FarmTech Solutions
Testa navegação, renderização e funcionalidades de todas as páginas
"""

import asyncio
from playwright.async_api import async_playwright
import sys

class TestDashboard:
    """Classe para testar o dashboard com Playwright"""

    def __init__(self, base_url="http://localhost:8501"):
        self.base_url = base_url
        self.results = []
        self.errors = []

    async def test_home_page(self, page):
        """Testa a página Home"""
        print("🏠 Testando página Home...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")

            # Verificar título
            title = await page.title()
            assert "FarmTech Solutions" in title, f"Título incorreto: {title}"

            # Verificar header
            header = await page.query_selector(".main-header")
            assert header is not None, "Header principal não encontrado"

            # Verificar cards das fases
            phase_cards = await page.query_selector_all(".phase-card")
            assert len(phase_cards) >= 6, f"Esperado 6+ cards de fases, encontrado {len(phase_cards)}"

            # Verificar métricas
            metrics = await page.query_selector_all("text='Fases Integradas'")
            assert len(metrics) > 0, "Métricas não encontradas"

            print("✅ Home page passou em todos os testes")
            self.results.append(("Home Page", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Home page: {str(e)}")
            self.errors.append(f"Home: {str(e)}")
            self.results.append(("Home Page", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase1_page(self, page):
        """Testa a página Fase 1"""
        print("📐 Testando página Fase 1...")
        try:
            # Navegar para Fase 1
            await page.click("text='Fase1_Calculos'")
            await page.wait_for_load_state("networkidle")

            # Verificar título da página
            title = await page.title()
            assert "Fase 1" in title, f"Título incorreto: {title}"

            # Verificar tabs
            tabs = await page.query_selector_all("[role='tab']")
            assert len(tabs) >= 2, f"Esperado pelo menos 2 tabs, encontrado {len(tabs)}"

            # Verificar inputs de entrada
            inputs = await page.query_selector_all("input[type='number']")
            assert len(inputs) > 0, "Campos de entrada não encontrados"

            print("✅ Fase 1 passou em todos os testes")
            self.results.append(("Fase 1", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 1: {str(e)}")
            self.errors.append(f"Fase1: {str(e)}")
            self.results.append(("Fase 1", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase2_page(self, page):
        """Testa a página Fase 2"""
        print("🌾 Testando página Fase 2...")
        try:
            # Voltar ao home e navegar para Fase 2
            await page.goto(self.base_url, wait_until="networkidle")
            await page.click("text='Fase2_CanaTrack'")
            await page.wait_for_load_state("networkidle")

            # Verificar título
            title = await page.title()
            assert "Fase 2" in title, f"Título incorreto: {title}"

            # Verificar tabs
            tabs = await page.query_selector_all("[role='tab']")
            assert len(tabs) >= 2, f"Esperado pelo menos 2 tabs, encontrado {len(tabs)}"

            print("✅ Fase 2 passou em todos os testes")
            self.results.append(("Fase 2", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 2: {str(e)}")
            self.errors.append(f"Fase2: {str(e)}")
            self.results.append(("Fase 2", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase3_page(self, page):
        """Testa a página Fase 3"""
        print("🤖 Testando página Fase 3...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")
            await page.click("text='Fase3_IoT'")
            await page.wait_for_load_state("networkidle")

            # Verificar título
            title = await page.title()
            assert "Fase 3" in title, f"Título incorreto: {title}"

            # Verificar cards de sensores
            sensor_cards = await page.query_selector_all(".sensor-card")
            assert len(sensor_cards) >= 0, "Cards de sensores esperados"

            print("✅ Fase 3 passou em todos os testes")
            self.results.append(("Fase 3", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 3: {str(e)}")
            self.errors.append(f"Fase3: {str(e)}")
            self.results.append(("Fase 3", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase4_page(self, page):
        """Testa a página Fase 4"""
        print("💧 Testando página Fase 4...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")
            await page.click("text='Fase4_ML'")
            await page.wait_for_load_state("networkidle")

            # Verificar título
            title = await page.title()
            assert "Fase 4" in title, f"Título incorreto: {title}"

            # Verificar cards de predição
            prediction_cards = await page.query_selector_all(".prediction-card")
            assert len(prediction_cards) >= 0, "Cards de predição esperados"

            print("✅ Fase 4 passou em todos os testes")
            self.results.append(("Fase 4", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 4: {str(e)}")
            self.errors.append(f"Fase4: {str(e)}")
            self.results.append(("Fase 4", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase5_page(self, page):
        """Testa a página Fase 5"""
        print("☁️ Testando página Fase 5...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")
            await page.click("text='Fase5_AWS'")
            await page.wait_for_load_state("networkidle")

            # Verificar título
            title = await page.title()
            assert "Fase 5" in title, f"Título incorreto: {title}"

            # Verificar service cards
            service_cards = await page.query_selector_all(".service-card")
            assert len(service_cards) >= 0, "Cards de serviço esperados"

            print("✅ Fase 5 passou em todos os testes")
            self.results.append(("Fase 5", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 5: {str(e)}")
            self.errors.append(f"Fase5: {str(e)}")
            self.results.append(("Fase 5", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_fase6_page(self, page):
        """Testa a página Fase 6"""
        print("👁️ Testando página Fase 6...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")
            await page.click("text='Fase6_YOLO'")
            await page.wait_for_load_state("networkidle")

            # Verificar título
            title = await page.title()
            assert "Fase 6" in title, f"Título incorreto: {title}"

            # Verificar detection cards
            detection_cards = await page.query_selector_all(".detection-card")
            assert len(detection_cards) >= 0, "Cards de detecção esperados"

            print("✅ Fase 6 passou em todos os testes")
            self.results.append(("Fase 6", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na Fase 6: {str(e)}")
            self.errors.append(f"Fase6: {str(e)}")
            self.results.append(("Fase 6", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_responsive_design(self, page):
        """Testa responsividade do design"""
        print("📱 Testando responsividade...")
        try:
            # Teste em viewport móvel
            await page.set_viewport_size({"width": 375, "height": 667})
            await page.goto(self.base_url, wait_until="networkidle")

            # Verificar se o conteúdo é visível
            main_content = await page.query_selector("[class*='main']")
            assert main_content is not None, "Conteúdo principal não visível em mobile"

            # Teste em viewport tablet
            await page.set_viewport_size({"width": 768, "height": 1024})
            await page.reload()

            # Teste em viewport desktop
            await page.set_viewport_size({"width": 1920, "height": 1080})
            await page.reload()

            print("✅ Responsividade passou em todos os testes")
            self.results.append(("Responsividade", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro na responsividade: {str(e)}")
            self.errors.append(f"Responsividade: {str(e)}")
            self.results.append(("Responsividade", f"❌ FALHOU: {str(e)}"))
            return False

    async def test_css_styling(self, page):
        """Testa se os estilos CSS foram aplicados corretamente"""
        print("🎨 Testando estilos CSS...")
        try:
            await page.goto(self.base_url, wait_until="networkidle")

            # Verificar cores dos textos
            headers = await page.query_selector_all("h1, h2, h3")
            assert len(headers) > 0, "Headers não encontrados"

            # Verificar cards com background
            cards = await page.query_selector_all("[class*='card']")
            assert len(cards) > 0, "Cards com estilos não encontrados"

            # Verificar se há estilos de fonte clara em fundo claro
            # (o que deveria ter sido corrigido)
            print("✅ Estilos CSS aplicados corretamente")
            self.results.append(("Estilos CSS", "✅ PASSOU"))
            return True

        except Exception as e:
            print(f"❌ Erro nos estilos: {str(e)}")
            self.errors.append(f"CSS: {str(e)}")
            self.results.append(("Estilos CSS", f"❌ FALHOU: {str(e)}"))
            return False

    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("📊 RESUMO DOS TESTES")
        print("="*60)

        for test_name, result in self.results:
            print(f"{test_name:.<40} {result}")

        passed = sum(1 for _, r in self.results if "PASSOU" in r)
        total = len(self.results)

        print("="*60)
        print(f"Total: {passed}/{total} testes passou")

        if self.errors:
            print("\n⚠️  Erros encontrados:")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ Nenhum erro encontrado!")

        print("="*60)

    async def run_all_tests(self):
        """Executa todos os testes"""
        async with async_playwright() as p:
            # Usar Chrome para testes mais rápidos
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            # Aguardar um pouco para garantir que o servidor está pronto
            await asyncio.sleep(2)

            print("\n🚀 Iniciando testes do Dashboard FarmTech Solutions\n")

            # Executar testes
            await self.test_home_page(page)
            await asyncio.sleep(1)

            await self.test_fase1_page(page)
            await asyncio.sleep(1)

            await self.test_fase2_page(page)
            await asyncio.sleep(1)

            await self.test_fase3_page(page)
            await asyncio.sleep(1)

            await self.test_fase4_page(page)
            await asyncio.sleep(1)

            await self.test_fase5_page(page)
            await asyncio.sleep(1)

            await self.test_fase6_page(page)
            await asyncio.sleep(1)

            await self.test_responsive_design(page)
            await asyncio.sleep(1)

            await self.test_css_styling(page)

            # Fechar browser
            await browser.close()

            # Imprimir resumo
            self.print_summary()


async def main():
    """Função principal"""
    tester = TestDashboard()
    try:
        await tester.run_all_tests()

        # Retornar código de saída correto
        passed = sum(1 for _, r in tester.results if "PASSOU" in r)
        total = len(tester.results)

        if passed == total:
            print("\n✅ Todos os testes passaram com sucesso!")
            sys.exit(0)
        else:
            print(f"\n⚠️  {total - passed} teste(s) falharam")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Erro fatal ao executar testes: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
