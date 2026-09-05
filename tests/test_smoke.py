import unittest

from vinaya import LatticeHealth, VinayaGovernor
from vinaya.runtime import load_vinaya_json, validate_schema


class LatticeVinayaSmokeTests(unittest.TestCase):
    def test_configuration_loads_and_validates(self):
        data = load_vinaya_json("lattice-vinaya.json")
        self.assertTrue(validate_schema(data))

    def test_governor_constructs(self):
        lattice = LatticeHealth()
        governor = VinayaGovernor(lattice)
        self.assertIsNotNone(governor)


if __name__ == "__main__":
    unittest.main()
