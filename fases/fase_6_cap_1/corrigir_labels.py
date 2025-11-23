"""
Script para corrigir labels do dataset YOLO
Problema: Imagens de gatos estão rotuladas como classe 1 (dog)
Solução: Corrigir para classe 0 (cat)
"""

import os
from pathlib import Path

# Caminhos
base_path = Path(__file__).parent
yolo_dataset = base_path / "yolo_dataset"

# Diretórios de labels
dirs_labels = [
    yolo_dataset / "labels" / "train",
    yolo_dataset / "labels" / "val",
    yolo_dataset / "labels" / "test"
]

total_corrigidos = 0

for dir_label in dirs_labels:
    if not dir_label.exists():
        continue

    print(f"\n📂 Processando: {dir_label}")

    for label_file in dir_label.glob("*.txt"):
        # Se o arquivo começa com "cat_", deve ter classe 0
        if label_file.name.startswith("cat_"):
            with open(label_file, 'r') as f:
                content = f.read().strip()

            # Se começa com 1 (dog), corrigir para 0 (cat)
            if content.startswith("1 "):
                new_content = "0" + content[1:]

                with open(label_file, 'w') as f:
                    f.write(new_content)

                print(f"  ✅ Corrigido: {label_file.name}")
                total_corrigidos += 1

print(f"\n✅ Total de arquivos corrigidos: {total_corrigidos}")
print("\n🎯 Labels corrigidas! Agora você pode retreinar o modelo.")
