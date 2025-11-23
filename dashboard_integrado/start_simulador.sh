#!/bin/bash

echo "🤖 Iniciando Simulador IoT - Fase 3"
echo "======================================"
echo ""
echo "O simulador irá gerar dados de sensores em tempo real."
echo "Pressione Ctrl+C para parar."
echo ""

cd "$(dirname "$0")"
python simulador_iot.py
