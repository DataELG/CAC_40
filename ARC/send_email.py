import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


# def send_email_with_attachment(file_path) :
    
#     # Chargement des variables d'environnement
#     load_dotenv()

#     expediteur = os.getenv('EMAIL')
#     mot_de_passe = os.getenv('PASSWORD')
#     destinataire = os.getenv('RECIPIENT')

#     # Création de l'objet de message
#     msg = MIMEMultipart()
#     msg['From'] = expediteur
#     msg['To'] = destinataire
#     msg['Subject'] = 'Compte rendu quotidien des actions en bourse'


#     # Corps de l'e-mail
#     corps = 'Bonjour, Voici le CR des actions du jour'
#     msg.attach(MIMEText(corps, 'plain'))

#     # Fichier à joindre
#     fichier = file_path

#     # Ajouter la pièce jointe
#     try:
#         with open(fichier, 'rb') as attachment:
#             part = MIMEBase('application', 'octet-stream')
#             part.set_payload(attachment.read())
#             encoders.encode_base64(part)
#             part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(fichier)}')
#             msg.attach(part)
#     except Exception as e:
#         exit()

#     # Connexion au serveur SMTP et envoi de l'e-mail
#     try:
#         serveur = smtplib.SMTP('smtp.office365.com', 587)
#         serveur.starttls()
#         serveur.login(expediteur, mot_de_passe)
#         texte = msg.as_string()
#         serveur.sendmail(expediteur, destinataire, texte)
#         serveur.quit()
#         print('E-mail envoyé avec succès')
#     except smtplib.SMTPAuthenticationError as e:
#         print(f'Erreur lors de l\'authentification: {e}')
#     except Exception as e:
#         print(f'Erreur lors de l\'envoi de l\'e-mail: {e}')

# import os
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# from io import BytesIO
# from dotenv import load_dotenv
# import logging

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     # Optionnel: Charger les variables d'environnement si besoin
#     load_dotenv()

#     expediteur = os.getenv('EMAIL')
#     mot_de_passe = os.getenv('PASSWORD')
#     destinataire = os.getenv('RECIPIENT')

#     # Création de l'objet de message
#     msg = MIMEMultipart()
#     msg['From'] = expediteur
#     msg['To'] = destinataire
#     msg['Subject'] = 'Compte rendu quotidien des actions en bourse'

#     # Corps de l'e-mail
#     corps = 'Bonjour, Voici le CR des actions du jour'
#     msg.attach(MIMEText(corps, 'plain'))

#     # Génération de la pièce jointe en mémoire
#     data = "Ceci est un exemple de rapport généré en mémoire."
#     fichier_en_memoire = BytesIO()
#     fichier_en_memoire.write(data.encode('utf-8'))
#     fichier_en_memoire.seek(0)

#     # Ajouter la pièce jointe
#     part = MIMEBase('application', 'octet-stream')
#     part.set_payload(fichier_en_memoire.read())
#     encoders.encode_base64(part)
#     part.add_header('Content-Disposition', f'attachment; filename="rapport.txt"')
#     msg.attach(part)

#     # Connexion au serveur SMTP et envoi de l'e-mail
#     try:
#         serveur = smtplib.SMTP('smtp.office365.com', 587)
#         serveur.starttls()
#         serveur.login(expediteur, mot_de_passe)
#         texte = msg.as_string()
#         serveur.sendmail(expediteur, destinataire, texte)
#         serveur.quit()
#         logging.info('E-mail envoyé avec succès')
#         return func.HttpResponse("E-mail envoyé avec succès.", status_code=200)
#     except smtplib.SMTPAuthenticationError as e:
#         logging.error(f'Erreur lors de l\'authentification: {e}')
#         return func.HttpResponse(f'Erreur lors de l\'authentification: {e}', status_code=500)
#     except Exception as e:
#         logging.error(f'Erreur lors de l\'envoi de l\'e-mail: {e}')
#         return func.HttpResponse(f'Erreur lors de l\'envoi de l\'e-mail: {e}', status_code=500)

from test import *
html_table = viz() 



def send_email_with_attachment(html_table) :
    
    # Chargement des variables d'environnement
    load_dotenv()

    sender = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    receiver = os.getenv('RECIPIENT')

    # Création de l'objet de message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Rapport du Marché - Variation des Actions'

    # Sujet et corps de l'email
    body = f"""
    <h2>Bonjour,</h2>
    <p>Voici le rapport des variations de prix et de volumes pour aujourd'hui :</p>
    {html_table}
    <p>Cordialement,<br>DataTradeX</p>
    """

    # Attacher le corps de l'email
    msg.attach(MIMEText(body, 'html'))

    # Connexion au serveur SMTP et envoi de l'email
    try:
        server = smtplib.SMTP('smtp.office365.com', 587) 
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")
        
send_email_with_attachment(html_table)