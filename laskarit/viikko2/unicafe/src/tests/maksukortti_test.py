import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1)
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.01 euroa")

    def test_saldo_vahenee_oikein_jos_raha_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1)
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 9.99 euroa")

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1001)
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.00 euroa")

    def test_metodi_palauttaa_true_jos_rahat_riittivat_ja_muuten_false(self):
        self.assertTrue(self.maksukortti.ota_rahaa(800))
        self.assertFalse(self.maksukortti.ota_rahaa(800))
