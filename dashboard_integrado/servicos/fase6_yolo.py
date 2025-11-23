"""
Serviços da Fase 6 - Vision Computacional com YOLO
FarmTech Solutions
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import base64
from io import BytesIO
from pathlib import Path

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None


class DetectorYOLO:
    """Detector YOLO real integrado com modelo treinado"""

    def __init__(self, model_path: Optional[str] = None, use_real_model: bool = True):
        """
        Inicializa o detector YOLO

        Args:
            model_path: Caminho para o modelo .pt treinado
            use_real_model: Se True, usa modelo YOLO real. Se False, usa simulação
        """
        self.use_real_model = use_real_model and YOLO is not None
        self.model = None

        # Classes do modelo treinado (cat/dog)
        self.classes = ["cat", "dog"]

        # Tradução para português
        self.class_names_pt = {
            "cat": "Gato 🐱",
            "dog": "Cachorro 🐶"
        }

        self.historico_deteccoes: List[Dict] = []

        # Tentar carregar modelo real
        if self.use_real_model:
            if model_path is None:
                # Caminho padrão para o melhor modelo (100 épocas com labels corrigidas)
                base_path = Path(__file__).parent.parent.parent
                model_path = base_path / "fases" / "fase_6_cap_1" / "runs" / "detect" / "train_100epochs_corrigido" / "weights" / "best.pt"

            if Path(model_path).exists():
                try:
                    self.model = YOLO(str(model_path))
                    print(f"✅ Modelo YOLO carregado: {model_path}")
                except Exception as e:
                    print(f"⚠️ Erro ao carregar modelo: {e}")
                    print("⚠️ Usando modo simulação")
                    self.use_real_model = False
            else:
                print(f"⚠️ Modelo não encontrado: {model_path}")
                print("⚠️ Usando modo simulação")
                self.use_real_model = False

    def detectar_objetos(
        self,
        imagem: np.ndarray,
        confianca_minima: float = 0.5
    ) -> Dict:
        """
        Detecta objetos em imagem usando YOLO real ou simulação

        Args:
            imagem: Array numpy da imagem (BGR ou RGB)
            confianca_minima: Confiança mínima para detecção

        Returns:
            Dict com detecções encontradas
        """
        if self.use_real_model and self.model is not None:
            # Usar modelo YOLO real
            deteccoes = self._detectar_com_modelo_real(imagem, confianca_minima)
        else:
            # Usar simulação
            deteccoes = self._gerar_deteccoes_simuladas(imagem.shape[0], imagem.shape[1])
            # Filtrar por confiança
            deteccoes = [d for d in deteccoes if d['confianca'] >= confianca_minima]

        resultado = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_objetos": len(deteccoes),
            "deteccoes": deteccoes,
            "confianca_media": np.mean([d['confianca'] for d in deteccoes]) if deteccoes else 0,
            "modo": "YOLO Real" if self.use_real_model else "Simulação"
        }

        self.historico_deteccoes.append(resultado)
        return resultado

    def _detectar_com_modelo_real(self, imagem: np.ndarray, confianca_minima: float) -> List[Dict]:
        """
        Executa detecção usando modelo YOLO real

        Args:
            imagem: Array numpy da imagem
            confianca_minima: Confiança mínima

        Returns:
            Lista de detecções
        """
        deteccoes = []

        try:
            # Executar predição com NMS para eliminar detecções duplicadas
            results = self.model.predict(
                source=imagem,
                conf=confianca_minima,
                iou=0.5,  # IoU threshold para NMS - elimina boxes sobrepostas
                max_det=10,  # Máximo de detecções por imagem
                verbose=False
            )

            # Processar resultados
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Extrair informações
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0].cpu().numpy())
                    cls = int(box.cls[0].cpu().numpy())

                    # Calcular centro e dimensões
                    x_center = int((x1 + x2) / 2)
                    y_center = int((y1 + y2) / 2)
                    width = int(x2 - x1)
                    height = int(y2 - y1)

                    # Nome da classe
                    class_name = self.classes[cls] if cls < len(self.classes) else f"Classe_{cls}"
                    class_name_pt = self.class_names_pt.get(class_name, class_name)

                    deteccoes.append({
                        "classe": class_name_pt,
                        "classe_original": class_name,
                        "classe_id": cls,
                        "confianca": round(conf, 3),
                        "bbox": {
                            "x": int(x1),
                            "y": int(y1),
                            "x_center": x_center,
                            "y_center": y_center,
                            "width": width,
                            "height": height
                        },
                        "area_pixels": width * height
                    })

        except Exception as e:
            print(f"⚠️ Erro na detecção: {e}")

        return deteccoes

    def _gerar_deteccoes_simuladas(self, altura: int, largura: int) -> List[Dict]:
        """Gera detecções simuladas para demonstração"""
        deteccoes = []

        # Simular algumas detecções
        num_deteccoes = np.random.randint(3, 8)

        for i in range(num_deteccoes):
            classe_idx = np.random.randint(0, len(self.classes))
            confianca = np.random.uniform(0.6, 0.99)

            x = np.random.randint(0, largura - 100)
            y = np.random.randint(0, altura - 100)
            w = np.random.randint(50, 150)
            h = np.random.randint(50, 150)

            deteccoes.append({
                "classe": self.classes[classe_idx],
                "classe_id": classe_idx,
                "confianca": round(confianca, 3),
                "bbox": {
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                },
                "area_pixels": w * h
            })

        return deteccoes

    def analisar_saude_plantacao(self, deteccoes: List[Dict]) -> Dict:
        """
        Analisa as detecções (adaptado para cat/dog)

        Args:
            deteccoes: Lista de detecções encontradas

        Returns:
            Dict com análise das detecções
        """
        total = len(deteccoes)

        # Contar por classe
        cats = sum(1 for d in deteccoes if d.get('classe_original', d['classe']) == 'cat')
        dogs = sum(1 for d in deteccoes if d.get('classe_original', d['classe']) == 'dog')

        # Score baseado na confiança média
        conf_media = np.mean([d['confianca'] for d in deteccoes]) if deteccoes else 0
        score = round(conf_media * 100, 1)

        status = "✅ Alta Confiança" if score >= 80 else \
                 "⚠️ Confiança Média" if score >= 50 else \
                 "🚨 Baixa Confiança"

        return {
            "score_saude": score,
            "status": status,
            "pragas_detectadas": 0,  # Mantido para compatibilidade
            "doencas_detectadas": 0,  # Mantido para compatibilidade
            "ervas_detectadas": 0,  # Mantido para compatibilidade
            "total_deteccoes": total,
            "gatos_detectados": cats,
            "cachorros_detectados": dogs,
            "recomendacoes": self._gerar_recomendacoes_deteccoes(cats, dogs, conf_media)
        }

    def _gerar_recomendacoes_deteccoes(self, cats: int, dogs: int, conf_media: float) -> List[str]:
        """Gera recomendações baseadas nas detecções"""
        recomendacoes = []

        if cats > 0 and dogs > 0:
            recomendacoes.append(f"🐱🐶 Detectados {cats} gato(s) e {dogs} cachorro(s)")

        if cats > 0 and dogs == 0:
            recomendacoes.append(f"🐱 Detectados {cats} gato(s) na imagem")

        if dogs > 0 and cats == 0:
            recomendacoes.append(f"🐶 Detectados {dogs} cachorro(s) na imagem")

        if conf_media >= 0.8:
            recomendacoes.append("✅ Detecções com alta confiança")
        elif conf_media >= 0.5:
            recomendacoes.append("⚠️ Detecções com confiança moderada")
        else:
            recomendacoes.append("🚨 Detecções com baixa confiança - tente outra imagem")

        if not recomendacoes:
            recomendacoes.append("ℹ️ Nenhum objeto detectado - tente com uma imagem de gato ou cachorro")

        return recomendacoes

    def _gerar_recomendacoes(self, pragas: int, doencas: int, ervas: int) -> List[str]:
        """Gera recomendações baseado em detecções"""
        recomendacoes = []

        if pragas > 2:
            recomendacoes.append("🐛 Alto nível de pragas - Considere aplicação de inseticida")

        if doencas > 1:
            recomendacoes.append("🦠 Presença de doenças - Isolem as plantas afetadas")

        if ervas > 3:
            recomendacoes.append("🌱 Infestação de ervas daninhas - Programar desherbagem")

        if not recomendacoes:
            recomendacoes.append("✅ Nenhuma ação imediata necessária - Continue monitoramento")

        return recomendacoes

    def obter_historico(self) -> List[Dict]:
        """Retorna histórico de detecções"""
        return self.historico_deteccoes

    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas gerais"""
        if not self.historico_deteccoes:
            return {
                "total_analises": 0,
                "media_objetos_por_imagem": 0,
                "confianca_media_geral": 0,
                "classes_mais_detectadas": []
            }

        total = len(self.historico_deteccoes)
        media_objetos = np.mean([d['total_objetos'] for d in self.historico_deteccoes])
        confianca_media = np.mean([d['confianca_media'] for d in self.historico_deteccoes])

        # Contar classes
        classes_count = {}
        for analise in self.historico_deteccoes:
            for det in analise['deteccoes']:
                classe = det['classe']
                classes_count[classe] = classes_count.get(classe, 0) + 1

        classes_top = sorted(classes_count.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "total_analises": total,
            "media_objetos_por_imagem": round(media_objetos, 1),
            "confianca_media_geral": round(confianca_media, 3),
            "classes_mais_detectadas": [c[0] for c in classes_top]
        }


class GeradorImagensTeste:
    """Gera imagens de teste para demonstração"""

    @staticmethod
    def gerar_imagem_aleatoria(altura: int = 480, largura: int = 640) -> np.ndarray:
        """
        Gera uma imagem aleatória simulando um pet (gato ou cachorro)

        Args:
            altura: Altura da imagem
            largura: Largura da imagem

        Returns:
            Array numpy com imagem RGB
        """
        if cv2 is None:
            # Fallback sem cv2
            imagem = np.zeros((altura, largura, 3), dtype=np.uint8)
            imagem[:] = [200, 200, 200]  # Gray background
            return imagem

        # Criar imagem com fundo cinza claro
        imagem = np.zeros((altura, largura, 3), dtype=np.uint8)
        imagem[:] = (220, 220, 220)  # Gray background

        # Escolher aleatoriamente entre gato e cachorro
        tipo = np.random.choice(['cat', 'dog'])

        if tipo == 'cat':
            # Cores para gato
            cor_corpo = (100, 100, 100)  # Cinza
            cor_olhos = (0, 255, 0)  # Verde
        else:
            # Cores para cachorro
            cor_corpo = (50, 100, 150)  # Marrom
            cor_olhos = (0, 100, 200)  # Castanho

        # Desenhar corpo (elipse central)
        centro_x = largura // 2
        centro_y = altura // 2
        cv2.ellipse(imagem, (centro_x, centro_y), (150, 100), 0, 0, 360, cor_corpo, -1)

        # Desenhar cabeça (círculo)
        cabeca_y = centro_y - 80
        cv2.circle(imagem, (centro_x, cabeca_y), 60, cor_corpo, -1)

        # Desenhar olhos
        cv2.circle(imagem, (centro_x - 20, cabeca_y - 10), 8, cor_olhos, -1)
        cv2.circle(imagem, (centro_x + 20, cabeca_y - 10), 8, cor_olhos, -1)

        # Desenhar nariz
        cv2.circle(imagem, (centro_x, cabeca_y + 10), 5, (0, 0, 0), -1)

        # Adicionar texto
        texto = "🐱 GATO" if tipo == 'cat' else "🐶 CACHORRO"
        cv2.putText(imagem, tipo.upper(), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return imagem

    @staticmethod
    def converter_para_base64(imagem: np.ndarray) -> str:
        """Converte imagem numpy para base64"""
        _, buffer = cv2.imencode('.jpg', imagem)
        img_bytes = buffer.tobytes()
        img_base64 = base64.b64encode(img_bytes).decode()
        return img_base64

    @staticmethod
    def converter_de_base64(img_base64: str) -> np.ndarray:
        """Converte imagem de base64 para numpy"""
        img_bytes = base64.b64decode(img_base64)
        nparr = np.frombuffer(img_bytes, dtype=np.uint8)
        imagem = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return imagem


class RelatorioVisao:
    """Gera relatórios de análise de visão computacional"""

    def __init__(self, detector: DetectorYOLO):
        self.detector = detector

    def gerar_relatorio_completo(self) -> Dict:
        """Gera relatório completo de análises"""
        historico = self.detector.obter_historico()
        stats = self.detector.obter_estatisticas()

        if not historico:
            return {
                "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mensagem": "Nenhuma análise realizada ainda"
            }

        # Análise geral
        todas_deteccoes = []
        for analise in historico:
            todas_deteccoes.extend(analise['deteccoes'])

        # Calcular saúde geral
        pragas_total = sum(1 for d in todas_deteccoes if d['classe'] == 'Praga')
        doencas_total = sum(1 for d in todas_deteccoes if d['classe'] == 'Doença')
        ervas_total = sum(1 for d in todas_deteccoes if d['classe'] == 'Erva Daninha')

        saude_geral = self.detector.analisar_saude_plantacao(todas_deteccoes)

        return {
            "data_geracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_analises": stats['total_analises'],
            "media_objetos": stats['media_objetos_por_imagem'],
            "confianca_media": stats['confianca_media_geral'],
            "saude_plantacao": saude_geral['status'],
            "score_saude": saude_geral['score_saude'],
            "pragas_totais": pragas_total,
            "doencas_totais": doencas_total,
            "ervas_totais": ervas_total,
            "classes_mais_detectadas": stats['classes_mais_detectadas'],
            "recomendacoes": saude_geral['recomendacoes']
        }


def gerar_dados_exemplo_yolo() -> Dict:
    """Gera dados de exemplo para demonstração YOLO"""

    detector = DetectorYOLO()

    # Gerar algumas análises de exemplo
    for i in range(5):
        imagem = GeradorImagensTeste.gerar_imagem_aleatoria()
        detector.detectar_objetos(imagem)

    relatorio = RelatorioVisao(detector)

    return {
        "detector": detector,
        "gerador_imagens": GeradorImagensTeste,
        "relatorio": relatorio
    }
