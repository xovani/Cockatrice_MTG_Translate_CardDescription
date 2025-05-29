import os
import time
import json
import xml.etree.ElementTree as ET
from googletrans import Translator
import re

# Caminhos
pasta_raiz = os.path.dirname(__file__)
caminho_base = os.path.join(pasta_raiz, 'Base', 'cards.xml')
caminho_saida = os.path.join(pasta_raiz, 'Traduzido', 'cards_traduzido.xml')
caminho_cache = os.path.join(pasta_raiz, 'cache_traducao.json')
os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

# Carregar cache
if os.path.exists(caminho_cache):
    with open(caminho_cache, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {}

# Substituições específicas
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
    # Gera tokens sempre em letras minúsculas no formato [[termo_000]], [[termo_001]], ...
    return {f"[[termo_{str(i).zfill(3)}]]": termo_pt for i, termo_pt in enumerate(substituicoes.values())}

def aplicar_marcadores(texto, tokens):
    for termo_en, termo_pt in substituicoes.items():
        token = [k for k, v in tokens.items() if v == termo_pt][0]
        # Substitui todas as ocorrências da palavra inteira, ignorando case
        padrao = re.compile(r'\b' + re.escape(termo_en) + r'\b', flags=re.IGNORECASE)
        texto = padrao.sub(token, texto)
    return texto

def remover_marcadores(texto, tokens):
    texto_final = texto
    for token, termo_pt in tokens.items():
        # Criar regex para pegar o token com variações:
        # Pode ter maiúsculas, colchetes faltando, espaços extras, etc.
        # Exemplo de regex: \[?\[?termo_060\]?\]?
        token_pattern = re.escape(token.strip('[]'))  # só "termo_060"
        padrao = re.compile(r'\[?\[?' + token_pattern + r'\]?\]?', re.IGNORECASE)

        def substituir(match):
            token_text = match.group(0)
            # Se a primeira letra do token é maiúscula (ignorando colchetes), capitaliza o termo_pt
            # Removendo colchetes pra ver a letra
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

# Carregar XML
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
            print(f"✅ [{i}/{total}] {nome_carta} ➜ {texto_final[:60]}...")
            time.sleep(0.05)

        except Exception as e:
            erros += 1
            print(f"⚠️ [{i}/{total}] Erro em {nome_carta}: {e}")
            time.sleep(0.05)

# Salvar XML traduzido
tree.write(caminho_saida, encoding='utf-8', xml_declaration=True)
print(f"\n✅ Tradução finalizada! Arquivo salvo em: {caminho_saida}")

# Salvar cache atualizado
with open(caminho_cache, 'w', encoding='utf-8') as f:
    json.dump(cache, f, ensure_ascii=False, indent=2)
print(f"🧠 Cache salvo em: {caminho_cache}")

# Estatísticas
print(f"\n📊 Total de textos encontrados: {total}")
print(f"📌 Já estavam no cache: {total - traduzidos}")
print(f"📥 Traduzidos nesta execução: {traduzidos}")
print(f"❌ Erros de tradução: {erros}")
