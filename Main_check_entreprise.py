import requests
from bs4 import BeautifulSoup
import json


url = 'https://www.boursorama.com/bourse/actions/cotations/?quotation_az_filter%5Bmarket%5D=1rPCAC'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tr_tag = soup.find_all('tr', class_="c-table__row")
    # for tag in tr_tag :
    #     print(len(tag))
    #     print('________')
print(len(tr_tag))
#     id_action_list = []
    
#     for tag in tr_tag : 
#         # ID de l'action
#         action_id = tag['data-ist'] 
#         id_action_list.append(action_id)
        
#         # Categorie de l'action 
#         if tag['data-ist-init'] :
#             category_tag = tag['data-ist-init']
#             category_tag_to_dict = json.loads(category_tag)
#             action_category = category_tag_to_dict['category']
#             print(action_category)
#             print(id_action_list)
#         else :
#             print(tag)
#             break
        
#         # Nom de l'Action
#         title_tag = tag.find('a', title=True)
#         action_name = title_tag['title']
#         print('__________________')
# print(len(id_action_list))
# print(id_action_list)
        
