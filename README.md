# Teams-Statuslicht für Home Assistant (ESPHome)

Ein Busy-Light am Monitor, das den Microsoft-Teams-Status anzeigt – vollständig über **Home Assistant** und **ESPHome**, ohne Software auf dem Arbeitsrechner. Der Status kommt aus der Microsoft-Cloud (Graph-Präsenz). Das Licht funktioniert deshalb unabhängig davon, ob Teams am Laptop, im Browser oder am Handy läuft.

## Inspiration und Gehäuse

Angeregt wurde das Projekt durch das **[Radig StatusLight](https://makerworld.com/de/models/2955341-radig-status-light)** von **Ulrich Radig** ([ulrichradig.de](https://www.ulrichradig.de/home/index.php/esp32/statuslight)). Ich verwende dessen 3D-gedruckte Teile und dieselbe Hardware (Seeed Studio XIAO ESP32S3, WS2812-Streifen, Datenleitung an GPIO1).

Das Original wird per USB über einen virtuellen COM-Port und eine Windows-Software gesteuert. Dieses Repository ersetzt nur die Firmware: Mit ESPHome wird das Licht eine Leuchte in Home Assistant, und eine Automation setzt die Farbe nach dem Teams-Status.

**Die 3D-Druckdateien sind nicht Teil dieses Repositorys.** Sie stehen ausschließlich auf MakerWorld zur Verfügung; deren Weiterveröffentlichung ist laut den Nutzungshinweisen des Designers nicht erlaubt. Bitte dort herunterladen und die dortigen Bedingungen beachten (u. a. kein Verkauf gedruckter Teile oder kompletter Geräte).

## Funktionen

- Statusfarbe nach Teams-Aktivität (Microsoft Graph)
- Nur aktiv, wenn du zuhause bist (Person-Entität)
- Werktags in der Arbeitszeit voller Status, sonst nur Call und Präsentieren
- Helligkeit je Farbe über Schieberegler in Home Assistant
- Farbtest-Skript, das alle Zustände nacheinander zeigt
- Kein Status ohne Verbindung: Verliert das Licht die Verbindung zu Home Assistant, schaltet es sich nach spätestens 30 s aus

## Farben

| Teams-Aktivität | Werktag, Arbeitszeit | Sonst |
|---|---|---|
| Presenting | **rot pulsierend** | **rot pulsierend** |
| InACall, InAConferenceCall | **rot** | **rot** |
| DoNotDisturb, UrgentInterruptionsOnly | **rot** | aus |
| InAMeeting, Busy | **gelb** | aus |
| Available | **grün** | aus |
| Away, BeRightBack, Inactive | **blau** | aus |
| Offline, unbekannt | aus | aus |

Ist die gewählte Person nicht zuhause, bleibt das Licht immer aus. Farben, Arbeitszeit und Pulsier-Effekt sind im Blueprint einstellbar.

## Inhalt

| Pfad | Inhalt |
|---|---|
| [`esphome/teams-status-licht.yaml`](esphome/teams-status-licht.yaml) | ESPHome-Firmware für den XIAO ESP32S3 |
| [`esphome/secrets.yaml.example`](esphome/secrets.yaml.example) | Vorlage für die Secrets |
| [`blueprints/automation/teams_status_licht.yaml`](blueprints/automation/teams_status_licht.yaml) | Blueprint: Statusanzeige |
| [`blueprints/script/teams_status_licht_farbtest.yaml`](blueprints/script/teams_status_licht_farbtest.yaml) | Blueprint: Farbtest |
| [`packages/teams_status_licht.yaml`](packages/teams_status_licht.yaml) | Helligkeits-Helfer (optional, für YAML-Nutzer) |
| [`docs/verdrahtung.md`](docs/verdrahtung.md) | Verdrahtung, Pegel, Strom, Löten |

## Voraussetzungen

- Hardware wie im Radig StatusLight: Seeed Studio XIAO ESP32S3 (mit Antenne), WS2812B-Streifen 60 LEDs/m (16 LEDs), drei Leitungen, 3D-Druckteile von MakerWorld
- Home Assistant 2024.10 oder neuer, ESPHome 2026.9 oder neuer (getestet mit 2026.10)
- Integration **[Microsoft Graph](https://github.com/geoffreylagaisse/Hass-Microsoft-Graph)** (HACS) für die Teams-Präsenz
- Integration **[Workday](https://www.home-assistant.io/integrations/workday/)** (Werktage inkl. Feiertage)

### Hinweis zu Microsoft Graph

Die Graph-Integration braucht eine App-Registrierung in Microsoft Entra ID (Azure AD) deines Microsoft-365-Tenants. Für den eigenen Status genügen die delegierten Berechtigungen `Presence.Read` und `User.Read`. Viele Firmen-Tenants erlauben Nutzern keine eigenen App-Registrierungen oder Zustimmungen – dann muss die IT mitspielen. Details stehen im README der Integration.

## Einrichtung

### 1. Firmware

1. Im ESPHome Device Builder ein neues Gerät anlegen und den Inhalt von [`esphome/teams-status-licht.yaml`](esphome/teams-status-licht.yaml) einfügen.
2. `wifi_ssid`, `wifi_password` und `api_encrypt` in den Secrets hinterlegen (Vorlage: [`secrets.yaml.example`](esphome/secrets.yaml.example)).
3. Bei Bedarf `num_leds` (Standard 16) und `led_pin` anpassen.
4. Das erste Mal per USB flashen, danach per OTA (verschlüsselt mit dem API-Schlüssel).
5. In Home Assistant das gefundene Gerät hinzufügen. Die Leuchte heißt `light.teams_status_licht`.

### 2. Helligkeits-Helfer

Vier Helfer vom Typ **Zahlenwert** anlegen (5–100 %, Schrittweite 5), z. B. „Teams-Licht Helligkeit Rot/Gelb/Grün/Blau“. YAML-Nutzer können stattdessen [`packages/teams_status_licht.yaml`](packages/teams_status_licht.yaml) einbinden.

Bewährte Startwerte: Rot 100 %, Gelb 100 %, Grün 60 %, Blau 30 %.

### 3. Blueprints importieren

[![Blueprint "Teams-Statuslicht" importieren](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fsebastianrak%2Fha-teams-status-light%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fteams_status_licht.yaml)
Statusanzeige

[![Blueprint "Farbtest" importieren](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fsebastianrak%2Fha-teams-status-light%2Fblob%2Fmain%2Fblueprints%2Fscript%2Fteams_status_licht_farbtest.yaml)
Farbtest

Aus dem ersten Blueprint eine Automation erstellen (Teams-Aktivität, Person, Werktag-Sensor, Leuchte, die vier Helfer), aus dem zweiten ein Skript.

## Gut zu wissen

- **Helligkeit wirkt nicht linear.** ESPHome wendet eine Gammakorrektur von 2,8 an. 30 % im Regler ergeben nur rund 3 % Leistung. Niedrige Werte wirken deshalb deutlich dunkler, als die Zahl vermuten lässt.
- **Gelb und Grün:** Auf WS2812 wirkt Gelb oft leicht grünstichig. Bei Bedarf im Blueprint z. B. `255, 160, 0` wählen.
- **Verzögerung:** Wie schnell ein Statuswechsel ankommt, hängt vom Abfrageintervall der Graph-Integration ab – Sekunden, nicht Echtzeit.
- **Kein Kamerastatus:** Die Graph-Präsenz enthält keine Information, ob die Kamera an ist. Das ginge nur mit Software auf dem Arbeitsrechner, was dieses Projekt bewusst vermeidet.
- **InAMeeting/Busy** setzt Teams auch, wenn nur ein Kalendertermin läuft – deshalb Gelb statt Rot.

## Haftung

DIY-Projekt, Aufbau und Betrieb auf eigene Verantwortung. Vor dem ersten Einschalten Polung, Datenrichtung und Kurzschlussfreiheit prüfen.

Kein offizielles Produkt von Microsoft und nicht mit Ulrich Radig verbunden. Microsoft Teams ist eine Marke der Microsoft Corporation.

## Lizenz

Die Dateien in diesem Repository (Firmware-Konfiguration, Blueprints, Dokumentation) stehen unter der MIT-Lizenz, siehe [LICENSE](LICENSE). Sie gilt **nicht** für das Gehäuse: Für die 3D-Druckdateien gelten ausschließlich die Bedingungen auf MakerWorld.

---

## English summary

A monitor busy light that shows your Microsoft Teams presence, built entirely with **ESPHome** and **Home Assistant** – no software on your work computer. Presence comes from Microsoft Graph via the HACS integration [Microsoft Graph](https://github.com/geoffreylagaisse/Hass-Microsoft-Graph), so it works whether you use Teams on a laptop, in a browser or on your phone.

Inspired by the **[Radig StatusLight](https://makerworld.com/de/models/2955341-radig-status-light)** by Ulrich Radig. I use its 3D-printed parts and the same hardware (Seeed Studio XIAO ESP32S3, 16 × WS2812, data on GPIO1), so an existing Radig StatusLight can run this firmware without rewiring. **The 3D files are not included** – download them from MakerWorld and follow the designer's terms.

Contents: an ESPHome config (the device is a plain RGB light), an automation blueprint mapping Teams activity to colours (red pulsing = presenting, red = call/DND, yellow = meeting/busy, green = available, blue = away/inactive) only while you are home and – except for calls and presenting – only on workdays within working hours, a colour-test script blueprint, and optional `input_number` helpers for per-colour brightness. MIT licensed (excluding the enclosure). Not affiliated with Microsoft or Ulrich Radig.
