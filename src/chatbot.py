# Importação de bibliotecas essenciais
import random                           # Usado para escolher respostas aleatórias
import joblib                           # Usado para carregar modelos treinados salvos
import re                               # Usado para limpar o texto do usuário (remoção de caracteres especiais)
from sklearn.feature_extraction.text import TfidfVectorizer  # Representa texto como vetores numéricos
from sklearn.preprocessing import LabelEncoder               # Codifica/decodifica rótulos de classes (intenções)
from sklearn.naive_bayes import MultinomialNB                # Algoritmo de classificação usado no modelo

# Carregamento dos modelos treinados anteriormente
vectorizer = joblib.load('./data/modelos/vectorizer.joblib')   # TF-IDF vectorizer treinado
encoder = joblib.load('./data/modelos/encoder.joblib')         # Codificador de intenções
modelo = joblib.load('./data/modelos/modelo.joblib')           # Classificador Naive Bayes treinado

# Base de intenções com exemplos de perguntas
intencoes = {
    "Horario": [
        "Qual é o horário de funcionamento da loja?",
        "A loja abre aos sábados?",
        "Vocês funcionam aos domingos?",
        "Que horas vocês fecham?",
        "Qual o expediente da loja?"
    ], 
    "Produto": [
        "Vocês vendem celulares?",
        "Quais produtos estão disponíveis?",
        "Tem notebook à venda?",
        "Vocês trabalham com acessórios para computador?",
    ],     
    "Serviços": [ 
        "Vocês consertam computadores?",
        "A loja oferece assistência técnica?",
        "Fazem manutenção em celulares?",
        "Vocês oferecem suporte técnico?",
        "Realizam limpeza de notebook?"
    ],
    "Agendamento": [
        "Posso marcar um horário para atendimento?",
        "É possível agendar manutenção?",
        "Vocês fazem atendimento com hora marcada?",
        "Consigo agendar pelo telefone?"
    ],
    "Pagamento": [ 
        "Quais formas de pagamento vocês aceitam?",
        "Posso pagar com cartão de crédito?",
        "Vocês parcelam as compras?",
        "Aceitam Pix?",
        "Dá pra pagar em dinheiro?"
    ],
    "Entrega": [
        "Vocês fazem entregas?",
        "Qual o prazo de entrega?",
        "Vocês entregam no mesmo dia?",
        "Fazem entrega para fora da cidade?"
    ],
    "Sugestão": [
        "Pode me sugerir um produto?",
        "Qual produtos você recomenda?",
        "O que você indica para um bom custo-benefício?",
        "Qual produto mais vendido da loja?"
    ],
    "Atendimento Humano": [
        "Quero falar com um atendente.",
        "Pode me transferir para um humano?",
        "Preciso de atendimento humano.",
        "Tem como falar com alguém da loja?",
        "Quero falar com uma pessoa, não com o robô."
    ]
}

# Respostas possíveis para cada intenção
respostas_por_intencao = {
    "Horario": ["Nosso horário de funcionamento é de segunda a sábado, das 9h às 18h."],
    "Produto": ["Temos celulares, notebooks, monitores e diversos acessórios disponíveis na loja."],
    "Serviços": ["Sim, oferecemos assistência técnica e manutenção para computadores e celulares."],
    "Agendamento": ["Sim, é possível agendar um atendimento pelo telefone ou pessoalmente na loja."],
    "Pagamento": ["Aceitamos dinheiro, cartão de débito/crédito, Pix e também parcelamos em até 6x."],
    "Entrega": ["Fazemos entregas em todo o território brasileiro, com prazos e valor de frete que variam de acordo com a região e disponibilidade do produto."],
    "Sugestão": ["Recomendamos os nossos notebooks da linha Dell Inspiron, com ótimo desempenho e preço acessível."],
    "Atendimento Humano": ["Claro! Você pode entrar em contato com um atendente pelo telefone (11) 99999-9999."]
}

# Mensagem exibida ao encerrar o atendimento
MENSAGEM_DESPEDIDA = (
    "\n---------------------------------------------------------\n"
    "Bot: Agradecemos pela conversa! Se precisar de algo, estaremos por aqui. Até logo!\n"
    "---------------------------------------------------------\n"
)

# Função que limpa e padroniza a entrada do usuário
def limpar_texto(texto):
    texto = texto.lower()  # Converte para minúsculas
    texto = re.sub(r'[^a-zà-ú0-9\s]', '', texto)  # Remove pontuação
    return texto

# Função que exibe a mensagem de saída e finaliza o programa
def mensagem_despedida():
    print(MENSAGEM_DESPEDIDA)
    exit()

# Função que analisa a pergunta e retorna uma resposta adequada
def responder(pergunta, intencao_escolhida):
    pergunta_limpa = limpar_texto(pergunta)

    if pergunta.strip() == '0':  # Encerrar se o usuário digitar "0"
        mensagem_despedida()

    vetor = vectorizer.transform([pergunta_limpa])        # Vetoriza a pergunta
    predicao = modelo.predict(vetor)                      # Faz a previsão da intenção
    intencao_prevista = encoder.inverse_transform(predicao)[0]  # Decodifica a intenção prevista

    if intencao_prevista == intencao_escolhida:
        # Intenção prevista bate com a escolhida: responder diretamente
        return random.choice(respostas_por_intencao[intencao_prevista])
    else:
        # Intenção prevista diferente: sugerir perguntas relacionadas à intenção escolhida
        print("\n---------------------------------------------------------")
        print("Bot: Parece que sua pergunta não foi reconhecida. Aqui estão algumas opções relacionadas ao tópico escolhido:")
        print("---------------------------------------------------------\n")
        perguntas_sugeridas = intencoes[intencao_escolhida]
        for idx, pergunta_exemplo in enumerate(perguntas_sugeridas, start=1):
            print(f"{idx}. {pergunta_exemplo}")
        print("0. Voltar para o menu")

        # Usuário escolhe uma sugestão ou volta ao menu
        while True:
            escolha_pergunta = input("\nInsira o número correspondente: ").strip()
            if escolha_pergunta == '0':
                return "voltar_menu"
            elif escolha_pergunta.isdigit() and 1 <= int(escolha_pergunta) <= len(perguntas_sugeridas):
                return random.choice(respostas_por_intencao[intencao_escolhida])
            else:
                print("\n---------------------------------------------------------")
                print("Número inválido. Tente novamente.")
                print("---------------------------------------------------------")

# Função principal do chatbot (interface de interação com o usuário)
def chatbot():
    intencoes_lista = list(intencoes.keys())  # Lista das intenções disponíveis

    while True:
        # Exibe o menu principal
        print("\nOlá! Sou o assistente da Loja GMV Tech. Como posso ajudar?")
        print("\nDigite o número da opção desejada para iniciarmos o atendimento:\n")
        for idx, item in enumerate(intencoes_lista, start=1):
            print(f"{idx}. {item}")
        print("0. Sair\n")

        escolha = input("Sua escolha: ").strip()
        if escolha == '0':
            mensagem_despedida()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(intencoes_lista):
            intencao_escolhida = intencoes_lista[int(escolha) - 1]
            print(f"Você escolheu: {intencao_escolhida}")

            while True:
                # Usuário digita a pergunta dentro da intenção escolhida
                entrada = input("\nDigite a sua pergunta: ").strip()
                if entrada == '0':
                    mensagem_despedida()

                resposta = responder(entrada, intencao_escolhida)

                if resposta == "voltar_menu":
                    break  # Retorna ao menu principal
                elif resposta:
                    print("\n---------------------------------------------------------")
                    print(f"Bot: {resposta}")
                    print("---------------------------------------------------------")

                    # Oferece ao usuário a opção de continuar ou encerrar
                    print("\nPodemos te ajudar em algo mais?\n")
                    print("1. Sim. Desejo fazer uma nova pergunta")
                    print("2. Encerrar conversa\n")
                    escolha_final = input("Você escolheu: ").strip()
                    if escolha_final == '2':
                        mensagem_despedida()
                    elif escolha_final == '1':
                        break
                    else:
                        print("\nOpção inválida. Retornando ao menu principal.")
                        break
                else:
                    print("\n---------------------------------------------------------")
                    print("Retornando ao menu principal...")
                    print("---------------------------------------------------------")
                    break
        else:
            print("\n---------------------------------------------------------")
            print("Opção inválida. Tente novamente.")
            print("---------------------------------------------------------")

# Início da aplicação
chatbot()
