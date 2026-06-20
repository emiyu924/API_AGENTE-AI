from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv 

#leitura da chave de api
load_dotenv()
#criar o nosso app
app = Flask(__name__)
#habilitar o cors
CORS(app)
#criar agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel Deski, slogan: Aqui até a insônia dorme"
    "Você responde de forma clara e humorada, informações sobre quartos, serviços, reservas e preços" 
    "Quarto Standard ($500), Quarto Deluxe($700), Quarto Suíte Presidencial($1000)"
    "Temos a fidelidade que chamamos de membros, com os tipos: Plus (De acordo com a disponibilidade do hotel late checkout and early check-in, depois de 6 meses como membro a cada reserva algum mimo grátis) Premium (Garantido late checkout e early check-in )"
    "Com  relação aos serviços, oferecemos um concierge particular para os hóspedes que são membros Premium para cima, Piscina, Hidromassagem e Sauna, Sala de jogos e lazer (videogames, biblioteca, filmes, sala de lazer onde temos a mesa para jogos (ping pong), disponibilidade para xadrez entre outros) Restaurante 5 estrelas com a Chef Isabella renomada, e menu personalizado dependendo do dia",
    markdown=True
)

#criar a rota vazia e o método get
@app.route("/", methods=['GET'])
def testar():
    return jsonify({"Mensagem":"API funcionando"})
#criar a rota e o método POST
@app.route("/chat",methods=['POST'])
def pergunta():
    dados = request.get_json()
    pergunta = dados['pergunta']
    resposta = agente.run(pergunta)
    return jsonify({"resposta":resposta.content})

#rodar o app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)