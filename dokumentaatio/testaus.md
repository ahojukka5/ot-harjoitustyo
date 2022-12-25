# Testausdokumentti

Ohjelmaa testataan yksikkötesteillä. Testit on laitettu kolmeen erilliseen tiedostoon:

- `test_entities.py` entiteettien testaus
- `test_repositories.py` repositorioiden testaus
- `test_service.py` sovelluslogiikan testaus
- `test_sources.py` lähteiden testaus

Testien ulkopuolelle on jätetty käyttöliittymä (`src/ui/*`) sekä päätiedosto
`saehaekkae.py`, joka niinikään on käyttöliittymän toiminnallisuuteen liittyvä
tiedosto.

## Testikattavuus

```text
Name                             Stmts   Miss Branch BrPart  Cover
------------------------------------------------------------------
src/config.py                       15     15      2      0     0%
src/entities/messages.py            73     26     16      0    60%
src/entities/record.py              57      1     18      3    95%
src/entities/selection.py           56      0     22      3    96%
src/entities/sources.py             76     28     18      3    59%
src/repositories/database.py        83      6     34      6    86%
src/services/dataservice.py         43     16     10      1    60%
src/services/datetimepicker.py      23      1      6      3    86%
src/services/messageservice.py      12      6      2      0    43%
------------------------------------------------------------------
TOTAL                              438     99    128     19    74%
```

Joitakin osia koodista on hankalaa testata mm. koska ne tekevät kyselyitä
requests-kirjastoa käyttäen. Nämä osuudet pitäisi eriyttää koodista erilliseen
tiedostoon ja jättää testaamatta, tai mockailla.
