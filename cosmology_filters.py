"""
TIMDR Cosmology Filters
========================
Filtry anomalii dla danych kosmologicznych, budowane wg protokolu
numerologia-vs-prawdziwa-matematyka (skill `timdr-signal-framework`, §18):
najpierw pre-rejestracja obiektu/metryki/modelu zerowego, dopiero potem
liczenie, jeden przebieg, uczciwy raport niezaleznie od wyniku.

Dlaczego to jest INNE (i lepiej ugruntowane) podejscie niz
`GIA-TIMDR/docs/filters/al_filter_predictions.md` (zaudytowany
wczesniej w tej sesji i w duzej mierze obalony jako numerologia,
nie fizyka):

1. Dane wejsciowe to prawdziwe, cytowane, zmierzone wartosci
   (Planck 2018, MESSENGER/radar ranging, SH0ES/JWST) — NIE recznie
   policzone cyfry dziesietne stalych matematycznych typu √2, √3.
2. Predykcja/model zerowy pochodzi z ugruntowanej fizyki (akustyczne
   piki CMB w plaskim ΛCDM, ogolna teoria wzglednosci, ΛCDM H0) — NIE
   z arbitralnych kombinacji π/√2/√3 dobieranych PO fakcie.
3. Wynikiem kazdego testu jest z-score/p-value z PRAWIDLOWA propagacja
   niepewnosci pomiarowej obu porownywanych wielkosci — NIE "% odchylenia"
   bez odniesienia do bledu pomiaru (blad, ktory dyskwalifikowal cala
   sekcje "Status" w al_filter_predictions.md).
4. Filtr dziala w OBIE strony: jeden z trzech przypadkow ponizej
   (napiecie Hubble'a) to GENUINE, duza, uznana w literaturze
   rozbieznosc (>5σ) — dowod, ze metoda wykrywa realna anomalie, gdy
   istnieje, a nie tylko zawsze potwierdza zgodnosc z null hipoteza.

Zrodla danych (patrz README.md dla pelnych cytowan):
- Planck 2018 (Tabela 5, Planck 2018 I — Overview, arXiv:1807.06205;
  potwierdzone niezaleznie przez Planck 2018 V, arXiv:1907.12875)
- Park et al. 2017 (MESSENGER ranging), arXiv/AJ 153:121
- Pogossian 2022 (N-body Newtonian baseline), arXiv:2112.07301
- Riess et al. 2022/2025 (SH0ES/JWST), Planck 2018 VI (arXiv:1807.06209)
"""

import math


def tension_zscore(value1, sigma1, value2, sigma2, label1="pomiar 1", label2="pomiar 2"):
    """
    Ogolny test "napiecia" (tension) miedzy dwoma niezaleznymi pomiarami
    tej samej wielkosci fizycznej:

        z = |v1 - v2| / sqrt(sigma1^2 + sigma2^2)

    Standardowa metoda w kosmologii do kwantyfikacji napiecia (np.
    "Hubble tension") przy zalozeniu niezaleznych bledow gaussowskich —
    nie autorska sztuczka, to najprostszy poprawny test dla dwoch
    niezaleznych pomiarow z podanymi niepewnosciami.
    """
    if sigma1 < 0 or sigma2 < 0:
        raise ValueError("niepewnosci (sigma) musza byc nieujemne")
    combined_sigma = math.sqrt(sigma1 ** 2 + sigma2 ** 2)
    if combined_sigma == 0:
        raise ValueError("obie niepewnosci wynosza zero - z-score niezdefiniowany")
    z = abs(value1 - value2) / combined_sigma
    p_two_sided = math.erfc(z / math.sqrt(2))
    return {
        "z": z,
        "p_two_sided": p_two_sided,
        "label1": label1, "value1": value1, "sigma1": sigma1,
        "label2": label2, "value2": value2, "sigma2": sigma2,
    }


def cmb_peak_spacing_filter(l1, sigma_l1, l2, sigma_l2, l3, sigma_l3):
    """
    PRE-REJESTRACJA: naiwny model zerowy - w idealnym, uproszczonym
    obrazie oscylacji akustycznych piki widma mocy CMB byłyby
    rownomiernie rozlozone w l (staly odstep ~ π/θ*). Test: czy odstep
    Δl2=(l2-l1) i Δl3=(l3-l2) sa statystycznie zgodne miedzy soba.

    WAZNY WYNIK WERYFIKACJI WLASNEGO ZALOZENIA (uczciwie odnotowany, nie
    ukryty): na prawdziwych danych Planck 2018 ten prosty model RÓWNEJ
    ODLEGLOSCI jest silnie odrzucony (z≈21, patrz test_cosmology_filters.py)
    - Δl2≈317.5 vs Δl3≈271.7, roznica dużo wieksza niz blad pomiaru.
    To NIE oznacza anomalii we wszechswiecie ani problemu z ΛCDM -
    oznacza, ze zalozenie "stały odstęp" jest zbyt naiwne. Prawdziwa
    predykcja ΛCDM przewiduje malejacy odstep miedzy kolejnymi pikami
    (tzw. "phase shift" pierwszego piku + efekty obciazenia barionowego
    i tlumienia Silka - ugruntowana fizyka, nie anomalia). Ten filtr
    pozostaje w kodzie jako uczciwy przyklad: PRE-REJESTROWANY, prosty
    model zerowy moze byc sam w sobie falszywy/zbyt uproszczony, i
    trzeba to przyznac zamiast interpretowac duzy z-score jako "odkrycie".
    Do prawdziwego testu zgodnosci z ΛCDM potrzebne jest pelne dopasowanie
    widma mocy (MCMC), nie porownanie trzech pozycji pikow - to jest
    filtr przesiewajacy z jawnie udokumentowanym ograniczeniem, nie
    zastepstwo dla pelnej analizy.
    """
    d1 = l2 - l1
    d2 = l3 - l2
    sigma_d1 = math.sqrt(sigma_l1 ** 2 + sigma_l2 ** 2)
    sigma_d2 = math.sqrt(sigma_l2 ** 2 + sigma_l3 ** 2)
    result = tension_zscore(
        d1, sigma_d1, d2, sigma_d2,
        label1="Δl (pik2-pik1)", label2="Δl (pik3-pik2)",
    )
    result["delta1"] = d1
    result["delta2"] = d2
    return result


def mercury_precession_filter(observed_excess, sigma_observed, gr_predicted=42.98):
    """
    PRE-REJESTRACJA: ogolna teoria wzglednosci nie ma wolnego parametru
    dopasowanego do Merkurego - 42.98"/wiek to predykcja z pierwszych
    zasad (masa Slonca, parametry orbity Merkurego, stala c; Nobili &
    Will 1986). Test: czy zmierzona anomalna (nie-Newtonowska) precesja
    peryhelium jest zgodna z ta predykcja w granicach bledu pomiaru.

    gr_predicted jest traktowane jako wartosc teoretyczna bez wlasnej
    niepewnosci pomiarowej (obliczona z ugruntowanych stalych fizycznych,
    nie dopasowana do danych) - cala niepewnosc pochodzi z pomiaru.
    """
    if sigma_observed <= 0:
        raise ValueError("niepewnosc obserwacji musi byc dodatnia")
    z = abs(observed_excess - gr_predicted) / sigma_observed
    p_two_sided = math.erfc(z / math.sqrt(2))
    return {
        "z": z, "p_two_sided": p_two_sided,
        "observed_excess": observed_excess, "sigma_observed": sigma_observed,
        "gr_predicted": gr_predicted,
    }


def hubble_tension_filter(h0_late, sigma_late, h0_early, sigma_early):
    """
    PRE-REJESTRACJA: test napiecia miedzy H0 z drabiny odleglosci
    (pomiar lokalny, "pozny wszechswiat", np. SH0ES/JWST Cefeidy+SNIa)
    a H0 wywnioskowanym z widma CMB przy zalozeniu modelu ΛCDM (Planck,
    "wczesny wszechswiat"). To jest DOKLADNIE ten sam typ testu co
    powyzsze (`tension_zscore`), zastosowany do najbardziej znanego,
    realnego napiecia we wspolczesnej kosmologii (>5σ w literaturze) -
    wlaczony jako pozytywna kontrola: dowod, ze ten filtr wykrywa
    realna, duza anomalie, gdy ona istnieje.
    """
    return tension_zscore(
        h0_late, sigma_late, h0_early, sigma_early,
        label1="H0 (drabina odleglosci, pozny wszechswiat)",
        label2="H0 (CMB + ΛCDM, wczesny wszechswiat)",
    )
