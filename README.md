# P-O3
Slim zonnehuis
import pyomo.environ as pe
import pyomo.opt as po


solver = po.SolverFactory('glpk')
m  = pe.ConcreteModel()
#######################################################################################################
# definiëren functies
def variabelen_constructor(lijst, aantal_apparaten, aantal_uren):
    for p in range(aantal_uren*aantal_apparaten):
        lijst.add()

def objectieffunctie(prijzen, variabelen, Delta_t, wattagelijst, aantal_uren):
    prijzen_per_apparaat = prijzen*len(wattagelijst)
    obj_expr = 0
    for p in range(1,len(variabelen)+1):
        obj_expr = obj_expr + Delta_t * wattagelijst[(p-1)//aantal_uren] * prijzen_per_apparaat[p-1]* variabelen[p]
    return obj_expr

def exacte_beperkingen(variabelen, voorwaarden_apparaten, aantal_apparaten, voorwaarden_apparaten_lijst, aantal_uren):
    for q in range(aantal_uren*aantal_apparaten):
        index_voor_voorwaarden = q//aantal_uren
        indexnummers = voorwaarden_apparaten_lijst[index_voor_voorwaarden]
        for p in indexnummers:
            if type(p) == int:
                voorwaarden_apparaten.add(expr=variabelen[p+ index_voor_voorwaarden*aantal_uren] == 1)

def uiteindelijke_waarden(variabelen, aantaluren):
    print('De totale kost is', pe.value(m.obj), 'euro')
    for p in range(len(variabelen)):
        if p % aantaluren == 0:
            print('toestel nr.', p/aantaluren + 1)
        print(pe.value(variabelen[p+1]))

def beperkingen_aantal_uur(werkuren_per_apparaat, variabelen, voorwaarden_werkuren, aantal_uren):
    for p in range(len(werkuren_per_apparaat)):
        som = 0
        for q in range(1,aantal_uren+1):
            som = som + variabelen[p*aantal_uren + q]
        if type(werkuren_per_apparaat[p]) == int:
            voorwaarden_werkuren.add(expr = som == werkuren_per_apparaat[p])

def finaal_uur(finale_uren, variabelen, constraint_lijst_finaal_uur, aantal_uren):
    for q in range(len(finale_uren)):  # dit is welk aparaat het over gaat
        if type(finale_uren[q]) == int:
            p = finale_uren[q]-1  # dit is het eind uur, hierna niet meer in werking
            for s in range(p + 1, aantal_uren + 1):
                constraint_lijst_finaal_uur.add(expr=variabelen[(aantal_uren*q) + s] == 0)
#######################################################################################################
#variabelen
from stroomprijzen import aantalapparaten as aantal_apparaten
from stroomprijzen import wattages_apparaten as wattagelijst
from stroomprijzen import voorwaarden_apparaten_exacte_uren as voorwaarden_apparaten_exact
from stroomprijzen import tijdsstap as Delta_t
from stroomprijzen import aantaluren as aantal_uren
from stroomprijzen import prijslijst as prijzen
from stroomprijzen import finale_tijdstip as einduren
from stroomprijzen import uur_werk_per_apparaat as werkuren_per_apparaat
#######################################################################################################

m.apparaten = pe.VarList(domain=pe.Binary)

m.apparaten.construct()

variabelen_constructor(m.apparaten, aantal_apparaten, aantal_uren) # maakt variabelen aan die apparaten voorstellen

obj_expr = objectieffunctie(prijzen, m.apparaten, Delta_t, wattagelijst, aantal_uren) # somfunctie die objectief creeërt

m.obj = pe.Objective(sense = pe.minimize, expr = obj_expr)

m.voorwaarden_exact = pe.ConstraintList() # voorwaarde om op een exact uur aan of uit te staan
m.voorwaarden_exact.construct()

exacte_beperkingen(m.apparaten, m.voorwaarden_exact,aantal_apparaten, voorwaarden_apparaten_exact, aantal_uren) # beperkingen met vast uur

m.voorwaarden_aantal_werkuren = pe.ConstraintList()

beperkingen_aantal_uur(werkuren_per_apparaat, m.apparaten, m.voorwaarden_aantal_werkuren, aantal_uren)

m.voorwaarden_finaal_uur = pe.ConstraintList()

finaal_uur(einduren, m.apparaten, m.voorwaarden_finaal_uur, aantal_uren)


result = solver.solve(m)

print(result)

uiteindelijke_waarden(m.apparaten, aantal_uren)


-------------------------------------------------------------------------------------------------------------------------------


recentere back up:

import pyomo.environ as pe
import pyomo.opt as po


solver = po.SolverFactory('glpk')
m  = pe.ConcreteModel()
#######################################################################################################
# definiëren functies
def variabelen_constructor(lijst, aantal_apparaten, aantal_uren):
    for p in range(aantal_uren*aantal_apparaten): # totaal aantal nodige variabelen = uren maal apparaten
        lijst.add() # hier telkens nieuwe variabele aanmaken

def objectieffunctie(prijzen, variabelen, Delta_t, wattagelijst, aantal_uren, stroom_zonnepanelen):
    obj_expr = 0
    for p in range(aantal_uren):
        subexpr = 0
        for q in range(len(wattagelijst)):
            subexpr = subexpr + wattagelijst[q]*variabelen[q*aantal_uren + (p+1)] # eerst de variabelen van hetzelfde uur samentellen om dan de opbrengst van zonnepanelen eraf te trekken
        obj_expr = obj_expr + Delta_t*prijzen[p] * (subexpr - stroom_zonnepanelen[p])
    return obj_expr

def exacte_beperkingen(variabelen, voorwaarden_apparaten, aantal_apparaten, voorwaarden_apparaten_lijst, aantal_uren):
    for q in range(aantal_uren*aantal_apparaten):
        index_voor_voorwaarden = q//aantal_uren # hierdoor weet je bij welk apparaat de uur-constraint hoort
        indexnummers = voorwaarden_apparaten_lijst[index_voor_voorwaarden] # hier wordt de uur-constraint, horende bij een bepaald apparaat, opgevraagd
        for p in indexnummers:
            if type(p) == int: # kan ook dat er geen voorwaarde is, dan wordt de uitdrukking genegeerd
                voorwaarden_apparaten.add(expr=variabelen[p+ index_voor_voorwaarden*aantal_uren] == 1) # variabele wordt gelijk gesteld aan 1

def uiteindelijke_waarden(variabelen, aantaluren, namen_apparaten):
    print('-' * 30)
    print('De totale kost is', pe.value(m.obj), 'euro') # de kost printen
    print('-' * 30)
    print('toestand apparaten (0 = uit, 1 = aan):')
    for p in range(len(variabelen)):
        if p % aantaluren == 0: # hierdoor weet je wanneer je het volgende apparaat begint te beschrijven
            print('toestel nr.', p/aantaluren+1, '(', namen_apparaten[int(p/aantaluren)], ')') # opdeling maken per toestel
        print(pe.value(variabelen[p+1]))

def beperkingen_aantal_uur(werkuren_per_apparaat, variabelen, voorwaarden_werkuren, aantal_uren):
    for p in range(len(werkuren_per_apparaat)):
        som = 0
        for q in range(1,aantal_uren+1):
            som = som + variabelen[p*aantal_uren + q] # hier neem je alle variabelen van hetzelfde apparaat, samen
        if type(werkuren_per_apparaat[p]) == int:
            voorwaarden_werkuren.add(expr = som == werkuren_per_apparaat[p]) # apparaat moet x uur aanstaan

def finaal_uur(finale_uren, variabelen, constraint_lijst_finaal_uur, aantal_uren):
    for q in range(len(finale_uren)):  # dit is welk aparaat het over gaat
        if type(finale_uren[q]) == int:
            p = finale_uren[q]-1  # dit is het eind uur, hierna niet meer in werking
            for s in range(p + 1, aantal_uren + 1):
                constraint_lijst_finaal_uur.add(expr=variabelen[(aantal_uren*q) + s] == 0)

def aantal_uren_na_elkaar(uren_na_elkaarVAR, variabelen, constraint_lijst_aantal_uren_na_elkaar, aantal_uren,
                              variabelen_start):
        # Dat een bepaald apparaat x aantal uur moet werken staat al in beperking_aantal_uur dus niet meer hier
        # wel nog zeggen dat de som van de start waardes allemaal slechts 1 mag zijn
    for i in range(len(uren_na_elkaarVAR)):  # zegt welk apparaat
        if type(uren_na_elkaarVAR[i]) == int:
            opgetelde_start = 0
            for p in range(1, aantal_uren + 1):  # zegt welk uur het is
                opgetelde_start = opgetelde_start + variabelen_start[aantal_uren * i + p]
            #print('dit is eerste constraint', opgetelde_start)
            constraint_lijst_aantal_uren_na_elkaar.add(expr=opgetelde_start == 1)
    for i in range(len(uren_na_elkaarVAR)):  # dit loopt de apparaten af
        if type(uren_na_elkaarVAR[i]) == int:
            #print('dit is nieuwe i', i)
            k = 0
            som = 0
            for p in range(0, aantal_uren):  # dit loopt het uur af
                SENTINEL = 1
                #print('dit is een nieuwe p', p)
                    # print('juist of fout', k < uren_na_elkaarVAR[i], k, uren_na_elkaarVAR[i])
                    # print('juist of fout', k < p)
                while k < uren_na_elkaarVAR[i] and k < p + 1:
                        # print('EERSTE while')
                    som = som + variabelen_start[aantal_uren * i + p + 1]
                    k = k + 1
                    #print('dit is mijn som1', som, 'en is gelijk aan', variabelen[aantal_uren * i + p + 1])
                    constraint_lijst_aantal_uren_na_elkaar.add(expr=variabelen[aantal_uren * i + p + 1] == som)
                    SENTINEL = 0
                while k <= aantal_uren and k >= uren_na_elkaarVAR[i] and SENTINEL == 1:
                    #print('tweede while', 'eerste index', aantal_uren * i + p + 1, 'tweede index',
                            #aantal_uren * i + p - uren_na_elkaarVAR[i] +1)
                    som = som + variabelen_start[aantal_uren * i + p + 1] - variabelen_start[aantal_uren * i + p - uren_na_elkaarVAR[i] + 1]
                    #print('dit is mijn som2', som, 'en is gelijk aan', variabelen[aantal_uren * i + p + 1])
                    k = k + 1
                    SENTINEL = 0
                    constraint_lijst_aantal_uren_na_elkaar.add(expr=variabelen[aantal_uren * i + p + 1] == som)
#######################################################################################################
#variabelen
from stroomprijzen import aantalapparaten as aantal_apparaten
from stroomprijzen import wattages_apparaten as wattagelijst
from stroomprijzen import voorwaarden_apparaten_exacte_uren as voorwaarden_apparaten_exact
from stroomprijzen import tijdsstap as Delta_t
from stroomprijzen import aantaluren as aantal_uren
from stroomprijzen import prijslijst_stroomverbruik_per_uur as prijzen
from stroomprijzen import finale_tijdstip as einduren
from stroomprijzen import uur_werk_per_apparaat as werkuren_per_apparaat
from stroomprijzen import stroom_per_uur_zonnepanelen as stroom_zonnepanelen
from stroomprijzen import uren_na_elkaar as uren_na_elkaarVAR
from stroomprijzen import namen_apparaten as namen_apparaten

#######################################################################################################

m.apparaten = pe.VarList(domain=pe.Binary)

m.apparaten.construct()

variabelen_constructor(m.apparaten, aantal_apparaten, aantal_uren) # maakt variabelen aan die apparaten voorstellen

obj_expr = objectieffunctie(prijzen, m.apparaten, Delta_t, wattagelijst, aantal_uren, stroom_zonnepanelen) # somfunctie die objectief creeërt

m.obj = pe.Objective(sense = pe.minimize, expr = obj_expr)

m.voorwaarden_exact = pe.ConstraintList() # voorwaarde om op een exact uur aan of uit te staan
m.voorwaarden_exact.construct()

exacte_beperkingen(m.apparaten, m.voorwaarden_exact,aantal_apparaten, voorwaarden_apparaten_exact, aantal_uren) # beperkingen met vast uur

m.voorwaarden_aantal_werkuren = pe.ConstraintList()

beperkingen_aantal_uur(werkuren_per_apparaat, m.apparaten, m.voorwaarden_aantal_werkuren, aantal_uren) # moet x uur werken, maakt niet uit wanneer

m.voorwaarden_finaal_uur = pe.ConstraintList()

finaal_uur(einduren, m.apparaten, m.voorwaarden_finaal_uur, aantal_uren) # moet na een bepaald uur klaarzijn

# Voor functie aantal_uren_na_elkaar
m.apparatenstart = pe.VarList(domain=pe.Binary)
m.apparatenstart.construct()
variabelen_constructor(m.apparatenstart, aantal_apparaten, aantal_uren)

m.voorwaarden_aantal_uren_na_elkaar = pe.ConstraintList()

aantal_uren_na_elkaar(uren_na_elkaarVAR, m.apparaten, m.voorwaarden_aantal_uren_na_elkaar, aantal_uren,
                          m.apparatenstart)

result = solver.solve(m)

print(result)

uiteindelijke_waarden(m.apparaten, aantal_uren, namen_apparaten)
