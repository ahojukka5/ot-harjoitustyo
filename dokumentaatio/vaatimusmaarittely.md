# Vaatimusmäärittely

## Taustatietoa

Pörssisähkö on sellainen sähkösopimuksen muoto, jossa sähkön hinta vaihtelee
tunnettein sähköpörssin markkinahinnan mukaan.

## Sovelluksen tarkoitus

**Sovelluksen tarkoitus on vähentää käyttäjänsä sähkölaskua**. Tämä tapahtuu
pääasiallisesti kahdella eri tavalla. Ensisijaisesti sovellus avustaa käyttäjää
siirtämään sähkönkulutusta halvoille tunneille joko muistutuksilla tai
laitteiden ohjauskomennoilla. Toissijaisesti käyttäjä voi tarkastella
jälkeenpäin historiallista sähkön kulutusta sekä hintatietoa sen toteamiseksi,
onko ohjaus onnistunut.

## Käyttäjät

Sovelluksessa on alustavasti kahdenlaista käyttäjäroolia: peruskäyttäjä ja
edistynyt käyttäjä. Peruskäyttäjä käyttää sovellusta yksinkertaisesta
graafisesta käyttöliittymästä. Toiminnallisuus on rajoitettua ja pääpaino on
käytön yksinkertaisuudessa. Edistynyt käyttäjä voi käyttää sovellusta
tekstikäyttöliittymästä ja tehdä monimutkaisempia ohjauksia. Tarkoitus ei ole
tehdä erillistä käyttäjän tunnistamista, vaan mahdolliset kehittyneet
ominaisuudet piilotetaan peruskäyttäjältä. Edistynyttä käyttäjää varten ohjelma
suunnitellaan siten, että se on laajennettavissa täsmällisesti omiin tarpeisiin.

## Käyttöliittymäluonnos

Sovelluksessa on kaksi erillistä käyttöliittymää.

Tekstipohjaisella käyttöliittymällä sovellusta voidaan käyttää komentoriviltä,
mikä on tärkeää ajatellen erilaisia automatisointiratkaisuja. Tekstipohjaisen
käyttöliittymän perusajatus on muotoilla viesti, joka voidaan edelleen lähettää
eri tavoin. Tällainen viesti voi olla esimerkiksi ohjauskomento wifi-releelle
json-muodossa, sähköpostiviesti, kalenterimerkintä tai ajastettu push up
-notifikaatio puhelimeen. Osa viestimenetelmistä on maksullisia ja ne jätetään
perustoiminnallisuuden ulkopuolelle.

Tämän lisäksi toteutetaan graafinen käyttöliittymä, jonka **keskeinen päämäärä
on olla mahdollisimman yksinkertainen**. Periaate on: *kaksi nappulaa on liikaa,
jos yhdelläkin pärjää*.

![gui_luonnos](gui_luonnos.png)

Käyttöliittymässä näkyy sen hetkinen sähkön hinta. Käyttäjä voi klikata,
maalata, tai muulla vastaavalla hiirellä tapahtuvalla interaktiolla valita
"halvat tunnit" ja valita komennon. Komento voi olla esimerkiksi releen
ohjauskomento päälle haluttuna aikana tai ilmoitus puhelimeen. Paras tapa saada
ilmoitus puhelimeen on kalenterimerkintä Googlen kalenteriin. Tämä kalenteri
voidaan sitten jakaa perheen kesken, joten ilmoitus halvasta tai kalliista
sähköstä voidaan jakaa kaikkiin perheen älylaitteisiin niin halutessaan. Onhan
sähkön säästäminen toki koko perheen yhteinen asia, joten jaettu kalenteri
toteuttaa tämän tavoitteen erinomaisesti.

## Perusversion tarjoama toiminnallisuus

Perusversiossa käyttäjä voi valita tekstikäyttöliittymästä tunnin tai tunteja ja
valita komennon. Komento voi esimerkiksi ohjelmoida wifi-releen ajastuksen.
Koska kaikilla ei tällaisia releitä ole, niin vaihtoehtoinen komento on pyytää
itselle kännykkään muistutus haluttuun ajanhetkeen, mikäli sellainen on
mahdollista ilmaiseksi toteuttaa. Kolmas vaihtoehto on ajastettu
sähköpostiviesti. Parhaassa tapauksessa käyttäjä voi käyttää kaikkia mainittuja
tapoja, esimerkiksi ohjata wifi-kellokytkimellä lämminvesivaraajan yöllä klo 3-5
päälle sekä pyytää kännykkään muistutuksen, kun on aika laittaa pyykinpesukone
päälle. Alkuperäinen ajatus oli, ajan valinta ja viestin lähetys voitaisiin
tehdä graafisesti käyttöliittymästä, mutta sitä ei projektin kuolemanviivan
puitteissa keretty tehdä.

- [x] käyttäjä voi tarkastella kuluvan päivän ja seuraavan päivän sähkön hintoja
      graafisesti käyttöliittymästä
- [x] käyttäjä voi tarkastella kuluvan päivän ja seuraavan päivän sähkön hintoja
      tekstikäyttöliittymästä
- [x] käyttäjä voi valita tunnin tai tunteja tekstikäyttöliittymästä
- [x] käyttäjä voi lähettää viestin jolla ohjataan lähiverkkoon kytkettyä Shelly
      wifi-relettä tekstikäyttöliittymästä
- [x] käyttäjä voi lähettää viestin jolla tehdään kalenterimerkintä Google
      kalenteriin tekstikäyttöliittymästä
- [x] käyttäjä voi ladata oma.datahub.fi palvelusta kulutustiedot ja ladata ne
      ohjelmaan sekä seurata aiempaa kulutushistoriaa
- [x] käyttäjä voi verrata sähkön historiallista hintaa ja kulutusta ja todeta
      että onko hinnan optimointi ollut onnistunutta vai ei
- [x] käyttäjä voi laajentaa ohjelman toiminnallisuutta määrittelemällä oman
      datalähteen
- [x] käyttäjä voi laajentaa ohjelman toiminnallisuutta määrittelemällä oman
      viestin
- [ ] käyttäjä voi valita tunnin tai tunteja graafisesta käyttöliittymästä
- [ ] käyttäjä voi lähettää viestin jolla ohjataan lähiverkkoon kytkettyä Shelly
      wifi-relettä graafisesta käyttöliittymästä
- [ ] käyttäjä voi lähettää viestin jolla tehdään kalenterimerkintä Google
      kalenteriin graafisesta käyttöliittymästä

## Jatkokehitysideoita

- automatiikka, joka valitsee esimerkiksi kolme halvinta tuntia ja toteuttaa
  kellokytkimen ohjelmoinnin täysin itsenäisesti crontab-ohjattuna
- sähkön hintatietojen ja kulutustiedon tallennus tietokantaan
- näkymä, josta voi seurata oman sähkön käytön toteutumista, laskea sähkön
  keskihinnan, saada hienoja graafeja ja käppyröitä yms.
- tuuli-, lämpötila ym. ennusteet
- anonymisoidun käyttötiedon lähetys pelipalvelimelle, "sähkönsäästökilpailu"
- integroituminen johonkin toiseen järjestelmään, esim. Home Assistant
- selainpohjainen käyttöliittymä, asennus esim. Android-tablettiin koko ruudun
  tilaan
