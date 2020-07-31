# 1live-plays

## 4 Gewinnt über YouTube Live Streams
Ein Spiel, bei dem zwei YouTube-Channel in Livestreams gegeneinander 4 Gewinnt spielen können. Züge werden im Livechat getätigt.

Das Projekt ist darauf vorbereitet, auf einem Linux-Server ohne physischem Bildschirm zu laufen. Das Spiel an sich läuft auch unter Windows, nur das Streaming muss dann selbst gelöst werden.

## Grundsätzliche Funktionsweise
Je "Spieler" gibt es einen Thread, der periodisch den Live-Chat abruft. Wenn der Democracy-Mode aktiv ist, gibt es einen zweiten Thread der die Votes aggregiert. Der Code hierfür findet sich in `bot.py`.

Die `main.py` orchestriert dann die Voting-Ergebnisse mit der Zeitsteuerung der Züge, UI-Updates und Spiellogik.

Im Production-Deploy haben wir verschiedene Varianten probiert, um das Spiel dann an beide Livestreams zu übertragen. Unser aktuelles Deployment sieht folgendes vor:

- Es wird ein virtueller X-Framebuffer gestartet in Größe des Spielfensters (`scripts/start_x.sh`)
- Das Spiel läuft in diesem Framebuffer im Vollbild-Modus (`scripts/start_game.sh`)
- Der Framebuffer wird von `ffmpeg` encoded und an einen lokalen `nginx`-Server geschickt (`scripts/start_nginx_stream.sh`)
    - Alternativ kann `ffmpeg` auch direkt den encodeten Stream duplizieren und an YouTube schicken (`scripts/start_dual_stream.sh`). Der Schritt über `nginx` hat aber in unseren Tests bessere Ergebnisse geliefert.
- Der `nginx`-Server pusht den Stream raus an beide Livestream-Endpoints
    - Ein `nginx`-Build mit dem [`rtmp`-Modul](https://www.nginx.com/products/nginx/modules/rtmp-media-streaming/) wird benötigt.

In unseren Tests lief das Spiel inkl. Streams in diesem Setup stabil über einen Monat.

## Setup
- `virtualenv` anlegen, aktivieren und via `pip install -r requirements.txt` die Abhängigkeiten installieren
- Eine `config.json` anlegen (`config.sample.json` als Vorlage verwenden)

## Live-Betrieb
- In der Google Cloud Console ein Projekt anlegen, einen API-Key für die YouTube Data API generieren und diesen in der `config.json` eintragen
    - Soll das Spiel 24/7 laufen, müssen zusätzliche API-Token beantragt werden
- In YouTube die Livestreams anlegen und auf "Nicht gelistet" stellen
- Die Video-IDs der beiden Livestreams in der `config.json` eintragen
- Eine `nginx.conf` anlegen (`nginx.sample.conf` als Vorlage verwenden) und die Stream-Keys eintragen
- Virtuellen Framebuffer starten
- Spiel starten
- `nginx` starten
- `ffmpeg`-Encoding starten

## Konfigurationsoptionen
Neben der Konfiguration der beiden Spieler können in der `config.json` zusätzlich folgende Einstellungen vorgenommen werden:

- `app.debug`: Wenn der Wert auf `true` gesetzt wird, kann man lokal über Tastatureingaben spielen.
- `app.game_mode`: Man kann wählen zwischen `"democracy"` (Meiste Stimmen für eine Spalte entscheiden) und `"first_come_first_serve"` (Erste Stimme für eine Spalte entscheidet).
- `app.democracy_timeout`: Zeitspanne in Sekunden in der Votes gesammelt werden
- `app.one_vote_per_person`: Entscheidet darüber, ob alle Stimmen des gleichen Users gezählt werden, oder nur die letzte.
- `app.prevent_switching_sides`: Wenn auf `true` gesetzt, können User während das Spiel läuft nicht für die Gegenseite abstimmen. Die erste Stimme, die man in einem Spiel abgibt, entscheidet darüber, zu welcher Seite man gehört.

## Copyright
Der Programmcode ist lizenziert unter der MIT-Lizenz. Für Grafiken, Design und Schriften werden alle Rechte vorbehalten.
