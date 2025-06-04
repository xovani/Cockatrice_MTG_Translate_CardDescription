# Cockatrice_MTG_Translate_CardDescription

Sou iniciante no Magic, e ler o que carta faz as vezes pode parece muito complexo pra mim, então resolvi desenvolver este projeto.
Este projeto automatiza a tradução dos textos das cartas na descrição, do jogo **Magic: The Gathering**, no formato utilizado pelo **Cockatrice** (`cards.xml`). O script usa a API pública do Google Tradutor, com suporte a um sistema de cache e substituição inteligente de termos técnicos.

## 🧠 Objetivo

- Traduzir na descrição os textos das cartas do inglês para o português com consistência.
- Evitar erros comuns de tradução automática com termos próprios do MTG (ex: "Flying" → "voar").
- Utilizar cache para evitar retraduções e reduzir uso de API.
- Manter o formato XML original para uso direto no Cockatrice.

![20250529-080616-001](https://github.com/user-attachments/assets/9d40a74d-9980-4d98-85a0-d930d50bfae0)


## 🛠️ Como funciona

1. Lê o arquivo XML de cartas localizado em `Base/cards.xml`.
2. Substitui termos técnicos por marcadores temporários.
3. Usa o Google Tradutor para traduzir o texto completo.
4. Reinsere os termos técnicos traduzidos no lugar correto.
5. Atualiza o cache (`cache_traducao.json`) para otimizar execuções futuras.
6. Salva o novo XML traduzido em `Traduzido/cards_traduzido.xml`.

## ▶️ Como usar

### 🔰 Opção 1 - Para usuários iniciantes (executável)

1. Baixe o **.ZIP com a estrutura completa** na [seção de releases do projeto](https://github.com/xovani/Cockatrice_MTG_Translate_CardDescription/releases).
2. Extraia o conteúdo do `.zip` em uma pasta de sua preferência.
3. Execute o arquivo `Traduzir_Cards_v1.2.exe` com **duplo clique**.
4. Após abrir a janela clique Iniciar Tradução, aguarde o processo ser concluído, você poderá acompanhar na janela de log.
   
   ![20250604-160933-002](https://github.com/user-attachments/assets/058ce7f7-8a3d-421d-ab54-86a29affbe67)

5. Após a conclusão uma mensagem será apresentada na tela, dê OK, depois fechar.
6. Será gerado um backup automatico do seu banco de cartas em inglês caso queira reverter o processo cards_en.xml. Caso queira reverter basta deletar o arquivo cards.xml e renomear o arquivo cards_en.xml para o nome original.
   
![20250604-161636-003](https://github.com/user-attachments/assets/d676c334-934c-47d7-8c8b-8413e671d67c)

7. Reinicie ou Inicie seu Cockatrice. Aproveite.

### ⚙️ Opção 2 - Para usuários avançados (código aberto)

0. Instale o Python em seu sistema operacional.

1. Instale as dependências:
   pip install googletrans==4.0.0-rc1
   
2. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/Cockatrice_MTG_Translate_CardDescription.git
   cd Cockatrice_MTG_Translate_CardDescription

3. Execute o script:
python Traduzir_Cards_v1.2.py

4. Após abrir a janela clique Iniciar Tradução, aguarde o processo ser concluído, você poderá acompanhar na janela de log.
   
   ![20250604-160933-002](https://github.com/user-attachments/assets/058ce7f7-8a3d-421d-ab54-86a29affbe67)

5. Após a conclusão uma mensagem será apresentada na tela, dê OK, depois fechar.
6. Será gerado um backup automatico do seu banco de cartas em inglês caso queira reverter o processo cards_en.xml. Caso queira reverter basta deletar o arquivo cards.xml e renomear o arquivo cards_en.xml para o nome original.
   
![20250604-161636-003](https://github.com/user-attachments/assets/d676c334-934c-47d7-8c8b-8413e671d67c)

7. Reinicie ou Inicie seu Cockatrice. Aproveite.

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

* Cockatrice Project - https://github.com/Cockatrice/Cockatrice
* https://cockatrice.github.io/

## 🧠 Contribuições
Sugestões, melhorias ou correções são bem-vindas! Abra uma issue ou envie um Pull Request.

## 📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.


