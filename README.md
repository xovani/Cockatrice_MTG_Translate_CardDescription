# Cockatrice_MTG_Translate_CardDescription

Este projeto automatiza a tradução dos textos das cartas do jogo **Magic: The Gathering**, no formato utilizado pelo Cockatrice (`cards.xml`). O script usa a API pública do Google Tradutor, com suporte a um sistema de cache e substituição inteligente de termos técnicos.

## 🧠 Objetivo

- Traduzir os textos das cartas do inglês para o português com consistência.
- Evitar erros comuns de tradução automática com termos próprios do MTG (ex: "Flying" → "voar").
- Utilizar cache para evitar retraduções e reduzir uso de API.
- Manter o formato XML original para uso direto no Cockatrice.

## 🛠️ Como funciona

1. Lê o arquivo XML de cartas localizado em `Base/cards.xml`.
2. Substitui termos técnicos por marcadores temporários.
3. Usa o Google Tradutor para traduzir o texto completo.
4. Reinsere os termos técnicos traduzidos no lugar correto.
5. Atualiza o cache (`cache_traducao.json`) para otimizar execuções futuras.
6. Salva o novo XML traduzido em `Traduzido/cards_traduzido.xml`.

## ▶️ Como usar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/Cockatrice_MTG_Translate_CardDescription.git
   cd Cockatrice_MTG_Translate_CardDescription
