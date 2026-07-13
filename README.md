# Project Poolmath

Custom integration för Home Assistant som hämtar vattenkemi från [Pool Math](https://www.troublefreepool.com/blog/poolmath/) (Trouble Free Pool) via appens delningslänk och skapar sensorer i Home Assistant.

Allt konfigureras via UI – ingen YAML behövs.

## Sensorer

Sensorer skapas automatiskt för de värden som finns i din pooldata:

| Sensor | Beskrivning |
|---|---|
| Fritt klor (FC) | ppm |
| Bundet klor (CC) | ppm |
| pH | – |
| Total alkalinitet (TA) | ppm |
| Kalciumhårdhet (CH) | ppm |
| Cyanursyra (CYA) | ppm |
| Salt | ppm |
| Borat | ppm |
| CSI | Calcium Saturation Index |
| Vattentemperatur | °C/°F (valbart) |
| SWG-celleffekt | % |
| Filtertryck | – |

Alla sensorer samlas under en enhet med poolens namn och har attributet `last_measured` när API:et anger tidsstämpel.

## Installation via HACS

1. HACS → menyn (⋮) uppe till höger → **Custom repositories**
2. Lägg till `https://github.com/CrallH/Project-Poolmath-` med typ **Integration**
3. Sök efter **Project Poolmath** i HACS och installera
4. Starta om Home Assistant

## Konfiguration

1. **Inställningar → Enheter & tjänster → Lägg till integration**
2. Sök på **Project Poolmath**
3. Klistra in din delningslänk, t.ex. `https://api.poolmathapp.com/share/Q5kpgY5`
   (finns i Pool Math-appen under *Settings → Sharing*)

Under **Konfigurera** på integrationen kan du sedan ändra:

- Uppdateringsintervall (standard 15 min)
- Temperaturenhet (°C/°F)

## Manuell installation

Kopiera mappen `custom_components/poolmath` till din HA-konfigurations `custom_components/` och starta om.

## Ansvarsfriskrivning

Detta är en inofficiell integration och är inte kopplad till Trouble Free Pool eller Pool Math.
