"""
Testy z prawdziwymi, cytowanymi wartosciami (patrz README.md dla zrodel
i pelnych cytowan). Kazdy test to jeden pre-zarejestrowany przypadek,
nie przeszukiwanie parametrow.
"""
import math
import pytest
from cosmology_filters import (
    tension_zscore,
    cmb_peak_spacing_filter,
    mercury_precession_filter,
    hubble_tension_filter,
)


def test_tension_zscore_identyczne_pomiary_daje_zero():
    r = tension_zscore(100.0, 1.0, 100.0, 1.0)
    assert r["z"] == 0.0
    assert r["p_two_sided"] == pytest.approx(1.0)


def test_tension_zscore_odrzuca_ujemna_niepewnosc():
    with pytest.raises(ValueError):
        tension_zscore(1.0, -1.0, 2.0, 1.0)


def test_tension_zscore_odrzuca_dwie_zerowe_niepewnosci():
    with pytest.raises(ValueError):
        tension_zscore(1.0, 0.0, 2.0, 0.0)


def test_cmb_peak_spacing_planck_2018_falsyfikuje_naiwny_model_rownej_odleglosci():
    """
    Planck 2018 (Tabela 5, arXiv:1807.06205; potwierdzone przez
    arXiv:1907.12875): l1=220.6±0.6, l2=538.1±1.3, l3=809.8±1.0.

    UCZCIWY WYNIK: naiwny model zerowy "piki rownoodlegle" jest tu
    SILNIE ODRZUCONY (z≈21, p≈3e-98) - Δl2=317.5 vs Δl3=271.7. To
    ZGODNE z prawdziwa fizyka ΛCDM (znany efekt "phase shift" +
    obciazenie barionowe daja malejacy odstep miedzy kolejnymi pikami),
    NIE jest to anomalia we wszechswiecie. Test pilnuje, zeby filtr
    poprawnie wykrywal te (oczekiwana) niezgodnosc z uproszczonym
    modelem, zamiast cichej pomylki w kodzie dajacej z≈0.
    """
    r = cmb_peak_spacing_filter(220.6, 0.6, 538.1, 1.3, 809.8, 1.0)
    assert r["delta1"] == pytest.approx(317.5)
    assert r["delta2"] == pytest.approx(271.7)
    assert math.isfinite(r["z"])
    assert r["z"] > 10  # naiwny model rownej odleglosci jest zdecydowanie odrzucony - to oczekiwane, patrz docstring


def test_mercury_precession_zgodny_z_gr_anderson_1991():
    """
    GR: 42.98"/wiek (Nobili & Will 1986). Anderson et al. 1991 (radar
    ranging 1966-1988): excess precession = 42.94"/wiek. Niepewnosc
    dla tej konkretnej wartosci nie jest spojnie podawana w zrodlach
    wtornych (patrz README) - uzywamy tu konserwatywnie 0.20"/wiek
    (typowy rzad wielkosci niepewnosci radarowych pomiarow z tej ery),
    jawnie oznaczone jako przyjete zalozenie, nie wartosc z jednego,
    jednoznacznego zrodla.
    """
    r = mercury_precession_filter(observed_excess=42.94, sigma_observed=0.20)
    assert r["z"] < 2.0, f"z={r['z']:.2f} - nieoczekiwane napiecie z GR dla dobrze potwierdzonego wyniku"


def test_mercury_precession_zgodny_z_gr_messenger_park_2017():
    """
    Park et al. 2017 (MESSENGER): calkowita precesja = 575.3100 ±
    0.0015"/wiek (najdokladniejszy dostepny pomiar). Newtonowski
    (nie-relatywistyczny) wklad wg niezaleznej symulacji N-cial
    (Pogossian 2022, arXiv:2112.07301): zbiega do 532.1"/wiek dla
    przedzialow dopasowania ~1000 lat.

    Roznica literaturowych wartosci wkladu Newtonowskiego (od 526.7 do
    532.37"/wiek u roznych autorow, patrz README) jest WIEKSZA niz
    niepewnosc samego pomiaru MESSENGER - dlatego uzywamy tu szerokiej,
    konserwatywnej niepewnosci 0.5"/wiek dla wyprowadzonej "obserwowanej"
    wartosci GR, zeby uczciwie odzwierciedlic te dominujaca niepewnosc
    systematyczna (nie sam blad pomiaru MESSENGER, ktory jest
    znikomy).
    """
    observed_gr_part = 575.3100 - 532.1  # = 43.21
    r = mercury_precession_filter(observed_excess=observed_gr_part, sigma_observed=0.5)
    assert r["z"] < 2.0, f"z={r['z']:.2f} - nieoczekiwane napiecie z GR"


def test_hubble_tension_jest_realna_i_duza():
    """
    SH0ES/JWST (Riess et al. 2025): H0 = 73.49 ± 0.93 km/s/Mpc.
    Planck 2018 + ΛCDM: H0 = 67.4 ± 0.5 km/s/Mpc.
    Znane, publikowane napiecie: >5σ. To POZYTYWNA KONTROLA - filtr
    MUSI wykryc te anomalie, bo jest ona realna i szeroko potwierdzona
    w literaturze (w przeciwienstwie do numerologii w GIA-TIMDR, gdzie
    zaden "filtr" nie mial takiej niezaleznie potwierdzonej pozytywnej
    kontroli).
    """
    r = hubble_tension_filter(h0_late=73.49, sigma_late=0.93, h0_early=67.4, sigma_early=0.5)
    assert r["z"] > 5.0, f"z={r['z']:.2f} - filtr nie wykryl znanego, realnego napiecia Hubble'a"
    assert r["p_two_sided"] < 1e-6
