import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luodun_kassapäätteen_rahamäärä_ja_myytyjen_lounaiden_määrä_on_oikea(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_riittavasti_rahaa(self):
        raha0 = self.kassapaate.kassassa_rahaa
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
        raha1 = self.kassapaate.kassassa_rahaa
        draha = raha1 - raha0
        self.assertEqual(draha, 240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_edullisesti_ei_riittavasti_rahaa(self):
        edulliset = self.kassapaate.edulliset
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(30), 30)
        self.assertEqual(self.kassapaate.edulliset, edulliset)

    def test_syo_maukkaasti_riittavasti_rahaa(self):
        raha0 = self.kassapaate.kassassa_rahaa
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
        raha1 = self.kassapaate.kassassa_rahaa
        draha = raha1 - raha0
        self.assertEqual(draha, 400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_maukkaasti_ei_riittavasti_rahaa(self):
        maukkaat = self.kassapaate.maukkaat
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(30), 30)
        self.assertEqual(self.kassapaate.maukkaat, maukkaat)

    def test_syo_kortilla_edullisesti_riittavasti_rahaa(self):
        kortti = Maksukortti(300)
        rahaa = self.kassapaate.kassassa_rahaa
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(rahaa, self.kassapaate.kassassa_rahaa)

    def test_syo_kortilla_edullisesti_ei_riittavasti_rahaa(self):
        kortti = Maksukortti(200)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_kortilla_maukkaasti_riittavasti_rahaa(self):
        kortti = Maksukortti(500)
        rahaa = self.kassapaate.kassassa_rahaa
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(rahaa, self.kassapaate.kassassa_rahaa)

    def test_syo_kortilla_maukkaasti_ei_riittavasti_rahaa(self):
        kortti = Maksukortti(200)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_lataa_rahaa_kortille(self):
        kortti = Maksukortti(200)
        rahaa0 = self.kassapaate.kassassa_rahaa
        self.kassapaate.lataa_rahaa_kortille(kortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa0 + 100)

    def test_lataa_rahaa_kortille_negatiivinen_maara(self):
        kortti = Maksukortti(200)
        rahaa0 = self.kassapaate.kassassa_rahaa
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, rahaa0)
