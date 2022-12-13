# Käyttöohje

## Konfigurointi

Ohjelmassa on tiedosto `settings.py`, jossa on muutamia konfiguroitavia muuttujia:

```python
ENERGY_PRICE_SOURCE = "test"
ENERGY_PRICE_URI = "https://api.spot-hinta.fi/TodayAndDayForward"
ENERGY_PRICE_FILE = "data/energy-prices.json"
ENERGY_CONSUMPTION_SOURCE = "test"
ENERGY_CONSUMPTION_FILE = "data/energy-consumption.csv"
```

`ENERGY_PRICE_SOURCE` voi saada arvot `test`, `local` ja `internet`.
`ENERGY_CONSUMPTION_SOURCE` arvon `test`. Oletusarvoisesti nämä ovat kaikki
`test`, jolloin ohjelma ei lataa mitään netistä eikä näytä siis ajantasaista
tietoa. Todennäköisesti käyttäjä haluaa laittaa `ENERGY_PRICE_SOURCE = internet`
jolloin hintatiedot haetaan netistä, ja `ENERGY_CONSUMPTION_SOURCE = local` sekä
ladata <oma.datahub.fi>-palvelusta kulutustietonsa csv-muodossa ja sijoittaa ne
vaikkapa tiedostoon `data/energy-consumption.csv`.

## Ohjelman käynnistäminen

Ohjelma käyttää poetryä, jolla voi asentaa kaikki riippuvuudet vaivattomasti.
Riippuvuudet asennetaan komennolla:

```bash
poetry install
```

Tämän jälkeen ohjelma käynnistetään komennolla

```bash
poetry run invoke start
```
