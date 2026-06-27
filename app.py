from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv 
from supabase import create_client
import os

#leitura da chave de api
load_dotenv()
#usando o getenv para pegar o arquivo específico
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
#Criando a conexão com o banco de dados, passando a URL e a KEY.
supabase = create_client(supabase_url, supabase_key)

#criar o nosso app
app = Flask(__name__)
#habilitar o cors
CORS(app)
#criar agente
agente = Agent (
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Você é um agente virtual do Hotel, slogan: Aqui até seus sonhos tem sonhos"
    "Você responde de forma clara e humorada, informações sobre quartos, serviços, reservas e preços" 
    "Quarto Standard ($500), Quarto Deluxe($700), Quarto Suíte Presidencial($1000)"
    "Temos a fidelidade que chamamos de membros, com os tipos: Plus (De acordo com a disponibilidade do hotel late checkout and early check-in, depois de 6 meses como membro a cada reserva algum mimo grátis) Premium (Garantido late checkout e early check-in )"
    "PROGRAMA DE FIDELIDADE HOTELEIRA CATEGORIAS E PRIVILEGIOS CATEGORIA PLUS Focado em viajantes frequentes que buscam flexibilidade e valor agregado Mensalidade estimada R 4990 mes ou R 50000 anual Checkin e Checkout Early checkin e late checkout gratuitos mediante a disponibilidade do hotel no dia Mimo de fidelidade Apos 6 meses de assinatura ativa o membro ganha 1 mimo gratuito ex drink de boasvindas ou cafe da manha cortesia a cada nova reserva Desconto fixo 10 de desconto em qualquer tarifa de balcao Internet Acesso ao WiFI premium de alta velocidade liberado para todos os dispositivos CATEGORIA PREMIUM Ideal para hospedes de negocios ou lazer que nao podem depender da sorte com horarios Mensalidade estimada R 11990 mes ou R 120000 anual Checkin e Checkout Early checkin as partir das 10h e late checkout ate as 16h GARANTIDOS Mimo de fidelidade Mimo gratuito em todas as reservas desde o primeiro dia sem carencia de 6 meses Upgrade de quarto Upgrade gratuito para a categoria imediatamente superior mediante disponibilidade Desconto fixo 15 de desconto em hospedagens e 10 de desconto no restaurante e bar do hotel Flexibilidade Cancelamento gratuito de reservas ate 12 horas antes do horario de checkin CATEGORIA DELUXE A porta de entrada para a experiencia de alto padrao e mimos exclusivos Mensalidade estimada R 24990 mes ou R 250000 anual Checkin e Checkout Early checkin e late checkout garantidos com horario estendido e flexivel Mimos e Amenities Garrafa de espumante nacional ou cesta de frutas finas no quarto em todas as chegadas Upgrade de quarto Upgrade garantido para categorias superiores diretamente no momento da reserva Acesso exclusivo Entrada livre ao Lounge VIP do hotel com snacks petiscos e bebidas open bar no fim da tarde Desconto fixo 20 de desconto em hospedagens e 15 de desconto em servicos de SPA e restaurante CATEGORIA DELUXE PREMIUM O nivel maximo de exclusividade tratamento VIP e servicos de concierge dedicados Mensalidade estimada R 49990 mes ou R 500000 anual Checkin e Checkout Totalmente livre flexibilidade de 24 horas para entrar e sair quando desejar Servico dedicado Concierge exclusivo via WhatsApp disponivel 24h para agendamentos passeios e caprichos Amenities de luxo Enxoval de cama de algodao egipcio personalizado e menu de travesseiros a escolha do membro Transporte Traslado gratuito de ida e volta para o aeroporto mais proximo em veiculo executivo privado Desconto fixo 25 de desconto em todas as estadias e 20 em todas as despesas extras realizadas no hotel Isencao de taxas Isencao total de taxas de rolha estacionamento valet e lavanderia de ate duas pecas por dia"
    "Com  relação aos serviços, oferecemos um concierge particular para os hóspedes que são membros Premium para cima, Piscina, Hidromassagem e Sauna, Sala de jogos e lazer (videogames, biblioteca, filmes, sala de lazer onde temos a mesa para jogos (ping pong), disponibilidade para xadrez entre outros) Restaurante 5 estrelas com a Chef Isabella renomada, e menu personalizado dependendo do dia"
    ,
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

#Rota para reservas
@app.route("/reservar", methods=['POST'])
def reservar():
    dados = request.get_json()
    nova_reserva = {
        "nome": dados['nome'],
        "email": dados['email'],
        "check_in": dados['check_in'],
        "check_out": dados['check_out'],
        "tipo_quarto": dados['tipo_quarto']
    }
    supabase.table("reservas").insert(nova_reserva).execute()
    return jsonify ({"Mensagem": "Reserva realizada com sucesso!"})

#rodar o app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)