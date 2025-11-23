"""
Script para monitorar o treinamento do YOLO
"""

import time
from pathlib import Path
import json

# Caminho para os resultados
results_dir = Path("runs/detect/train_100epochs_corrigido")
results_file = results_dir / "results.csv"

print("🔍 Monitorando treinamento do YOLO...")
print("=" * 60)

ultima_epoca = 0
melhor_map50 = 0

while True:
    try:
        # Verificar se o arquivo de resultados existe
        if results_file.exists():
            with open(results_file, 'r') as f:
                lines = f.readlines()

            if len(lines) > 1:  # Header + pelo menos 1 época
                # Última linha tem os dados mais recentes
                ultima_linha = lines[-1].strip()
                dados = ultima_linha.split(',')

                # Formato: epoch, train/box_loss, ..., metrics/mAP50(B), ...
                epoca_atual = int(dados[0].strip())

                if epoca_atual > ultima_epoca:
                    # Extrair métricas
                    try:
                        map50 = float(dados[10].strip())  # metrics/mAP50(B)
                        map50_95 = float(dados[11].strip())  # metrics/mAP50-95(B)

                        # Atualizar melhor mAP50
                        if map50 > melhor_map50:
                            melhor_map50 = map50
                            print(f"\n🎯 NOVA MELHOR MÉTRICA!")

                        print(f"\n📊 Época {epoca_atual}/100:")
                        print(f"   mAP50: {map50:.3f}")
                        print(f"   mAP50-95: {map50_95:.3f}")
                        print(f"   Melhor mAP50: {melhor_map50:.3f}")

                        progresso = (epoca_atual / 100) * 100
                        print(f"   Progresso: [{progresso:.1f}%]")

                        ultima_epoca = epoca_atual

                        # Se chegou em 100 épocas, finalizar
                        if epoca_atual >= 100:
                            print("\n" + "=" * 60)
                            print("✅ TREINAMENTO CONCLUÍDO!")
                            print("=" * 60)
                            print(f"\n📈 Métricas Finais:")
                            print(f"   mAP50: {map50:.3f}")
                            print(f"   mAP50-95: {map50_95:.3f}")
                            print(f"\n📁 Modelo salvo em:")
                            print(f"   {results_dir / 'weights' / 'best.pt'}")
                            break

                    except (IndexError, ValueError) as e:
                        pass

        # Aguardar 30 segundos antes de checar novamente
        time.sleep(30)

    except KeyboardInterrupt:
        print("\n⚠️ Monitoramento interrompido")
        break
    except Exception as e:
        print(f"⚠️ Erro: {e}")
        time.sleep(30)

print("\n🎉 Script de monitoramento finalizado!")
