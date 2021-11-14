# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 17:30:29 2021

@author: agnes
"""

'''Program to read a list of anonymized logs from a file 
and calculate a feature vector for each user by saving the data in json format
Expected json data: a list of log with the following fields:
- Data/Ora
- Identificativo unico dell’utente
- Contesto dell’evento
- Componente
- Evento
- Descrizione
- Origine 
- Indirizzo IP

Feature per ogni utente : 
    -data primo evento 
    -data ultimo evento
'''

import json
import sys



# sottoprogramma che legge il file in formato json e crea una lista di liste (lista di log)
def read_json_file(file_name):
    """
    :param file_name: file da leggere
    :return: lista di liste (lista di log)
    """
    try:
        fin = open(file_name)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except:
        print('*** errore *** Non è stato trovato nessun file')
        sys.exit()

#sottoprogramma per scrivere sul file json
def write_json_file(data, file_name, indnt=3):
    """
    :param data: oggetto python che deve essere scritto sul file
    :param file_name: file su cui screvere
    :param indent:
    :return: None
    """
    try:
        fout = open(file_name, 'w')
        json.dump(data, fout, indent=indnt)
        fout.close()
    except:
        print('*** errore *** La scrittura sul file non è andata a buon fine')
        sys.exit()

        




#log[1] : codice identificativo utente 
#sottoprogramma che conta le occorrenze totali di ogni utente dalla lista di log
def tot_occurrences(log_list):
    '''

    :param log_list: lista di log
    :return: dizionario che conta tutte le occorrenze per ogni utente, 
             in cui è presente un 
             dizionario che ha come nome il codice identificativo dell' utente
    '''
    tab_tot_occurences = {}
    for log in log_list:
        if not log[1] in tab_tot_occurences:
            tab_tot_occurences[(log[1])]= {} #dizionario di codici identificativi
            tab_tot_occurences[(log[1])]['tot_occurences']=1
        else:
            tab_tot_occurences[log[1]]['tot_occurences']+=1
    return tab_tot_occurences




#sottoprogramma che calcola le occorrenze per ogni evento
#il conteggio avviene nel dizionario che ha come nome il codice identificativo dell'utente
#il sottoprogramma restituisce il dizionario tab_tot_occurences aggiornato 
#log[4] : evento 
''' '''
def event_occurences(log_list, tab_tot_occurences):
    '''
    calcola le occorrenze per ogni evento
    :param log_list: a list of logs
    :param tab_tot_occurences
    :return: l'elenco dei log e lo stesso dizionario
             con le occorrenze per ogni evento
    '''
    
    for log in log_list:
        if not log[4] in tab_tot_occurences[log[1]]:
            tab_tot_occurences[log[1]][log[4]]=1 
            
        else:
            tab_tot_occurences[log[1]][log[4]]+=1
    return tab_tot_occurences





#sottoprogramma che trova le date degli eventi per ogni utente 
#in corrispondenza della chiave 'dates' ci sarà una lista di date 
#per ognuna delle quali c'è stato un evento
def dates_of_occurences(tab_tot_occurences):
    '''

    :param tab_tot_occurences: dictionary of dictionary with user codes,
             total occurences per user and occurences for each event
    :return: the same dictionary with all dates on which the user performs an event
    '''
    for key in tab_tot_occurences:
        tab_tot_occurences[key]['dates']=[] 
        #dates è di tipo lista
        for log in log_list:
            data = log[0].split() 
            if log[1]==key:
                tab_tot_occurences[key]['dates']+=[data[0]]
    return tab_tot_occurences



def x(tab_tot_occurences):
    for key in tab_tot_occurences:
        date_eventi = tab_tot_occurences[key]['dates'] #lista di date
        tab_tot_occurences[key]['last_date']=date_eventi[0] 
        tab_tot_occurences[key]['first_date']=date_eventi[-1]
    return tab_tot_occurences
                        

filein = input('insert path of the json file to analyze:') 
#C:\Users\agnes\OneDrive\Desktop\analizza_log_21-22\indata\logs_Fondamenti di informatica [20-21]_20211103-1845_anonymized.json
log_list = read_json_file(filein)
tab_tot_occurences = tot_occurrences(log_list)
tab_tot_occurences = event_occurences(log_list, tab_tot_occurences)
tab_tot_occurences = dates_of_occurences(tab_tot_occurences)
tab_tot_occurences = x(tab_tot_occurences)
write_json_file(tab_tot_occurences,'newfile.json', indnt=3)
# il risultato viene salvato come un file chiamato newfile.json

print('Fine')
