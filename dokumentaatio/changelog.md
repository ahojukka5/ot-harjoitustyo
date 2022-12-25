# Changelog

## Viikko 3

- Alustettu projekti
- Lisätty ja testattu luokat Record ja Database
- Käyttäjä voi käynnistää ohjelman `poetry run invoke start` -komennolla,
  jolloin aukeaa graafinen käyttöliittymä (vielä kesken)

## Viikko 4

- Lisätty riippuvuuksia: requests, pandas, matplotlib
- Toteutettu tietokannan expottaus dataframeen
- Toteutettu sähkön hinnan piirto matplotlibillä
- Toteutettu sähkön hinnan haku spot-hinta.fi -palvelusta
- Lisätty linttaus (`poetry run invoke lint`)
- Lisätty arkkitehtuurikuvaus

## Viikko 5

- Toteutettu tuntien valinta: käyttäjä voi pylväsdiagramin pylvästä klikkaamalla
  valita potentiaaliset tunnit.

## Viikko 6

- Dokumentoitu kauttaaltaan docstringeillä.
- Implementoitu fetcher käyttäjädatalle <oma.datahub.fi> palvelua ajatellen.
- Implementoitu widget kulutusdatan visualisointiin.
- Paranneltu pörssihinta-widgetin ulkoasua.

## Viikko 7-8

- Lisätty testikattavuutta
- Tehty viestien lähetystoiminnallisuus: ShellyMessage ja GoogleMessage
- Tehty komentorivikäyttöliittymä
- Tehty DateTimePicker
- Refactoroitu koodia, tehty DataService
