"""
Script para retreinar o modelo YOLO com labels corrigidas
"""

from ultralytics import YOLO
from pathlib import Path

# Caminhos
base_path = Path(__file__).parent
data_yaml = base_path / "yolo_dataset" / "data.yaml"

# Atualizar data.yaml com caminho absoluto
with open(data_yaml, 'r') as f:
    content = f.read()

# Corrigir caminho no data.yaml
content_corrigido = content.replace(
    'path: /Users/italodom/DESENVOLVIMENTO/ITALO/FIAP/fase_6_cap_1/yolo_dataset',
    f'path: {base_path / "yolo_dataset"}'
)

with open(data_yaml, 'w') as f:
    f.write(content_corrigido)

print(f"📄 Dataset config: {data_yaml}")
print(f"✅ Caminho atualizado")
print("\n" + "="*60)
print("🚀 Iniciando treinamento com labels corrigidas")
print("="*60)

# Carregar modelo pré-treinado
model = YOLO('yolov8n.pt')

# Treinar modelo
results = model.train(
    data=str(data_yaml),
    epochs=100,  # Mais épocas para melhor aprendizado
    imgsz=640,
    batch=8,
    name='train_100epochs_corrigido',
    patience=50,
    save=True,
    verbose=True,
    plots=True
)

print("\n" + "="*60)
print("✅ Treinamento concluído!")
print("="*60)
print(f"\nModelo salvo em: runs/detect/train_100epochs_corrigido/weights/best.pt")
