# Project Poolmath

Custom integration för Home Assistant som hämtar vattenkemi från [Pool Math](https://www.troublefreepool.com/blog/poolmath/) (Trouble Free Pool) via appens delningslänk och skapar sensorer i Home Assistant.

Allt konfigureras via UI – ingen YAML behövs.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CrallH&repository=Project-Poolmath-&category=integration)
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=poolmath)

> [!NOTE]
> **🤖 AI-genererat projekt**
> Hela den här integrationen — kod, dokumentation och konfiguration — är genererad av en AI-assistent (Claude, Anthropic) utifrån instruktioner från en mänsklig utvecklare. Koden har granskats översiktligt för grundläggande korrekthet och säkerhet under utvecklingen, men har inte genomgått traditionell mänsklig kodgranskning eller omfattande produktionstestning. Använd på egen risk, testa i din egen miljö innan du litar på den, och rapportera gärna buggar eller konstigheter via [Issues](https://github.com/CrallH/Project-Poolmath-/issues).

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
| Dagar sedan bakspolning | dagar |
| Dagar sedan borstning | dagar |
| Dagar sedan filterrengöring | dagar |
| Dagar sedan dammsugning | dagar |
| Dagar sedan öppning | dagar |
| Dagar sedan stängning | dagar |

"Dagar sedan"-sensorerna skapas bara om du loggat aktiviteten minst en gång i Pool Math-appen. Alla sensorer samlas under en enhet med poolens namn och har attributet `last_measured` när API:et anger tidsstämpel.

## Installation via HACS

Klicka på knappen nedan för att öppna HACS direkt i din egen Home Assistant med repot förifyllt:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=CrallH&repository=Project-Poolmath-&category=integration)

Eller manuellt:

1. HACS → menyn (⋮) uppe till höger → **Custom repositories**
2. Lägg till `https://github.com/CrallH/Project-Poolmath-` med typ **Integration**
3. Sök efter **Project Poolmath** i HACS och installera
4. Starta om Home Assistant

## Konfiguration

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=poolmath)

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
