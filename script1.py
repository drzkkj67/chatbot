import streamlit as st
import g4f
import time
import os

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTADOS GLOBAIS
# ==============================================================================
st.set_page_config(
    page_title="PyChef Pro - Hub Gastronômico", 
    page_icon="🧑‍🍳", 
    layout="wide",
    initial_sidebar_state="expanded"
)

ARQUIVO_RECEITAS = "receitas_salvas.txt"

def carregar_receitas():
    receitas = {}
    if os.path.exists(ARQUIVO_RECEITAS):
        with open(ARQUIVO_RECEITAS, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if conteudo:
                blocos = conteudo.split("=== FIM DA RECEITA ===\n")
                for bloco in blocos:
                    if "TITULO:" in bloco and "CONTEUDO:" in bloco:
                        try:
                            partes = bloco.split("CONTEUDO:")
                            titulo = partes[0].replace("TITULO:", "").strip()
                            texto = partes[1].strip()
                            receitas[titulo] = texto
                        except:
                            pass
    return receitas

def salvar_receita_no_arquivo(titulo, texto):
    with open(ARQUIVO_RECEITAS, "a", encoding="utf-8") as f:
        f.write(f"TITULO: {titulo}\nCONTEUDO:\n{texto}\n=== FIM DA RECEITA ===\n")

# Inicialização de variáveis de configuração no Session State
if "idioma" not in st.session_state:
    st.session_state.idioma = "Português"
if "tamanho_fonte" not in st.session_state:
    st.session_state.tamanho_fonte = "Normal"
if "notificacoes" not in st.session_state:
    st.session_state.notificacoes = True
if "modo_resposta" not in st.session_state:
    st.session_state.modo_resposta = "Detalhado"
if "lista_compras" not in st.session_state:
    st.session_state.lista_compras = []

# ==============================================================================
# DESIGN E CUSTOMIZAÇÃO DE CSS AVANÇADO (COM SUA CORREÇÃO)
# ==============================================================================
tamanho_px = "16px" if st.session_state.tamanho_fonte == "Normal" else "20px" if st.session_state.tamanho_fonte == "Grande" else "24px"

st.markdown(
    f"""
    <style>
    p, span, li, input, button, select {{ 
        font-size: {tamanho_px} !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: transparent;
        padding: 8px;
        border-radius: 12px;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 12px 24px;
        background-color: rgba(128, 128, 128, 0.08);
        border-radius: 8px;
        color: inherit;
        border: none;
        transition: all 0.3s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: rgba(255, 75, 75, 0.1);
        color: #FF4B4B;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold;
        box-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);
    }}
    [data-testid="stChatMessage"] {{
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid rgba(128, 128, 128, 0.1);
    }}
    [data-testid="stChatInput"] {{
        border-radius: 25px !important;
        border: 2px solid rgba(128, 128, 128, 0.2) !important;
        padding: 5px !important;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color: #FF4B4B !important;
    }}
    .stButton>button {{
        border-radius: 8px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }}
    .stExpander {{
        border-radius: 12px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
        background-color: rgba(128, 128, 128, 0.03);
    }}
    
    /* Correção para ocultar o texto do ícone quebrado na barra lateral */
    button[data-testid="collapse-sidebar-button"] {{
        font-size: 0px !important;
        color: transparent !important;
    }}
    button[data-testid="collapse-sidebar-button"]::before {{
        content: "◀" !important;
        font-size: 14px !important;
        color: inherit !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Dicionário de Idiomas
textos = {
    "Português": {
        "boas_vindas": "Bem-vindo ao seu Hub Gastronômico! O que vamos criar na cozinha hoje? 🍳",
        "aba_chat": "💬 Assistente Inteligente",
        "aba_compras": "🛒 Lista de Compras",
        "aba_financeiro": "💰 Calculadora de Custos",
        "aba_utilitarios": "⏱️ Timer & Medidas",
        "aba_favoritas": "⭐ Livro de Receitas",
        "aba_config": "⚙️ Configurações do Sistema",
        "titulo_chat": "💬 Converse com o Chef",
        "sub_chat": "Solicite receitas personalizadas ou tire dúvidas culinárias.",
        "btn_limpar": "🗑️ Limpar Conversa Atual",
        "chef_pensando": "O Chef está escrevendo sua receita...",
        "input_chat": "Pergunte ao Chef...",
        "txt_config": "⚙️ Painel de Controle e Customização",
        "txt_idioma": "Idioma do Sistema",
        "txt_fonte": "Tamanho do Texto (Acessibilidade)",
        "txt_notif": "Ativar Alertas Sonoros e Visuais",
        "txt_resposta": "Estilo de Resposta da IA",
    },
    "Inglês": {
        "boas_vindas": "Welcome to your Gastronomic Hub! What are we cooking today? 🍳",
        "aba_chat": "💬 Intelligent Assistant",
        "aba_compras": "🛒 Shopping List",
        "aba_financeiro": "💰 Cost Calculator",
        "aba_utilitarios": "⏱️ Timer & Measures",
        "aba_favoritas": "⭐ Recipe Book",
        "aba_config": "⚙️ System Settings",
        "titulo_chat": "💬 Talk to the Chef",
        "sub_chat": "Request personalized recipes or ask culinary questions.",
        "btn_limpar": "🗑️ Clear Current Chat",
        "chef_pensando": "The Chef is writing your recipe...",
        "input_chat": "Ask the Chef...",
        "txt_config": "⚙️ Control Panel and Customization",
        "txt_idioma": "System Language",
        "txt_fonte": "Text Size (Accessibility)",
        "txt_notif": "Enable Sound and Visual Alerts",
        "txt_resposta": "AI Response Style",
    },
    "Espanhol": {
        "boas_vindas": "¡Bienvenido a tu Hub Gastronómico! ¿Qué vamos a cocinar hoy? 🍳",
        "aba_chat": "💬 Asistente Inteligente",
        "aba_compras": "🛒 Lista de Compras",
        "aba_financeiro": "💰 Calculadora de Costos",
        "aba_utilitarios": "⏱️ Temporizador",
        "aba_favoritas": "⭐ Libro de Recetas",
        "aba_config": "⚙️ Configuración",
        "titulo_chat": "💬 Habla con el Chef",
        "sub_chat": "Solicite receitas personalizadas ou faça perguntas culinárias.",
        "btn_limpar": "🗑️ Limpar Conversación",
        "chef_pensando": "El Chef está escribiendo tu receta...",
        "input_chat": "Pregúntale al Chef...",
        "txt_config": "⚙️ Panel de Control y Personalización",
        "txt_idioma": "Idioma del Sistema",
        "txt_fonte": "Tamaño del Texto (Accesibilidad)",
        "txt_notif": "Activar Alertas Sonoras y Visuales",
        "txt_resposta": "Estilo de Respuesta de IA",
    }
}

txt = textos[st.session_state.idioma]

if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "system", "content": f"Você é o PyChef Pro. Responda no idioma {st.session_state.idioma}. Modo de resposta: {st.session_state.modo_resposta}."},
        {"role": "assistant", "content": txt["boas_vindas"]}
    ]

# ==============================================================================
# 2. BARRA LATERAL (PAINEL DE CONTROLE)
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>🧑‍🍳</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: 0;'>PyChef Pro</h2>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("🧠 IA Engine")
    modelo_selecionado = st.selectbox(
        "Model:", ["GPT-4o (Recomendado)", "GPT-4", "GPT-3.5"], index=0, label_visibility="collapsed"
    )
    
    st.divider()
    st.subheader("🥑 Diet & Preferences")
    dieta = st.multiselect(
        "Filters:", ["Sem Glúten", "Sem Lactose", "Vegano", "Vegetariano", "Low Carb"], placeholder="No restrictions"
    )
    
    st.divider()
    if st.button(txt["btn_limpar"], use_container_width=True, type="secondary"):
        st.session_state.messages = [
            {"role": "system", "content": f"Você é o PyChef Pro. Responda no idioma {st.session_state.idioma}."},
            {"role": "assistant", "content": txt["boas_vindas"]}
        ]
        st.rerun()

# ==============================================================================
# 3. SISTEMA DE ABAS PRINCIPAIS ESTILIZADAS
# ==============================================================================
aba_chat, aba_compras, aba_financeiro, aba_utilitarios, aba_favoritas, aba_config = st.tabs([
    txt["aba_chat"], txt["aba_compras"], txt["aba_financeiro"], txt["aba_utilitarios"], txt["aba_favoritas"], txt["aba_config"]
])

# ABA 1: CHAT INTELIGENTE
with aba_chat:
    st.markdown(f"## {txt['titulo_chat']}")
    st.caption(txt["sub_chat"])
    st.divider()
    
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = "👤" if message["role"] == "user" else "🧑‍🍳"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            
    if prompt_usuario := st.chat_input(txt["input_chat"]):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt_usuario)
            
        prompt_final = f"{prompt_usuario} [Responda obrigatoriamente em {st.session_state.idioma}]. [Estilo de escrita: {st.session_state.modo_resposta}]."
        if dieta:
            prompt_final += f" [Restrições: {', '.join(dieta)}]."
            
        st.session_state.messages.append({"role": "user", "content": prompt_final})
        
        with st.chat_message("assistant", avatar="🧑‍🍳"):
            placeholder_resposta = st.empty()
            with st.spinner(txt["chef_pensando"]):
                try:
                    if "GPT-4" in modelo_selecionado:
                        modelo_string = "gpt-4"
                    elif "GPT-3.5" in modelo_selecionado:
                        modelo_string = "gpt-3.5-turbo"
                    else:
                        modelo_string = "gpt-4o"
                    
                    resposta_ia = g4f.ChatCompletion.create(
                        model=modelo_string,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    )
                    placeholder_resposta.markdown(resposta_ia)
                    st.session_state.messages.append({"role": "assistant", "content": resposta_ia})
                except Exception as e:
                    placeholder_resposta.error(f"Não foi possível conectar ao Chef IA no momento. Detalhes: {e}")

# ABA 2: LISTA DE COMPRAS
with aba_compras:
    st.markdown("## 🛒 Planning & Shopping")
    st.divider()
    novo_item = st.text_input("Adicionar ingrediente:", placeholder="Ex: Chocolate 70% 200g")
    if st.button("➕ Adicionar", key="add_item_btn"):
        if novo_item:
            st.session_state.lista_compras.append(novo_item)
            st.rerun()
            
    for indice, item in enumerate(st.session_state.lista_compras):
        col_t, col_b = st.columns([5, 1])
        col_t.markdown(f"- {item}")
        if col_b.button("❌", key=f"del_it_{indice}"):
            st.session_state.lista_compras.pop(indice)
            st.rerun()

# ABA 3: FINANCEIRO
with aba_financeiro:
    st.markdown("## 💰 Custos de Receita")
    st.divider()
    c_ing = st.number_input("Ingredientes (R$):", min_value=0.0, value=10.0)
    c_ad = st.number_input("Custos extras/gás (R$):", min_value=0.0, value=2.0)
    margem = st.slider("Lucro (%):", min_value=10, max_value=200, value=100)
    
    total_c = c_ing + c_ad
    venda = total_c + (total_c * (margem/100))
    st.metric("Preço de Venda Sugerido", f"R$ {venda:.2f}", f"Custo: R$ {total_c:.2f}")

# ABA 4: UTILITÁRIOS & TIMER
with aba_utilitarios:
    st.markdown("## ⏱️ Cozinha Utils & Timer")
    st.divider()
    
    t_min = st.number_input("Minutos de cozimento:", min_value=1, max_value=120, value=1)
    
    if st.button("🚀 Iniciar Alerta Seguro"):
        status_timer = st.empty()
        pb = st.progress(0)
        
        total_segundos = t_min * 60
        for s in range(total_segundos):
            time.sleep(1)
            porcentagem = int((s + 1) / total_segundos * 100)
            pb.progress(porcentagem)
            status_timer.caption(f"Tempo decorrido: {s+1}s de {total_segundos}s")
            
        status_timer.success("🔔 Tempo Esgotado! Sua receita está pronta!")
        if st.session_state.notificacoes:
            st.toast("🔔 Receita Concluída!", icon="🍳")
        st.balloons()

# ABA 5: LIVRO DE RECEITAS FAVORITAS
with aba_favoritas:
    st.markdown("## ⭐ Livro de Favoritos Permanente")
    st.caption("As receitas salvas aqui ficam gravadas no servidor e não somem ao atualizar a página.")
    st.divider()
    
    t_fav = st.text_input("Título da Receita:")
    c_fav = st.text_area("Passo a Passo / Ingredientes:")
    
    if st.button("💾 Guardar para Sempre"):
        if t_fav and c_fav:
            salvar_receita_no_arquivo(t_fav, c_fav)
            st.success(f"Receita '{t_fav}' gravada com sucesso!")
            time.sleep(0.5)
            st.rerun()
            
    st.markdown("### 📖 Suas Receitas Salvas")
    receitas_permanentes = carregar_receitas()
    
    if not receitas_permanentes:
        st.info("Nenhuma receita salva ainda. Adicione uma acima!")
    else:
        for k, v in receitas_permanentes.items():
            with st.expander(f"📋 {k}"):
                st.write(v)

# ABA 6: CONFIGURAÇÕES AVANÇADAS
with aba_config:
    st.markdown(f"## {txt['txt_config']}")
    st.divider()
    
    st.markdown(f"### 🌐 Localização")
    novo_idioma = st.selectbox(
        txt["txt_idioma"],
        ["Português", "Inglês", "Espanhol"],
        index=["Português", "Inglês", "Espanhol"].index(st.session_state.idioma)
    )
    if novo_idioma != st.session_state.idioma:
        st.session_state.idioma = novo_idioma
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    
    st.markdown("### 👁️ Acessibilidade & Texto")
    nova_fonte = st.select_slider(
        txt["txt_fonte"],
        options=["Normal", "Grande", "Gigante"],
        value=st.session_state.tamanho_fonte
    )
    if nova_fonte != st.session_state.tamanho_fonte:
        st.session_state.tamanho_fonte = nova_fonte
        st.rerun()
        
    st.divider()
    
    st.markdown("### 🤖 Ajustes da Inteligência Artificial")
    novo_modo = st.radio(
        txt["txt_resposta"],
        ("Detalhado", "Direto", "Humorístico"),
        index=0 if st.session_state.modo_resposta.startswith("Detalhado") else 1 if st.session_state.modo_resposta.startswith("Direto") else 2
    )
    if novo_modo != st.session_state.modo_resposta:
        st.session_state.modo_resposta = novo_modo
        
    st.divider()
    
    st.markdown("### 🔔 Alertas e Sistema")
    notif_check = st.checkbox(txt["txt_notif"], value=st.session_state.notificacoes)
    st.session_state.notificacoes = notif_check
