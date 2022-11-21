# Tehtävä 2: Laajennettu Monopoli

Luokat:

- Peli
- Pelilauta
- Pelaaja
- Ruutu
- Noppa
- Pelinappula

Lisäksi:

- Aloitusruutu
- Vankila
- Sattuma
- Yhteismaa
- Asema
- Laitos
- Katu
- Kortti
- Toiminto
- Hotelli
- Talo

```mermaid
classDiagram
%% Monopolia pelataan käyttäen kahta noppaa.
Monopoli "1" -- "2" Noppa
%% Pelaajia on vähintään 2 ja enintään 8.
Pelaaja "2..8" -- "1" Monopoli
%% Peliä pelataan pelilaudalla joita on yksi.
Monopoli "1" -- "1" Pelilauta
%% Pelilauta sisältää 40 ruutua.
Pelilauta "1" -- "40" Ruutu
%% Kukin ruutu tietää, mikä on sitä seuraava ruutu pelilaudalla.
Ruutu "1" -- "1" Ruutu
%% Kullakin pelaajalla on yksi pelinappula.
Pelaaja "1" -- "1" Pelinappula
%% Pelinappula sijaitsee aina yhdessä ruudussa.
Pelinappula "0..1" -- "1" Ruutu

%% Ruutuja on useampaa eri tyyppiä:
%% Aloitusruutu
Ruutu <-- Aloitusruutu
%%Aloitusruutu --> Ruutu
%% Vankila
Ruutu <-- Vankila
%% Sattuma ja yhteismaa
Ruutu <-- Sattuma
Ruutu <-- Yhteismaa
%% Asemat ja laitokset
Ruutu <-- Asema
Ruutu <-- Laitos
%% Normaalit kadut (joihin liittyy nimi)
Ruutu <-- Katu
Katu : string nimi
%% Monopolipelin täytyy tuntea sekä aloitusruudun että vankilan sijainti
%% Aloitusruutu : int sjainti
%% Vankila : int sijainti
Monopoli "1" -- "1" Aloitusruutu
Monopoli "1" -- "1" Vankila
%% Jokaiseen ruutuun liittyy jokin toiminto
Ruutu "1" -- "1" Toiminto
%% Sattuma- ja yhteismaaruutuihin liittyy kortteja,
Sattuma -- Kortti
Yhteismaa -- Kortti
%% joihin kuhunkin liittyy joku toiminto.
Kortti -- Toiminto
%% Toimintoja on useanlaisia. Ei ole vielä tarvetta tarkentaa toiminnon laatua.
%% Normaaleille kaduille voi rakentaa korkeintaan 4 taloa
Katu "1" -- "0..4" Talo
%% tai yhden hotellin.
Katu "1" -- "0..1" Hotelli
%% Kadun voi omistaa joku pelaajista.
Pelaaja "1" -- "*" Katu
%% Pelaajilla on rahaa (seteleitä)
Pelaaja "1" -- "*" Raha
```
