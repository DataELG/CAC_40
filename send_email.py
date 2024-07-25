import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os


def send_email_with_attachment(file_path) :
    
    # Chargement des variables d'environnement
    load_dotenv()

    expediteur = os.getenv('EMAIL')
    mot_de_passe = os.getenv('PASSWORD')
    destinataire = os.getenv('RECIPIENT')

    # Création de l'objet de message
    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = destinataire
    msg['Subject'] = 'Compte rendu quotidien des actions en bourse'


    # Corps de l'e-mail
    corps = 'Bonjour, Voici le CR des actions du jour'
    msg.attach(MIMEText(corps, 'plain'))

    # Fichier à joindre
    fichier = file_path

    # Ajouter la pièce jointe
    try:
        with open(fichier, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(fichier)}')
            msg.attach(part)
    except Exception as e:
        exit()

    # Connexion au serveur SMTP et envoi de l'e-mail
    try:
        serveur = smtplib.SMTP('smtp.office365.com', 587)
        serveur.starttls()
        serveur.login(expediteur, mot_de_passe)
        texte = msg.as_string()
        serveur.sendmail(expediteur, destinataire, texte)
        serveur.quit()
        print('E-mail envoyé avec succès')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Erreur lors de l\'authentification: {e}')
    except Exception as e:
        print(f'Erreur lors de l\'envoi de l\'e-mail: {e}')
