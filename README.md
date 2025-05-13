# **Chatbot Inteligente - Loja GMV Tech**

Este repositório contém um chatbot inteligente em Python desenvolvido para simular interações com clientes de uma loja de tecnologia (Loja GMV Tech). O assistente responde dúvidas frequentes, sugere produtos e encaminha para atendimento humano quando necessário.
_______________________________________________________________________________
# **Índice**

- Funcionalidades
- Tecnologias
- Estrutura de Pastas
- Instalação
- Uso
- Exemplos de Interação
_______________________________________________________________________________
**Funcionalidades**

1. Saudações e menu inicial
2. Respostas contextuais sobre:
    > Horário de funcionamento
    > Produtos disponíveis
    > Serviços oferecidos
    > Agendamento de atendimento
    > Formas de pagamento
    > Opções de entrega
    > Sugestões de produtos
    > Encaminhamento para atendimento humano
3. Simulação de sistema de recomendação simples
4. Encerramento adequado da conversa
5. Estrutura de agente inteligente com classificação de intenções (Naive Bayes)
_______________________________________________________________________________
**Tecnologias**

- Python 3.x
- Bibliotecas:
    > scikit-learn
    > joblib
    > re (expressões regulares)
    > (Opcional para expansão: NLTK, spaCy, ChatterBot, Transformers, Rasa)
_______________________________________________________________________________
Estrutura de Pastas
```bash
├── data/
│   ├── intenções.json           
│   ├── respostas.json           
│   └── modelos/                 
│       ├── vectorizer.joblib
│       ├── encoder.joblib
│       └── modelo.joblib
├── src/
│   └── chatbot.py               
├── README.md                    
└── requirements.txt
```           
______________________________________________________________________________
**Instalação**

1. Clone este repositório:

    ```bash
   git clone https://github.com/V1mendes/ChatBot-GMV-Tech.git
    ```
    ```bash
    cd gmvtech-chatbot
    ``` 

3. Crie e ative um ambiente virtual (opcional, mas recomendado):

    ```bash
    python3 -m venv venv
    ``` 
    ```bash
    source venv/bin/activate   # Linux/Mac
    ``` 
    ```bash
    venv\Scripts\activate    # Windows
    ```

4. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

5. Certifique-se de que os modelos serializados (vectorizer.joblib, encoder.joblib, modelo.joblib) estejam na pasta data/modelos/.
_____________________________________________________________________________
**Uso**

Para executar o chatbot, rode o script:

python src/chatbot.py

Ao iniciar, o assistente exibirá um menu com opções de intenções. Digite o número correspondente para selecionar a categoria de sua dúvida e em seguida digite sua pergunta ou escolha uma pergunta de exemplo.

Comandos disponíveis

Digite 0 a qualquer momento para sair do atendimento.
____________________________________________________________________________
**Exemplos de Interação**

Olá! Sou o assistente da Loja GMV Tech. Como posso ajudar?

Digite o número da opção desejada:
1. Horario
2. Produto
3. Serviços
4. Agendamento
5. Pagamento
6. Entrega
7. Sugestão
8. Atendimento Humano
0. Sair

Sua escolha: 1
Você escolheu: Horario

Digite sua pergunta: Qual o expediente da loja?
Bot: Nosso horário de funcionamento é de segunda a sábado, das 9h às 18h.

Se você tem mais alguma pergunta, escolha uma opção:
...
