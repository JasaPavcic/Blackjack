from bottle import Bottle, request, redirect, run
from bottle_login import LoginPlugin
from bottle import static_file
from bottle import template
import sys
from model import *
import random


app = Bottle()
app.config["SECRET_KEY"] = "skrivnost"

login_plugin = app.install(LoginPlugin())

aktivne_igre = []
igra_predloge = ['stava.tpl', 'korak1.tpl', 'stand.tpl']

vrednosti_kart = ['a',2,3,4,5,6,7,8,9,10,'j','q','k']
barve_kart = ['hearts','spades','diams','clubs']


@app.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')

@login_plugin.load_user
def load_user_by_id(id_uporabnika):
    return Uporabnik.dobi({'id': id_uporabnika})

@app.route("/", method='GET')
def index():
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    return template('predloge/index.tpl', uporabnik=uporabnik)

@app.route('/odjava')
def odjava():
    login_plugin.logout_user()
    return redirect("/")

@app.route("/prijava", method='POST')
def prijava():
    uporabnisko_ime = request.POST.get('ime')
    geslo = request.POST.get('geslo')
    uporabnik = Uporabnik.dobi({'ime': uporabnisko_ime, 'geslo': geslo})
    if uporabnik:
        login_plugin.login_user(uporabnik[0])
        return redirect("/")
    else:
        return template('predloge/prijava_neuspesna.tpl', msg='Napacno upor. ime ali geslo.')

@app.route('/registracija')
def registracija():
    return template('predloge/registracija_obrazec.tpl')

@app.route('/registracija_uspesna')
def registracija_uspesna():
    return template('predloge/registracija_uspesna.tpl')

@app.route('/registriraj', method='POST')
def registriraj():
    #try:
    uporabnisko_ime = request.POST.get('ime')
    geslo = request.POST.get('geslo')
    potrditev = request.POST.get('potrditev')
    napaka = ''
    if not Uporabnik.dobi({'ime': uporabnisko_ime}):
        if geslo == potrditev:
            Uporabnik.ustvari({'ime':uporabnisko_ime, 'geslo': geslo, 'denar': 100})
            return redirect("/registracija_uspesna")
        else:
            napaka = 'Gesli se ne ujemata'
    else:
        napaka = 'Uporabnik ze obstaja'
    return template('predloge/registracija_neuspesna.tpl', msg=napaka)

@app.route('/igra', method='GET')
def igra():
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi_aktivno(uporabnik[0])
    if not igra:
        Igra.ustvari({'uporabnik_id': uporabnik[0],'stava': 0,'status': 0,'podvojitev': 0})
        igra = Igra.dobi_aktivno(uporabnik[0])
        deck = []
        for v in vrednosti_kart:
            for b in barve_kart:
                deck.append({'barva': b, 'vrednost':v})
        aktivne_igre.append({'id': igra[0], 'igralceve_karte': [], 'igralceva_vsota': [], 'dilerjeve_karte': [], 'dilerjeva_vsota': [], 'deck': deck, 'rezultat': 0, 'stand': 0})
    return redirect('/igra/' + str(igra[0]))



@app.route('/igra/<id_igre>', method='GET')
def igra(id_igre):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])
    if not aktivna_igra:
        return redirect('/igra')
    rezultat = aktivna_igra['rezultat']
    if not rezultat and igra[4] < 3:
        predloga = igra_predloge[igra[4]]
        return template('predloge/' + predloga, igra_podatki=igra, aktivna_igra=aktivna_igra, uporabnik=uporabnik)
    else:
        return redirect('/igra/konec/' + str(igra[0]))

def poisci_igro(id_igre):
    for aktivna_igra in aktivne_igre:
        if aktivna_igra['id'] == id_igre:
            return aktivna_igra
    Igra.odstrani({'id': id_igre})
    return False

def izracunaj_vsoto(roka):
    vsote = []
    for karta in roka:
        if karta['vrednost'] in ['q', 'j', 'k']:
            vsote.append(10)

    for karta in roka:
        if karta['vrednost'] not in ['q', 'j', 'k', 'a']:
            vsote.append(karta['vrednost'])
   
    for as_vrednost in [11, 1]:
        vsote_z_asi = vsote.copy()
        asi_ind = [roka.index(k) for k in roka if k['vrednost'] == 'a']
        for as_index in asi_ind:
            for karta in roka:
                if roka.index(karta) == as_index:
                    vsote_z_asi.append(as_vrednost)
        if sum(vsote_z_asi) <= 21:
            vsote = vsote_z_asi.copy()
            break
    return sum(vsote)

@app.route('/igra/stava/<id_igre>', method='POST')
def stava(id_igre):
    id_igre = int(id_igre)
    stava = request.POST.get('stava')
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    Igra.posodobi({'id': id_igre}, {'status': 1, 'stava': int(stava)}) 

    aktivna_igra = poisci_igro(igra[0])

    while(len(aktivna_igra['igralceve_karte']) > 0):
        aktivna_igra['deck'].push(aktivna_igra['igralceve_karte'].pop())
    while(len(aktivna_igra['dilerjeve_karte']) > 0):
        aktivna_igra['deck'].push(aktivna_igra['dilerjeve_karte'].pop())

    random.shuffle(aktivna_igra['deck'])

    aktivna_igra['igralceve_karte'].append(aktivna_igra['deck'].pop())
    #SPODNJE KARTE NE SMEMO PRIKAZATI NA ZACETKU
    aktivna_igra['dilerjeve_karte'].append(aktivna_igra['deck'].pop())
    aktivna_igra['igralceve_karte'].append(aktivna_igra['deck'].pop())
    aktivna_igra['dilerjeve_karte'].append(aktivna_igra['deck'].pop())


    aktivna_igra['igralceva_vsota'] = izracunaj_vsoto(aktivna_igra['igralceve_karte'])
    #TREBA UPOSTEVATI LE 2 KARTO
    aktivna_igra['dilerjeva_vsota'] = izracunaj_vsoto(aktivna_igra['dilerjeve_karte'])

    return redirect('/igra/' + str(igra[0]))

@app.route('/igra/hit/<id_igre>', method='GET')
def hit(id_igre):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])
    aktivna_igra['igralceve_karte'].append(aktivna_igra['deck'].pop())
    aktivna_igra['igralceva_vsota'] = izracunaj_vsoto(aktivna_igra['igralceve_karte'])
    aktivna_igra['dilerjeva_vsota'] = izracunaj_vsoto(aktivna_igra['dilerjeve_karte'])
    return redirect('/igra/' + str(igra[0]))

    

@app.route('/igra/double_down/<id_igre>', method='GET')
def double_down(id_igre):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])
    stava = igra[3]
    stava = 2 * stava
    Igra.posodobi({'id': id_igre}, {'podvojitev': 1, 'stava': stava})
    aktivna_igra['igralceve_karte'].append(aktivna_igra['deck'].pop())
    aktivna_igra['igralceva_vsota'] = izracunaj_vsoto(aktivna_igra['igralceve_karte'])
    return redirect('/igra/stand/' + str(igra[0]))

@app.route('/igra/stand/<id_igre>', method='GET')
def stand(id_igre):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])
    dilerjeva_vsota = izracunaj_vsoto(aktivna_igra['dilerjeve_karte'])
    while dilerjeva_vsota < 17:
        aktivna_igra['dilerjeve_karte'].append(aktivna_igra['deck'].pop())
        dilerjeva_vsota = izracunaj_vsoto(aktivna_igra['dilerjeve_karte'])
        aktivna_igra['dilerjeva_vsota'] = dilerjeva_vsota
    rezultat = zmagovalec(id_igre, diler_17 = True)
    aktivna_igra['rezultat'] = rezultat
    print("-----------------------",aktivna_igra)
    Igra.posodobi({'id': igra[0]}, {'status': 3})
    return template('predloge/stand.tpl', igra_podatki=igra, aktivna_igra=aktivna_igra, uporabnik=uporabnik)


def zmagovalec(id_igre, igralec_pocaka = False, diler_17 = False):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])

    vsota_diler = izracunaj_vsoto(aktivna_igra['dilerjeve_karte'])
    vsota_igralec = izracunaj_vsoto(aktivna_igra['igralceve_karte'])
    
 
    if 21 == vsota_igralec:
        if 21 == vsota_diler:
            print("Ni zmagovalca!!!")
            return 3
        else:
            print("Igralec je zmagal!!!")
            return 1
    elif 21 == vsota_diler:
        print("Diler je zmagal!!!")
        return 2
    else:
        #Tukaj preverimo se, ce je kdo sel cez 21
        diler_out = True
        if vsota_diler <= 21:
            diler_out = False
        
        igralec_out = True
        if vsota_igralec <= 21:
            igralec_out = False

        if diler_out and not igralec_out:
            return 1
        elif igralec_out and not diler_out:
            return 2
        elif igralec_out and diler_out:
            return 3
        elif diler_17:
            if vsota_diler == vsota_igralec:
                return 3
            elif vsota_diler > vsota_igralec and vsota_diler <=21:
                return 2
            else:
                return 1
        else:
            if igralec_pocaka:
                diler_zmaga = True
                if vsota_igralec > vsota_diler and vsota_igralec <= 21 :
                    diler_zmaga = False 
                if diler_zmaga:
                    return 2
                else:
                    return False
            else:
                return False

@app.route('/igra/konec/<id_igre>', method='GET')
def konec(id_igre):
    id_igre = int(id_igre)
    uporabnik = login_plugin.get_user()
    if not uporabnik:
        return template('predloge/prijava.tpl')
    igra = Igra.dobi({'id': id_igre})
    aktivna_igra = poisci_igro(igra[0])
    Igra.posodobi({'id': igra[0]}, {'izid': aktivna_igra['rezultat'], 'status': 3})
    stava = igra[3]
    if igra[5]:
        stava = 2 * stava
    if aktivna_igra['rezultat'] == 1:
        Uporabnik.posodobi({'id': uporabnik[0]},{'denar': uporabnik[3] + stava})
    elif aktivna_igra['rezultat'] == 2:
        Uporabnik.posodobi({'id': uporabnik[0]},{'denar': uporabnik[3] - stava})
    aktivne_igre.remove(aktivna_igra)
    return template('predloge/konec.tpl', igra_podatki=igra, aktivna_igra=aktivna_igra, uporabnik=uporabnik)






#'localhost'

run(app, host='0.0.0.0' , port=8083)
