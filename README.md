# Automatyzacja stanowiska pomiarowego modułów fotowoltaicznych

Skrypt umożliwiający generowanie charakterystyk modułów fotowoltaicznych i eksport wyników w postaci raportu PDF. Kompatybilny ze sztucznym obciążeniem Array 3711A i podobnymi modelami. 

Stowrzony na potrzeby koła naukowego AGH Solar Plane w celu badania wydajności modułów fotowoltaicznych montowanych na skrzydłach samolotów solarnych.

W katalogu output znajduje się programw formacie exe

## Instalacja sterowników

Po podłączeniu interfejsu obciążenia w menedżerze urządzeń wyświetli się "PL2303HXA PHASED OUT SINCE 2012. PLEASE CONTACT YOUR SUPPLIER". Należy rozłączyć się z internetem, usunąć sterowniki tego urządzenia i ręcznie zainstalować sterowniki z katalogu Drivers. Jeśli po instalacji interfejs nie jest wykrywany to trzeba go odłączyć i podłączyć na nowo do komputera. Wtedy powinien zostać prawidłowo wykryty, a obok jego nazwy powinien pojawić się numer portu COM.