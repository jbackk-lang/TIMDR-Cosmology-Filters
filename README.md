# TIMDR Cosmology Filters

Nowy moduł — filtry anomalii dla danych kosmologicznych, budowane od
zera po audycie `GIA-TIMDR/docs/filters/al_filter_predictions.md`
(wcześniej w tej sesji), gdzie znaleziono błąd arytmetyczny, obalone
twierdzenie o gęstości cyfr i ogólny wzorzec numerologii (dobór
parametrów po fakcie, brak propagacji niepewności, brak korekty na
wielokrotne porównania). Cel: pokazać, jak wygląda **ta sama idea
filtra anomalii, ale zrobiona metodologicznie poprawnie**.

## Czym różni się to podejście od `al_filter_predictions.md`

| | GIA-TIMDR (`al_filter_predictions.md`) | Ten moduł |
|---|---|---|
| Dane wejściowe | ręcznie liczone cyfry dziesiętne √2, √3 | cytowane, publikowane pomiary (Planck, MESSENGER, SH0ES) |
| Model zerowy / predykcja | arbitralne kombinacje π/√2/√3 dobrane PO zobaczeniu wyniku | predykcja z ugruntowanej fizyki (ΛCDM, OTW) zdefiniowana PRZED liczeniem |
| Wynik | "% odchylenia" bez błędu pomiaru | z-score/p-value z propagacją niepewności obu wielkości |
| Korekta na wielokrotne porównania | brak (kilka "zbieżności" w tym samym dokumencie) | każdy filtr to jeden, z góry zdefiniowany test |
| Pozytywna kontrola (dowód, że metoda w ogóle coś wykrywa) | brak | tak — napięcie Hubble'a (patrz niżej) |
| Uczciwość przy niewygodnym wyniku | "status: remarkable" nawet przy błędach w obliczeniach | filtr CMB poniżej sam odrzucił własny naiwny model zerowy — i to jest udokumentowane jako taki wynik, nie ukryte |

## Trzy filtry

### 1. `cmb_peak_spacing_filter` — odstępy pików akustycznych CMB

Dane: Planck 2018, pozycje pierwszych trzech pików widma mocy TT
(Tabela 5, *Planck 2018 results. I. Overview*, arXiv:1807.06205;
potwierdzone niezależnie przez *Planck 2018 results. V*,
arXiv:1907.12875):

```
l1 = 220.6 ± 0.6
l2 = 538.1 ± 1.3
l3 = 809.8 ± 1.0
```

**Wynik**: naiwny model zerowy "piki są równoodległe w l" jest **silnie
odrzucony** (z≈21, p≈3×10⁻⁹⁸) — Δl(2-1)=317.5 vs Δl(3-2)=271.7.

**Uczciwa interpretacja**: to NIE jest anomalia we wszechświecie. To
znany, ugruntowany efekt fizyczny — tzw. "phase shift" pierwszego piku
oraz obciążenie barionowe powodują, że kolejne piki są coraz bliżej
siebie (malejący odstęp), nie równoodległe. Prosty model "stały
odstęp" był zbyt naiwny i sam filtr to wykrył. Zostawiono to w kodzie
celowo, jako uczciwy przykład: pre-zarejestrowany model zerowy może
się okazać sam w sobie błędny/uproszczony — trzeba to przyznać, a nie
interpretować duży z-score jako "odkrycie" (dokładnie odwrotność tego,
co robi `al_filter_predictions.md`). Pełny test zgodności z ΛCDM
wymagałby dopasowania całego widma mocy (MCMC), nie tylko trzech
pozycji pików.

### 2. `mercury_precession_filter` — precesja peryhelium Merkurego

Predykcja OTW: **42.98"/wiek** (Nobili & Will 1986; Biswas & Mani
2005) — bez wolnego parametru dopasowanego do Merkurego.

Dwie niezależne obserwacje testowane:

- Anderson et al. 1991 (radar ranging 1966–1988): excess precession =
  **42.94"/wiek**. Niepewność dla tej konkretnej liczby nie jest
  spójnie podawana w źródłach wtórnych (różne cytowania w literaturze
  mieszają ją z pokrewną wartością 43.13±0.14"/wiek liczoną względem
  innej linii bazowej) — użyto tu konserwatywnie 0.20"/wiek, jawnie
  oznaczone jako przyjęte założenie.
- Park et al. 2017 (MESSENGER ranging, arXiv/AJ 153:121): całkowita
  precesja = **575.3100 ± 0.0015"/wiek** (najdokładniejszy dostępny
  pomiar). Wkład Newtonowski (nie-relatywistyczny) z niezależnej
  symulacji N-ciał (Pogossian 2022, arXiv:2112.07301) zbiega do
  **532.1"/wiek**. Wyprowadzona wartość "GR-only" = 575.31−532.1 =
  43.21"/wiek. **Uwaga uczciwościowa**: literaturowe wartości wkładu
  Newtonowskiego wahają się od 526.7 do 532.37"/wiek u różnych autorów
  (patrz Pogossian 2022, przegląd w Tabeli tegoż artykułu) — ten
  rozrzut jest WIĘKSZY niż błąd pomiaru MESSENGER, więc użyto
  konserwatywnej niepewności 0.5"/wiek dla wyprowadzonej wartości,
  żeby nie sugerować fałszywej precyzji.

**Wynik obu testów**: z=0.20 i z=0.46 — pełna zgodność z OTW,
niezależnie od tego, które z dwóch różnych, niezależnych źródeł
historycznych danych się użyje. To jest różnica względem
`al_filter_predictions.md`, który używał JEDNEJ, niesprawdzonej
wartości bez żadnej niepewności ("×Al₋ = 42.9362", "deviation: 0.15%",
bez wskazania z jakiego pomiaru pochodzi porównanie ani jaki jest jego
błąd).

### 3. `hubble_tension_filter` — napięcie Hubble'a (kontrola pozytywna)

```
H0 (SH0ES/JWST, Riess et al. 2025): 73.49 ± 0.93 km/s/Mpc
H0 (Planck 2018 + ΛCDM):            67.4  ± 0.5  km/s/Mpc
```

**Wynik**: z≈5.77, p≈8×10⁻⁹ — silne, statystycznie jednoznaczne
napięcie. To zgadza się z szeroko publikowanym w literaturze wynikiem
(">5σ", "Hubble tension") — patrz źródła niżej.

**Dlaczego to jest ważne dla wiarygodności całego modułu**: żaden z
filtrów w `GIA-TIMDR/al_filter_predictions.md` nie miał pozytywnej
kontroli — czyli przypadku, w którym metoda POWINNA wykryć dużą
rozbieżność i rzeczywiście ją wykrywa. Tutaj taki przypadek jest,
i filtr go poprawnie wykrywa z ogromną istotnością statystyczną. To
pokazuje, że framework faktycznie coś mierzy, a nie tylko zawsze
potwierdza brak anomalii.

## Uruchomienie

```bash
pip install pytest
pytest -q          # 7/7 testów
python3 -c "from cosmology_filters import *; print(hubble_tension_filter(73.49,0.93,67.4,0.5))"
```

## Źródła

- Planck Collaboration, *Planck 2018 results. I. Overview and the
  cosmological legacy of Planck*, arXiv:1807.06205 (Tabela 5: pozycje
  pików).
- Planck Collaboration, *Planck 2018 results. V. CMB power spectra and
  likelihoods*, arXiv:1907.12875.
- Planck Collaboration, *Planck 2018 results. VI. Cosmological
  parameters*, arXiv:1807.06209 (H0 = 67.4±0.5 km/s/Mpc).
- Nobili A.M., Will C.M. 1986, *Nature* 320:39–41 (predykcja OTW
  42.98"/wiek).
- Anderson J.D. i in. 1991, *Publ. Astron. Soc. Aust.* 9(2):324
  (radar ranging, excess precession 42.94"/wiek).
- Park R.S. i in. 2017, *AJ* 153(3):121 (MESSENGER ranging, całkowita
  precesja 575.3100±0.0015"/wiek).
- Pogossian S.P. 2022, *Celestial Mech. Dyn. Astron.*, arXiv:2112.07301
  (przegląd literaturowych wartości wkładu Newtonowskiego; własna
  symulacja N-ciał zbiegająca do 532.1"/wiek).
- Riess A.G. i in. 2022/2025 (SH0ES/JWST), H0 ≈ 73.0–73.5 km/s/Mpc.

## Ograniczenia (uczciwie)

- `cmb_peak_spacing_filter` to filtr przesiewający na trzech liczbach,
  nie zastępstwo dla pełnego dopasowania widma mocy CMB (MCMC/CAMB).
- Niepewność dla starszych pomiarów (Anderson 1991, wkład Newtonowski)
  jest oszacowana konserwatywnie, nie wzięta z jednego jednoznacznego
  źródła — oznaczone w kodzie i testach.
- Moduł nie implementuje pełnych modeli kosmologicznych (ΛCDM
  parameter fitting) — to są proste, ale metodologicznie poprawne
  testy zgodności/napięcia między konkretnymi liczbami z literatury.
