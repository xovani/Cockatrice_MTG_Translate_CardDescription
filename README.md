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
0. Instale o Python em seu sistema operacional.

1. Instale as dependências:
   pip install googletrans==4.0.0-rc1

2. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/Cockatrice_MTG_Translate_CardDescription.git
   cd Cockatrice_MTG_Translate_CardDescription

3. Coloque o arquivo cards.xml original na pasta Base/.
   Geralmente no Cockatrice este arquivos esta na pasta: C:\Users\[USUARIO]\AppData\Local\Cockatrice\Cockatrice

4. Execute o script:
python traduzir_cards.py

## ⚠️ Observações
* O cache (cache_traducao.json) evita retraduções e acelera o processo. Deixei um cache já no projeto com as traduções em PT-BR.

* Pequenos delays são aplicados para evitar bloqueio pela API.

* O script respeita o layout XML original do Cockatrice.

* Se você entende um pouco de Python pode utilizar para qualquer idioma, basta alterar a função traduzir_texto:
   def traduzir_texto(texto):
    try:
        resultado = translator.translate(texto, src='en', dest='pt')
        return resultado.text
    except Exception as e:
        raise Exception(f"Erro ao traduzir com Google: {e}")

  *** Caso for alterar o arquivo de cache atual deverá ser excluído para o script criar uma base nova na sua lingua.

## 🧠 Contribuições
Sugestões, melhorias ou correções são bem-vindas! Abra uma issue ou envie um Pull Request.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


