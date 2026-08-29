# Instrukcja obsługi

## Konfiguracja środowiska:

Program był testowany w środowisku stworzonym przy pomocy komendy:

~~~

conda create -y -n my_env python=3.11 sympy numpy matplotlib

~~~

## Flow programu

Za uruchomienie programu odpowiedzialny jest plik particles.py, który uruchamia lagrangian.py w podprocesie, ten pyta użytkownika o dane dotyczące symulacji, wczytuje wybrany lagrangian z pliku Files_withL.py zapisany w składni kodu SymPy i generuje plik nagłówkowy generated_physics.h.  



Plik ten jest importowany przez solver.c, który odpowiada za przeprowadzanie obliczeń przy uzyciu metody Rungego-Kutty 4. rzędu. Pliki w C są kompilowane w locie.  



Warunki począstkowe są ustawiane jednakowo dla wszystkich lagrangianów, co prowadzi potencjalnie do problemów, gdyż zmienne uogólnione niekoniecznie są położeniem we spółrzednych kartezjańskich, a projekt skupiał się na dodaniu możliwości dopisywania kolejnych lagrangianów bez zapewnienia konwersji na zmienne x, y.  



Na koniec pliki odpowiedzialne za animację oraz obliczenia współpracują przy wyświetlaniu symulacji.  

## Uruchamianie

Aby uruchomić program, wystarczy użyć komendy:

~~~

python3 -m particles [liczba_cząstek]

~~~

i następnie wybrać lagrangian z wyświetlonej listy, podając właściwy numer.  

## Dodanie nowego lagrangianu

W celu przetestowania własnego lagrangianu należy dodać odpowiadający mu case w pliku Files_withL.py oraz zmodyfikować wyświetlaną listę w pliku lagrangian.py. W przypadku użycia niezdefiniowanych wcześniej zmiennych należy dopisać je wewnątrz metody generate_c_function.  

## Uwagi końcowe

Ze względu na brak uwzględnienia rodzaju zmiennych uogólnionych przy ustalaniu warunków początkowych oraz wyświetlanie wykresu we współrzędnych uogólnionych zaleca się użycia większej liczby ciał, np. 10, wtedy interpretacja poprawności wyników jest prostsza oraz jest większa pewność, że chociaż część cząstek zostanie utworzona z warunkami początkowymi, które nie spowodują szybkich i nieintuicyjnych błędów w symulacji (np. znikanie cząstek).  