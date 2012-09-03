FlaskMaschines
==============

## FlaskMaschines jest to przykładowa web aplikacja napisana w Pythonie z wykorzystaniem frameworka Flask.

### Instalacja
Instalacje wykonujemy najlepiej z użyciem virutalenv. Plik requiments.txt definuje listę wymaganych pakietów dla instalatora pip (wymagana wersja Pythona 2.7.2).
Aplikacja wykorzystuje bazę danych SQLite. Należy upewnić się, czy plik database.db ma pełne uprawnienia dostępu (777).

### Użycie
Użytkownik ze strony głównej wybiera jedno zadania i listę maszyn, które mają je wykonać. Następnie zadanie jest przesyłane do serwera i zapamiętywane. 
W kolejnych zapytaniach sprawdzany jest czas jego realizacji na kolejnych etapach dla każdej z maszyn. Stan wykonania prezentowany jest na liście. Dopiero po
wykonaniu zadania na wszystkich maszynach można zlecić kolejen z nich do realizacji.


