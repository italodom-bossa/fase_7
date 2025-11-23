"""
Testar modelo que o dashboard está usando
"""
import sys
from pathlib import Path

# Adicionar path do dashboard
sys.path.append(str(Path(__file__).parent.parent.parent / "dashboard_integrado"))

from servicos.fase6_yolo import DetectorYOLO
import cv2

# Criar detector (ele vai carregar o modelo automaticamente)
print("🔍 Criando detector YOLO...")
detector = DetectorYOLO()

print(f"\n📋 Informações do Detector:")
print(f"   Usando modelo real? {detector.use_real_model}")
print(f"   Modelo carregado? {detector.model is not None}")

if detector.model:
    print(f"   Classes: {detector.model.names}")

    # Testar com imagem de gato
    cat_img_path = Path("yolo_dataset/images/test/cat_37.jpg")
    dog_img_path = Path("yolo_dataset/images/test/dog_37.jpg")

    for img_path in [cat_img_path, dog_img_path]:
        if img_path.exists():
            print(f"\n🧪 Testando: {img_path.name}")
            img = cv2.imread(str(img_path))
            resultado = detector.detectar_objetos(img, confianca_minima=0.25)

            print(f"   Modo: {resultado['modo']}")
            print(f"   Total objetos: {resultado['total_objetos']}")

            if resultado['deteccoes']:
                for det in resultado['deteccoes']:
                    print(f"   ✅ {det['classe']} (confiança: {det['confianca']:.2f})")
            else:
                print(f"   ❌ Nenhuma detecção")
else:
    print("   ⚠️ MODELO NÃO FOI CARREGADO!")
    print("\n   Verificando caminho esperado:")
    base_path = Path(__file__).parent.parent.parent
    model_path = base_path / "fases" / "fase_6_cap_1" / "runs" / "detect" / "train_100epochs_corrigido" / "weights" / "best.pt"
    print(f"   Caminho: {model_path}")
    print(f"   Existe? {model_path.exists()}")
