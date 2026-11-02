# Verdrahtung

Die Verdrahtung entspricht der des [Radig StatusLight](https://makerworld.com/de/models/2955341-radig-status-light): Die Datenleitung liegt auf **GPIO1**. Ein bereits aufgebautes Radig StatusLight lässt sich daher ohne Umlöten mit dieser Firmware betreiben.

## Anschlüsse

| XIAO ESP32S3 | Leitung (Radig) | WS2812-Streifen |
|---|---|---|
| 5V | rot | +5V |
| GND | schwarz | GND |
| D0 (GPIO1) | grün | DIN |

```
 USB-C-Netzteil ──► XIAO ESP32S3

 XIAO 5V  ─────────────────────── Streifen +5V
 XIAO GND ─────────────────────── Streifen GND
 XIAO D0  ─────────────────────── Streifen DIN
```

Der Streifen wird über den 5V-Pin des XIAO versorgt, also direkt aus USB. Ein separates Netzteil ist nicht nötig.

## Hinweise

- **Datenrichtung:** Am Streifenanfang anlöten, also dort, wo die Pfeile **weg**zeigen (Pad `DIN`/`DI`, nicht `DO`).
- **Pegel:** WS2812B erwarten laut Datenblatt mindestens 0,7 × VDD ≈ 3,5 V am Dateneingang, der ESP32-S3 liefert 3,3 V. Bei kurzer Datenleitung funktioniert das in der Praxis meist zuverlässig. Bei Flackern oder falschen Farben hilft ein Pegelwandler (z. B. 74AHCT125) oder ein Widerstand von etwa 330 Ω in der Datenleitung nahe am Streifen.
- **Strapping-Pin:** D2 (GPIO3) nicht für die Datenleitung verwenden.
- **Antenne:** Der XIAO ESP32S3 hat keine Platinenantenne. Ohne die mitgelieferte U.FL-Antenne ist das WLAN sehr schwach.
- **Strom (Schätzung):** Pro LED und Farbkanal etwa 20 mA bei voller Helligkeit. 16 LEDs in Rot ≈ 0,3 A, volles Weiß ≈ 1 A. Ein USB-Netzteil mit mindestens 2 A ist ausreichend.
- **Erstes Flashen:** Wird der XIAO nicht erkannt, die Taste BOOT gedrückt halten und dabei das USB-Kabel einstecken.

## Löten

| Lot | Lötspitze |
|---|---|
| bleihaltig (Sn60Pb40, Sn63Pb37) | 320–350 °C |
| bleifrei (z. B. SAC305) | 350–380 °C |

Pads des LED-Streifens kurz (2–3 s) und mit etwas Flussmittel löten; die Flexplatine löst sich bei zu langer Hitze ab.
