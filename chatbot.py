import random
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import re

# Dados de exemplo
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
    ]
}


# Preparar os dados
perguntas = []
respostas = []

for intencao, frases in intencoes.items():
    for frase in frases:
        perguntas.append(frase)
        respostas.append(intencao)

# Vetorização e codificação
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(perguntas)

encoder = LabelEncoder()
y = encoder.fit_transform(respostas)

# Treinamento do modelo
modelo = MultinomialNB()
modelo.fit(X, y)

# Salvando os modelos
joblib.dump(vectorizer, 'vectorizer.joblib')
joblib.dump(encoder, 'encoder.joblib')
joblib.dump(modelo, 'modelo.joblib')

# Respostas automáticas
respostas_por_intencao = {
     "Horario": [
        "Nosso horário de funcionamento é de segunda a sábado, das 9h às 18h.",
        "Abrimos de segunda a sábado, das 9h às 18h, e não funcionamos aos domingos."
    ],
    "Produto": [
        "Trabalhamos com uma grande variedade de produtos, incluindo celulares, notebooks e acessórios.",
        "Temos celulares, notebooks, monitores e diversos acessórios disponíveis na loja."
    ],
    "Serviços": [
        "Sim, oferecemos assistência técnica e manutenção para computadores e celulares.",
        "Prestamos serviços como conserto, limpeza e suporte técnico em diversos equipamentos."
    ],
    "Agendamento": [
        "Sim, é possível agendar um atendimento pelo telefone ou pessoalmente na loja.",
        "Trabalhamos com agendamentos para serviços; entre em contato conosco para marcar."
    ],
    "Pagamento": [
        "Aceitamos dinheiro, cartão de débito/crédito, Pix e também parcelamos em até 6x.",
        "Você pode pagar com Pix, dinheiro ou cartão. Parcelamos dependendo do valor da compra."
    ],
    "Entrega": [
        "Realizamos entregas na cidade e também para regiões próximas, consulte a disponibilidade.",
        "Fazemos entregas com prazos que variam de acordo com a região e disponibilidade do produto."
    ]
}

def limpar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-zà-ú0-9\s]', '', texto)
    return texto

def responder(pergunta):
    pergunta_limpa = limpar_texto(pergunta)
    vetor = vectorizer.transform([pergunta_limpa])
    predicao = modelo.predict(vetor)
    intencao_prevista = encoder.inverse_transform(predicao)[0]
    resposta = random.choice(respostas_por_intencao.get(intencao_prevista, ['Desculpe, não entendi sua pergunta.']))
    
    return resposta

# Loop de conversa
print("Olá! Sou o assistente da Loja Tech. Como posso ajudar?")
print("Digite 'sair' para encerrar a conversa.\n")

while True:
    entrada = input("Você: ")
    if entrada.lower() == 'sair':
        print("Bot: Obrigado por conversar conosco. Até logo!")
        break
    resposta = responder(entrada)
    print(f"Bot: {resposta}")
