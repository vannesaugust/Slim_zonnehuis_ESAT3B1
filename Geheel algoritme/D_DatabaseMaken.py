import csv
import sqlite3
#######################################################################################################################
# Altijd connecteren met de database als je deze wilt gebruiken
con = sqlite3.connect("D_VolledigeDatabase.db")
# Code die nodig is om de andere opdrachten te kunnen laten runnen
cur = con.cursor()
#######################################################################################################################
# Aparte tabellen maken met een het aantal kolommen dat je wilt
cur.execute("CREATE TABLE Stroomprijzen(DatumBelpex, Prijs)")
cur.execute("CREATE TABLE Weer(DatumWeer, Windsnelheid, Temperatuur, RadiatieDirect, RadiatieDiffuse)")
cur.execute("CREATE TABLE Geheugen(Nummering, Apparaten, Wattages, ExacteUren, BeginUur, FinaleTijdstip, UrenWerk,\
                                   UrenNaElkaar, SoortApparaat, Capaciteit, RememberSettings, Status, VerbruikPerApparaat, Aanpassing, UurVanToevoeging, LijstenLeds)")
cur.execute("CREATE TABLE OudGeheugen(Nummering, Apparaten, Wattages, ExacteUren, BeginUur, FinaleTijdstip, UrenWerk,\
                                   UrenNaElkaar, SoortApparaat, Capaciteit, RememberSettings, Status, VerbruikPerApparaat, Aanpassing, UurVanToevoeging, LijstenLeds)")
cur.execute("CREATE TABLE ToegevoegdGeheugen(Nummering, Apparaten, Wattages, ExacteUren, BeginUur, FinaleTijdstip, UrenWerk,\
                                   UrenNaElkaar, SoortApparaat, Capaciteit, RememberSettings, Status, VerbruikPerApparaat, Aanpassing, UurVanToevoeging,LijstenLeds)")
cur.execute("CREATE TABLE RememberSettingsGeheugen(Nummering, Apparaten, Wattages, ExacteUren, BeginUur, FinaleTijdstip, UrenWerk,\
                                   UrenNaElkaar, SoortApparaat, Capaciteit, RememberSettings, Status, VerbruikPerApparaat, Aanpassing, UurVanToevoeging, LijstenLeds)")
cur.execute("CREATE TABLE InfoLijsten24uur(Nummering, VastVerbruik)")
cur.execute("CREATE TABLE Zonnepanelen(Aantal, Oppervlakte, Rendement)")
cur.execute("CREATE TABLE Batterijen(NaamBatterij, MaxEnergie, OpgeslagenEnergie, Laadvermogen, Batterijvermogen)")
cur.execute("CREATE TABLE Huisgegevens(TemperatuurHuis, MinTemperatuur, MaxTemperatuur, VerbruikWarmtepomp, COP , \
                                       UWaarde, OppervlakteMuren, VolumeHuis, Kost, KostMetOptimalisatie, KostZonderOptimalisatie, \
                                       StatusWarmtepomp, TotaalVerbruikWarmtepomp)")
cur.execute("CREATE TABLE ExtraWaarden(SentinelOptimalisatie, SentinelInterface, HuidigeDatum, HuidigUur, SentinelOptimalisatie2)")
#######################################################################################################################
# CSV-bestanden open, dit kan door de import van csv
with open("D_CSV_Belpex2021-2022.csv", 'r') as file:
    # Gaat rij per rij af en splits de gegevens wanneer het de puntkomma tegenkomt
    csvreaderBelpex = csv.reader(file, delimiter=';')
    # Houdt 2 kolommen over en elk komt op een plaats van een vraagteken
    cur.executemany("INSERT INTO Stroomprijzen VALUES(?, ?)", csvreaderBelpex)
with open("D_CSV_WeatherData.csv", 'r') as file:
    csvreaderWeather = csv.reader(file)
    cur.executemany("INSERT INTO Weer VALUES(?, ?, ?, ?, ?)", csvreaderWeather)
# Op deze manier kunnen er maximaal 10 apparaten toegevoegd worden
#######################################################################################################################
lengte = 15
# Aanmaken van een nul matrix
ZeroMatrix = []
for i in range(lengte):
    # In de eerste kolom is een nummering nodig om later naar de juiste positie te verwijzen
    Row = [i]
    # Range(13) want er zijn 14 kolommen die aangemaakt moeten worden
    for i2 in range(15):
        # Geven alles voorlopig een nul om later via de interface het deze plaatste te vervangen naar het juiste
        Row.append(0)
    ZeroMatrix.append(Row)
cur.executemany("INSERT INTO Geheugen VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ZeroMatrix)
#######################################################################################################################
cur.execute("INSERT INTO OudGeheugen SELECT * FROM Geheugen")
#######################################################################################################################
cur.execute("INSERT INTO ToegevoegdGeheugen SELECT * FROM Geheugen")
#######################################################################################################################
cur.execute("INSERT INTO RememberSettingsGeheugen SELECT * FROM Geheugen")
for i in range(lengte):
    cur.execute("UPDATE RememberSettingsGeheugen SET UurVanToevoeging =" + str(-1) +
                " WHERE Nummering =" + str(i))
#######################################################################################################################
lengte2 = 24
ZeroMatrix2 = []
for i3 in range(lengte2):
    Row = [i3]
    for i4 in range(1):
        Row.append(0)
    ZeroMatrix2.append(Row)
cur.executemany("INSERT INTO InfoLijsten24uur VALUES (?, ?)", ZeroMatrix2)
#######################################################################################################################
ZeroMatrix3 = [[0, 0, 0]]
cur.executemany("INSERT INTO Zonnepanelen VALUES(?, ?, ?)", ZeroMatrix3)
#######################################################################################################################
ZeroMatrix4 = [[0, 0, 0, 0, 0]]
cur.executemany("INSERT INTO Batterijen VALUES( ?, ?, ?, ?, ?)", ZeroMatrix4)
#######################################################################################################################
ZeroMatrix5 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
cur.executemany("INSERT INTO Huisgegevens VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ZeroMatrix5)
#######################################################################################################################
cur.execute("INSERT INTO ExtraWaarden VALUES (0, 0, 0, 0, 0)")
#######################################################################################################################
# Als je iets in de database verandert moet je altijd con.commit() gebruiken zodat het goed wordt opgeslagen
con.commit()
#######################################################################################################################
# Op deze manier kan je kolommen van gegevens uit een bepaalde tabel halen
res = cur.execute("SELECT DatumBelpex FROM Stroomprijzen")
print(res.fetchall())
