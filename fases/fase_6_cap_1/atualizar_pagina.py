"""
Script para remover a opção "Gerar Imagem de Teste" da página YOLO
"""

arquivo = "/Users/italodom/DESENVOLVIMENTO/ITALO/FIAP/fase_7/fases/fase_6_cap_1/../../dashboard_integrado/pages/06_🔍_Fase6_YOLO.py"

with open(arquivo, 'r', encoding='utf-8') as f:
    linhas = f.readlines()

# Encontrar e substituir a seção
nova_secao = """    with col1:
        st.markdown("### Envio de Imagem")

        arquivo_upload = st.file_uploader(
            "Selecione uma imagem de gato ou cachorro",
            type=["jpg", "jpeg", "png"],
            help="Faça upload de uma foto de gato ou cachorro para detecção"
        )

        if arquivo_upload:
            imagem_pil = Image.open(arquivo_upload)
            imagem_numpy = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
            st.image(imagem_pil, caption="Imagem Enviada", use_container_width=True)
            st.session_state.imagem_temp = imagem_numpy

"""

# Remover linhas 142-177 e adicionar nova seção
novas_linhas = linhas[:141] + [nova_secao] + linhas[178:]

# Salvar
with open(arquivo, 'w', encoding='utf-8') as f:
    f.writelines(novas_linhas)

print("✅ Arquivo atualizado com sucesso!")
print("Removida a opção 'Gerar Imagem de Teste'")
