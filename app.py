import os, sys
from flask import Flask, render_template, request
from utils import wit_response
from pymessenger import Bot


app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAE18RIylZC4BO2bJC9GbRJsizuW3xwF9nn5hEY1tYBqaswgSPJZB0t6VxycS0zBq83Fh0TmZCHuG3nXCPs7VPvanDuuFHCOMWpGMEuKDsd7LhhRCYoL11W1XDk69KIXVUStYBumtzhADV91rQd5NUPR9zr1QM6Xv4yWOZCnHLZCUQckBvsGNth7lpFzMOmZCcQcTICc2B"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	#Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return render_template('index.html'), 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
            
            # IDS
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
                
                response = None

                entity, value = wit_response(messaging_text)

                if entity == 'morning:morning':
                     response = "{} cher(e) client(e) puis je savoir votre nom s'il vous plait ?".format(str(value))

                elif entity == 'afternoon:afternoon':
                     response = "{} cher(e) client(e) puis je savoir votre nom s'il vous plait ?".format(str(value))
                     
                elif entity == 'greeting:greeting':
                     response = "{} cher(e) client(e) puis je savoir votre nom s'il vous plait ?".format(str(value))

                elif entity == 'present:present':
                     response = "Bievenue {} puis je vous aider ?".format(str(value))

                elif entity == 'promo:promo':
                     response = "Oui nous avons tous les jours quelques produits en promotion, voici la liste de quelques"\
                                "promotions d'aujourd'hui: Mocassin 100 % en cuir à 29 900 FCFA au lieu de 39 900 FCFA ; "\
                                "Sac de voyage à 8 990 FCFA au lieu de 13 990 FCFA et beaucoup d'autres, pour en savoir "\
                                "d'avantage, merci de visiter notre site à tavers le lien suivant : https://be68-89-39-106-228.ngrok-free.app!"
                
                elif entity == 'newstype:newstype':
                     response = "D'accord. On va vous envoyer des {} ".format(str(value))
                     
                elif entity == 'order:order':
                     response = "D'accord, ça sera ajouté dans votre panier avec plaisir. Donnez votre adresse et votre numéro de téléphone s'il vous plait !"

                elif entity == 'office:office':
                     response = "Notre siège se trouve à Colobane en face de la pharmacie Lebou."

                elif entity == 'activity:activity':
                     response = "Witshop est une entreprise innovante dans le domaine de la mode, créée en 2020 pour répondre aux "\
                                "besoins des consommateurs modernes à la recherche de produits élégants et intelligemment conçus. "\
                                "Spécialisée dans la vente de chaussures, sacs, tissus, vêtements (t-shirts, pantalons), et autres "\
                                "accessoires, Witshop se distingue par son engagement envers la créativité, la qualité et la satisfaction"\
                                " client. Chez Witshop, nous accordons une importance primordiale à l'expérience client. Notre équipe "\
                                "dévouée est là pour fournir un service exceptionnel, des conseils de mode personnalisés et des options "\
                                "de livraison pratiques pour garantir une satisfaction totale. Witshop est bien plus qu'un simple magasin "\
                                "de mode. C'est un lieu où l'élégance rencontre l'innovation, et où chaque achat raconte une histoire de "\
                                "style et de qualité. Rejoignez-nous pour découvrir une nouvelle façon de vivre la mode avec intelligence."     

                elif entity == "location:location":
                     response = "D'accord. Donc vous habitez à {0}, ça marche, on vous enverra très bientot un livreur à {0} qui vous contactera une fois arrivé à {0} ".format(str(value))

                elif entity == 'aurevoir:aurevoir':
                     response = "Merci pour la visite à très bientot !!!"

                elif entity == 'thank:thank':
                     response = "Je vous en prie cher(e) client(e) sachez que je suis là uniquement pour votre satisfaction !"

                if response == None:
                     response = "Désolé, je n'arrive pas à vous comprendre"

                bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
    app.run(debug=True, port=80)