import os
import sys
import time
import json
import xml.etree.ElementTree as ET
from googletrans import Translator
import re
import shutil
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Função para pegar pasta do Cockatrice via variável de ambiente do usuário
def obter_pasta_cockatrice():
    userprofile = os.environ.get('USERPROFILE') or os.path.expanduser('~')
    pasta_cockatrice = os.path.join(userprofile, 'AppData', 'Local', 'Cockatrice', 'Cockatrice')
    return pasta_cockatrice

# Pasta raiz do script/exe
if getattr(sys, 'frozen', False):
    pasta_raiz = os.path.dirname(sys.executable)
else:
    pasta_raiz = os.path.dirname(os.path.abspath(__file__))

# Pastas
pasta_cockatrice = obter_pasta_cockatrice()
caminho_cards_original = os.path.join(pasta_cockatrice, 'cards.xml')
caminho_cards_backup = os.path.join(pasta_cockatrice, 'cards_en.xml')

pasta_base = os.path.join(pasta_raiz, 'Base')
pasta_cache = os.path.join(pasta_raiz, 'Cache')
pasta_traduzido = os.path.join(pasta_raiz, 'Traduzido')

# Criar pastas locais se não existirem
os.makedirs(pasta_base, exist_ok=True)
os.makedirs(pasta_cache, exist_ok=True)
os.makedirs(pasta_traduzido, exist_ok=True)

# Caminhos locais
caminho_base = os.path.join(pasta_base, 'cards.xml')
caminho_saida = os.path.join(pasta_traduzido, 'cards_traduzido.xml')
caminho_cache = os.path.join(pasta_cache, 'cache_traducao.json')

# Copiar cards.xml do Cockatrice para Base, se não existir ainda
if not os.path.exists(caminho_base):
    shutil.copy2(caminho_cards_original, caminho_base)

# Carregar cache
if os.path.exists(caminho_cache):
    with open(caminho_cache, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

# Substituições específicas (pode ampliar se quiser)
substituicoes = {
    "Flying": "voar",
    "Trample": "atropelar",
    "Haste": "ímpeto",
    "Deathtouch": "toque mortífero",
    "Lifelink": "vínculo com a vida",
    "First strike": "iniciativa",
    "Double strike": "golpe duplo",
    "Vigilance": "vigilância",
    "Menace": "ameaça",
    "Reach": "alcance",
    "Hexproof": "resistência à magia",
    "Indestructible": "indestrutível",
    "Ward {X}": "proteção ward {X}",
    "Flash": "lampejo",
    "Protection from": "proteção contra",
    "Defender": "defensor",
    "Exalted": "exaltado",
    "Prowess": "pujança",
    "Morph": "metamorfose",
    "Megamorph": "megametamorfose",
    "Persist": "persistir",
    "Undying": "imortal",
    "Annihilator": "aniquilador",
    "Cascade": "cascata",
    "Scry": "adivinhar",
    "Surveil": "vigiar",
    "Convoke": "convocar",
    "Delve": "devassar",
    "Escape": "fugir",
    "Embalm": "embalsamar",
    "Eternalize": "eternizar",
    "Ninjutsu": "ninjutsu",
    "Unearth": "desenterrar",
    "Flashback": "retrospectiva",
    "Aftermath": "consequência",
    "Adventure": "aventura",
    "Mutate": "mutação",
    "Crew": "tripular",
    "Equip": "equipar",
    "Fortify": "fortificar",
    "Kicker": "chutar",
    "Multikicker": "chutar múltiplas vezes",
    "Buyback": "resgatar",
    "Suspend": "suspender",
    "Vanishing": "desvanecer",
    "Fading": "desbotar",
    "Modular": "modular",
    "Evolve": "evoluir",
    "Exploit": "explorar",
    "Escalate": "escalar",
    "Fabricate": "fabricar",
    "Devoid": "sem cor",
    "Training": "treinamento",
    "Cleave": "separar",
    "Prototype": "protótipo",
    "Battle cry": "grito de batalha",
    "Myriad": "miríade",
    "Rebound": "ricochetear",
    "Enchant creature": "encantar criatura",
    "Enchant player": "encantar jogador",
    "Library": "biblioteca (grimório)",
    "Enchant Land": "encantar terreno"
}

translator = Translator()

def gerar_tokens(substituicoes):
    return {f"[[termo_{str(i).zfill(3)}]]": termo_pt for i, termo_pt in enumerate(substituicoes.values())}

def aplicar_marcadores(texto, tokens):
    for termo_en, termo_pt in substituicoes.items():
        token = [k for k, v in tokens.items() if v == termo_pt][0]
        padrao = re.compile(r'\b' + re.escape(termo_en) + r'\b', flags=re.IGNORECASE)
        texto = padrao.sub(token, texto)
    return texto

def remover_marcadores(texto, tokens):
    texto_final = texto
    for token, termo_pt in tokens.items():
        token_pattern = re.escape(token.strip('[]'))
        padrao = re.compile(r'\[?\[?' + token_pattern + r'\]?\]?', re.IGNORECASE)
        def substituir(match):
            token_text = match.group(0)
            letras = re.sub(r'[\[\]]', '', token_text)
            if letras and letras[0].isupper():
                return termo_pt[0].upper() + termo_pt[1:]
            else:
                return termo_pt
        texto_final = padrao.sub(substituir, texto_final)
    return texto_final

def traduzir_texto(texto):
    try:
        resultado = translator.translate(texto, src='en', dest='pt')
        return resultado.text
    except Exception as e:
        raise Exception(f"Erro ao traduzir com Google: {e}")

# Função para atualizar log na interface
def adicionar_log_gui(texto):
    log_text.config(state='normal')
    log_text.insert(tk.END, texto + "\n")
    log_text.see(tk.END)
    log_text.config(state='disabled')

# Função para atualizar barra de progresso
def atualizar_barra(valor):
    barra_progresso['value'] = valor
    janela.update_idletasks()

def traduzir_cards():
    global traduzidos, erros
    try:
        # Copiar cards.xml para Base (atualizar toda vez)
        shutil.copy2(caminho_cards_original, caminho_base)
        adicionar_log_gui(f"📁 Arquivo cards.xml copiado para pasta Base.")

        # Backup do arquivo original no Cockatrice (cards_en.xml)
        if not os.path.exists(caminho_cards_backup):
            shutil.copy2(caminho_cards_original, caminho_cards_backup)
            adicionar_log_gui(f"📁 Backup criado: cards_en.xml")
        else:
            adicionar_log_gui(f"📁 Backup já existe: cards_en.xml")

        tree = ET.parse(caminho_base)
        root = tree.getroot()

        cards_com_texto = [card for card in root.iter('card') if card.find('text') is not None and card.find('text').text]
        total = len(cards_com_texto)

        traduzidos = 0
        erros = 0

        for i, card in enumerate(cards_com_texto, start=1):
            text_elem = card.find('text')
            name_elem = card.find('name')
            original_texto = text_elem.text.strip()
            nome_carta = name_elem.text.strip() if name_elem is not None else "Sem nome"

            if original_texto in cache:
                text_elem.text = cache[original_texto]["translated"]
                # Não mostrar no log quando vem do cache
            else:
                try:
                    tokens = gerar_tokens(substituicoes)
                    texto_com_marcadores = aplicar_marcadores(original_texto, tokens)
                    texto_traduzido = traduzir_texto(texto_com_marcadores)
                    texto_final = remover_marcadores(texto_traduzido, tokens)

                    cache[original_texto] = {
                        "name": nome_carta,
                        "translated": texto_final
                    }

                    text_elem.text = texto_final
                    traduzidos += 1
                    adicionar_log_gui(f"✅ [{i}/{total}] {nome_carta} ➜ {texto_final[:60]}...")
                    time.sleep(0.1)

                except Exception as e:
                    erros += 1
                    adicionar_log_gui(f"⚠️ [{i}/{total}] Erro em {nome_carta}: {e}")
                    time.sleep(0.1)

            progresso = int((i / total) * 100)
            atualizar_barra(progresso)

        # Salvar XML traduzido local
        tree.write(caminho_saida, encoding='utf-8', xml_declaration=True)
        adicionar_log_gui(f"\n✅ Tradução finalizada! Arquivo salvo em: {caminho_saida}")

        # Salvar cache atualizado
        with open(caminho_cache, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        adicionar_log_gui(f"🧠 Cache salvo em: {caminho_cache}")

        # Copiar o arquivo traduzido para pasta Cockatrice, sobrescrevendo cards.xml
        shutil.copy2(caminho_saida, caminho_cards_original)
        adicionar_log_gui(f"📂 Arquivo traduzido copiado para a pasta Cockatrice.")

        # Estatísticas finais
        adicionar_log_gui(f"\n📊 Total de textos encontrados: {total}")
        adicionar_log_gui(f"📌 Já estavam no cache: {total - traduzidos}")
        adicionar_log_gui(f"📥 Traduzidos nesta execução: {traduzidos}")
        adicionar_log_gui(f"❌ Erros de tradução: {erros}")

        messagebox.showinfo("Sucesso", "Tradução finalizada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def iniciar_traducao():
    botao_iniciar.config(state='disabled')
    threading.Thread(target=traduzir_cards).start()

def fechar_janela():
    if messagebox.askokcancel("Sair", "Deseja realmente fechar?"):
        janela.destroy()

# --- Interface gráfica ---
janela = tk.Tk()
janela.title("Tradutor de Cards Cockatrice")
janela.geometry("700x500")
janela.protocol("WM_DELETE_WINDOW", fechar_janela)

label_titulo = tk.Label(janela, text="Cockatrice MTG - Tradutor de Cartas - V1.2", font=("Helvetica", 14, "bold"))
label_titulo.pack(pady=(10, 5))

frame_log = tk.Frame(janela)
frame_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

log_text = tk.Text(frame_log, state='disabled', height=20, wrap='word')
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_log, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text['yscrollcommand'] = scrollbar.set

barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=600, mode="determinate")
barra_progresso.pack(pady=10)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

botao_iniciar = tk.Button(frame_botoes, text="Iniciar Tradução", command=iniciar_traducao)
botao_iniciar.pack(side=tk.LEFT, padx=10)

botao_fechar = tk.Button(frame_botoes, text="Fechar", command=fechar_janela)
botao_fechar.pack(side=tk.LEFT, padx=10)

janela.mainloop()