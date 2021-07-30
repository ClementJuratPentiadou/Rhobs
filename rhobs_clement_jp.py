from pymongo import MongoClient
from pprint import pprint

from dateutil import parser
from datetime import date

client = MongoClient(
    "15.236.51.148",
    username="rhobs",
    password="xeiPhie3Ip8IefooLeed0Up6",
    authSource="rhobs",
    authMechanism="SCRAM-SHA-1",
)

db = client.rhobs.test
tout = list(db.find())

def musiques():

    dico_music = {}

    for i in range(db.estimated_document_count()):

        list_music_perso = list(tout[i].items())[1][1]['music']

        if type(list_music_perso) != list:
            list_music_perso = [list_music_perso]

        for x in list_music_perso:

            if not x in dico_music:
                dico_music[x] = 1
            else:
                dico_music[x] += 1

    final = sorted(dico_music.items(), key=lambda x: x[1], reverse=True)

    i=1
    for (x,y) in final:
        print(i, "-", x, "|", y, "auditeurs")
        i=i+1

def calculate_age(date_yyyymmdd):

    born = parser.parse(date_yyyymmdd)
    today = date.today()
    
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def ages():

    dico_music = {}

    for i in range(db.estimated_document_count()):

        donnees = list(tout[i].items())[1][1]
        list_music_perso = donnees['music']
        age = calculate_age(donnees['birthdate'])

        if type(list_music_perso) != list:
            list_music_perso = [list_music_perso]

        for x in list_music_perso:

            if not x in dico_music:
                dico_music[x] = [1, age]
            else:
                dico_music[x][0] += 1
                dico_music[x][1] += age

    dico_age = {}

    for x in dico_music.items():
        dico_age[x[0]] = round(x[1][1]/x[1][0])

    final = sorted(dico_age.items(), key=lambda x: x[1])

    i=1
    for (x,y) in final:
        print(i, "-", x, "|", y, "ans en moyenne")
        i=i+1

def pyramide(city, age_slice):

    print("Ville de", city, "| Slice de", age_slice, "ans")

    dico_pyramide = {}

    for i in range(db.estimated_document_count()):

        donnees = list(tout[i].items())[1][1]
        ville = donnees['city']
        age = calculate_age(donnees['birthdate'])

        if ville == city:

            age_min = age//age_slice*age_slice

            if not age_min in dico_pyramide:
                dico_pyramide[age_min] = 1
            else:
                dico_pyramide[age_min] += 1

    final = sorted(dico_pyramide.items(), key=lambda x: x[0])

    i=0
    for (x,y) in final:
        
        while x != i:
            print(i, "-", i+age_slice-1, "|", "None")
            i += age_slice
            
        print(x, "-", x+age_slice-1, "|", y, "personnes")
        i += age_slice

musiques()
print("")
ages()
print("")
pyramide('Gay', 5)
