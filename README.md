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
