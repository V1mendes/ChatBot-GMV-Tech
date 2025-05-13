import random
import joblib
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB

# Carregar modelos treinados
vectorizer = joblib.load('./data/modelos/vectorizer.joblib')
encoder = joblib.load('./data/modelos/encoder.joblib')
modelo = joblib.load('./data/modelos/modelo.joblib')

# Intenções cadastradas
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
        "Posso comprar um monitor aí?"
    ],
    "Serviços": [
        "Vocês consertam computadores?",
        "A loja oferece assistência técnica?",
        "Fazem manutenção em celulares?",
        "Vocês oferecem suporte técnico?",
        "Realizam limpeza de notebook?"
    ],
    "Agendamento": [
        "Preciso marcar um horário para atendimento?",
        "Como agendo um serviço?",
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
        "A loja entrega produtos comprados?",
        "Vocês entregam no mesmo dia?",
        "Fazem entrega para fora da cidade?"
    ],
    "Sugestão": [
        "Pode me sugerir um produto?",
        "Quais produtos você recomenda?",
        "Tem alguma sugestão de compra?",
        "O que você indica para um bom custo-benefício?",
        "Quais os mais vendidos?"
    ],
    "Atendimento Humano": [
        "Quero falar com um atendente.",
        "Pode me transferir para um humano?",
        "Preciso de atendimento humano.",
        "Tem como falar com alguém da loja?",
        "Quero falar com uma pessoa, não com o robô."
    ]
}

respostas_por_intencao = {
    "Horario": ["Nosso horário de funcionamento é de segunda a sábado, das 9h às 18h."],
    "Produto": ["Temos celulares, notebooks, monitores e diversos acessórios disponíveis na loja."],
    "Serviços": ["Sim, oferecemos assistência técnica e manutenção para computadores e celulares."],
    "Agendamento": ["Sim, é possível agendar um atendimento pelo telefone ou pessoalmente na loja."],
    "Pagamento": ["Aceitamos dinheiro, cartão de débito/crédito, Pix e também parcelamos em até 6x."],
    "Entrega": ["Fazemos entregas com prazos que variam de acordo com a região e disponibilidade do produto."],
    "Sugestão": ["Recomendamos os nossos notebooks da linha Dell Inspiron, com ótimo desempenho e preço acessível."],
    "Atendimento Humano": ["Claro! Você pode entrar em contato com um atendente pelo telefone (11) 99999-9999."]
}

def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-zà-ú0-9\s]', '', texto)
    return texto

def responder(pergunta, intencao_escolhida):
    pergunta_limpa = limpar_texto(pergunta)
    
    if pergunta.strip() == '0':  # Se o usuário inserir '0', encerramos o chat
        print("\nBot: Atendimento encerrado. Até logo!")
        exit()

    vetor = vectorizer.transform([pergunta_limpa])
    predicao = modelo.predict(vetor)
    intencao_prevista = encoder.inverse_transform(predicao)[0]

    if intencao_prevista == intencao_escolhida:
        return random.choice(respostas_por_intencao[intencao_prevista])
    else:
        print("\nBot: Parece que sua pergunta não foi reconhecida. Aqui estão algumas opções relacionadas ao seu tópico escolhido:")
        perguntas_sugeridas = intencoes[intencao_escolhida]
        for idx, pergunta_exemplo in enumerate(perguntas_sugeridas, start=1):
            print(f"{idx}. {pergunta_exemplo}")
        print("0. Voltar para o menu")
        
        while True:
            escolha_pergunta = input("Escolha uma pergunta: ").strip()
            if escolha_pergunta == '0':
                return None  # Voltar ao menu principal
            elif escolha_pergunta.isdigit() and 1 <= int(escolha_pergunta) <= len(perguntas_sugeridas):
                pergunta_certa = perguntas_sugeridas[int(escolha_pergunta) - 1]
                return random.choice(respostas_por_intencao[intencao_escolhida])
            else:
                print("Número inválido. Tente novamente.")

def chatbot():
    intencoes_lista = list(intencoes.keys())

    while True:
        print("\nOlá! Sou o assistente da Loja GMV Tech. Como posso ajudar?")
        print("\nDigite o número da opção desejada para iniciarmos o atendimento:")
        for idx, item in enumerate(intencoes_lista, start=1):
            print(f"{idx}. {item}")
        print("0. Sair\n")

        escolha = input("Sua escolha: ").strip()
        if escolha == '0':
            print("\nBot: Obrigado por conversar conosco. Até logo!")
            exit()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(intencoes_lista):
            intencao_escolhida = intencoes_lista[int(escolha) - 1]
            print(f"Você escolheu: {intencao_escolhida}")
            
            while True:
                entrada = input("\nDigite sua pergunta ou insira um número: ").strip()
                if entrada == '0':
                    print("\nBot: Atendimento encerrado. Até logo!")
                    exit()

                resposta = responder(entrada, intencao_escolhida)
                if resposta:
                    print("\nBot:", resposta)
                else:
                    print("\nRetornando ao menu principal...")
                    break

                print("\nSe você possui mais alguma pergunta, escolha uma das opções abaixo:")
                for idx, item in enumerate(intencoes_lista, start=1):
                    print(f"{idx}. {item}")
                print("0. Sair\n")
        else:
            print("\nOpção inválida. Tente novamente.")

chatbot()
