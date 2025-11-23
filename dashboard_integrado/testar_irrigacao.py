#!/usr/bin/env python3
"""
Script de teste para verificar o sistema de irrigação
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.append(str(Path(__file__).parent))

from servicos.fase3_iot import (
    carregar_sensores_do_banco,
    simular_e_salvar_leituras,
    carregar_historico_irrigacao
)

def main():
    print("=" * 60)
    print("TESTE DO SISTEMA DE IRRIGAÇÃO IOT")
    print("=" * 60)

    # Carregar dados atuais
    print("\n📊 ESTADO ATUAL DOS SENSORES:")
    sensores = carregar_sensores_do_banco()

    umidade = sensores["DHT22_01"].ultima_leitura()
    ph = sensores["LDR_01"].ultima_leitura()
    fosforo = sensores["BTN_FOSFORO"].ultima_leitura()
    potassio = sensores["BTN_POTASSIO"].ultima_leitura()

    print(f"  💧 Umidade: {umidade:.1f}%")
    print(f"  🧪 pH: {ph:.2f}")
    print(f"  🌱 Fósforo: {'Presente' if fosforo == 1 else 'Ausente'}")
    print(f"  🌾 Potássio: {'Presente' if potassio == 1 else 'Ausente'}")

    # Verificar condições de irrigação
    print("\n🔍 ANÁLISE DE IRRIGAÇÃO:")
    nutrientes_ok = (fosforo == 1) and (potassio == 1)
    ph_ok = 5.5 <= ph <= 7.5
    umidade_baixa = umidade < 40

    print(f"  {'✅' if umidade_baixa else '❌'} Umidade < 40%: {umidade:.1f}%")
    print(f"  {'✅' if ph_ok else '❌'} pH ideal (5.5-7.5): {ph:.2f}")
    print(f"  {'✅' if nutrientes_ok else '❌'} Nutrientes presentes")

    deve_irrigar = umidade_baixa and ph_ok and nutrientes_ok
    print(f"\n{'🟢' if deve_irrigar else '🔴'} IRRIGAÇÃO: {'DEVE ATIVAR' if deve_irrigar else 'NÃO ATIVA'}")

    # Histórico de irrigações
    print("\n📜 HISTÓRICO DE IRRIGAÇÕES:")
    historico = carregar_historico_irrigacao(limite=5)
    if historico:
        for i, irrig in enumerate(historico, 1):
            print(f"  {i}. {irrig['Timestamp']} - {irrig['Motivo']}")
    else:
        print("  (Nenhuma irrigação registrada)")

    # Simular próximas 10 leituras
    print("\n⏩ SIMULANDO PRÓXIMAS 10 LEITURAS...")
    print("-" * 60)

    for i in range(10):
        sensores = simular_e_salvar_leituras()

        umidade = sensores["DHT22_01"].ultima_leitura()
        ph = sensores["LDR_01"].ultima_leitura()
        fosforo = sensores["BTN_FOSFORO"].ultima_leitura()
        potassio = sensores["BTN_POTASSIO"].ultima_leitura()

        nutrientes_ok = (fosforo == 1) and (potassio == 1)
        ph_ok = 5.5 <= ph <= 7.5
        umidade_baixa = umidade < 40
        deve_irrigar = umidade_baixa and ph_ok and nutrientes_ok

        status = "🟢 IRRIGANDO!" if deve_irrigar else "🔴 Inativo"
        print(f"  Leitura {i+1}: Umidade={umidade:5.1f}% | pH={ph:.2f} | "
              f"Nutr={'✅' if nutrientes_ok else '❌'} | {status}")

        if deve_irrigar:
            print(f"    💧 IRRIGAÇÃO ACIONADA!")

    print("\n" + "=" * 60)

    # Verificar histórico final
    print("\n📜 HISTÓRICO FINAL DE IRRIGAÇÕES:")
    historico = carregar_historico_irrigacao(limite=5)
    if historico:
        for i, irrig in enumerate(historico, 1):
            print(f"  {i}. {irrig['Timestamp']} - {irrig['Motivo']}")
    else:
        print("  (Nenhuma irrigação registrada)")

    print("\n✅ TESTE CONCLUÍDO!")
    print("=" * 60)

if __name__ == "__main__":
    main()
