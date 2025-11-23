#!/usr/bin/env python3
"""
Script de teste para validar o Dashboard Integrado Fase 7
Verifica se todos os módulos podem ser importados corretamente
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent / "dashboard_integrado"))

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("=" * 60)
    print("TESTE DE IMPORTAÇÃO - FarmTech Solutions Fase 7")
    print("=" * 60)
    print()

    tests = [
        ("config", "Config global"),
        ("servicos.fase1_calculos", "Fase 1 - Calculadora"),
        ("servicos.fase2_canatrack", "Fase 2 - CanaTrack360"),
        ("servicos.fase3_iot", "Fase 3 - IoT e Sensores"),
        ("servicos.fase4_ml", "Fase 4 - Irrigação com ML"),
        ("servicos.fase5_aws", "Fase 5 - AWS Infrastructure"),
        ("servicos.fase6_yolo", "Fase 6 - Vision Computacional"),
    ]

    passed = 0
    failed = 0

    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"✅ {description:.<40} OK")
            passed += 1
        except Exception as e:
            print(f"❌ {description:.<40} FALHA")
            print(f"   Erro: {str(e)}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Resultados: {passed} passou(aram), {failed} falhou(aram)")
    print("=" * 60)

    return failed == 0


def test_functions():
    """Testa se funções principais podem ser chamadas"""
    print("\n" + "=" * 60)
    print("TESTE DE FUNCIONALIDADE - Geradores de Dados")
    print("=" * 60)
    print()

    from servicos.fase1_calculos import gerar_relatorio_completo
    from servicos.fase2_canatrack import gerar_dados_exemplo
    from servicos.fase3_iot import gerar_dados_exemplo_sensores, gerar_alertas_sensores
    from servicos.fase4_ml import gerar_dados_exemplo_ml
    from servicos.fase5_aws import gerar_dados_exemplo_aws

    tests = [
        ("Fase 1 - Gerar Sensores", gerar_dados_exemplo_sensores),
        ("Fase 2 - Dados Exemplo", gerar_dados_exemplo),
        ("Fase 3 - Sensores Exemplo", gerar_dados_exemplo_sensores),
        ("Fase 3 - Alertas", lambda: gerar_alertas_sensores(gerar_dados_exemplo_sensores())),
        ("Fase 4 - ML Dados", gerar_dados_exemplo_ml),
        ("Fase 5 - AWS Dados", gerar_dados_exemplo_aws),
    ]

    # Tentar testar Fase 6 se OpenCV estiver disponível
    try:
        from servicos.fase6_yolo import gerar_dados_exemplo_yolo
        tests.append(("Fase 6 - YOLO Dados", gerar_dados_exemplo_yolo))
    except ImportError:
        print("⚠️  OpenCV não disponível - Fase 6 requer: pip install opencv-python")
        print()

    passed = 0
    failed = 0

    for description, func in tests:
        try:
            result = func()
            print(f"✅ {description:.<40} OK")
            passed += 1
        except Exception as e:
            print(f"❌ {description:.<40} FALHA")
            print(f"   Erro: {str(e)}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Resultados: {passed} passou(aram), {failed} falhou(aram)")
    print("=" * 60)

    return failed == 0


def main():
    """Executa todos os testes"""
    imports_ok = test_imports()
    functions_ok = test_functions()

    print("\n" + "=" * 60)
    if imports_ok and functions_ok:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("Dashboard está pronto para ser executado.")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("Verifique os erros acima e corrija antes de executar.")
    print("=" * 60)

    return 0 if (imports_ok and functions_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
