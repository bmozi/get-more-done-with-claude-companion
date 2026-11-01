import unittest,tempfile
from pathlib import Path
from reference import valid_identifier,within_limit,inspect_cards
class PracticeTests(unittest.TestCase):
 def test_accepted_identifiers(self):
  for value in ['VT-AB07', 'VT-ZZ99']:self.assertTrue(valid_identifier(value),value)
 def test_rejected_identifiers(self):
  for value in ['VT-Ab07', 'VT-AB7', 'VT-AB007', 'XVT-AB07', 'VT-AB07\n']:self.assertFalse(valid_identifier(value),value)
 def test_limit_boundary(self):
  self.assertEqual([within_limit(n,12) for n in [11, 12, 13]],[True,True,False])
 def test_actual_deck(self):self.assertEqual(inspect_cards(Path(__file__).with_name('flashcards.txt')),4)
 def test_bad_card_shapes(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'bad.txt'
   for bad in ['Q\t\n','Q\tA\textra\n','Q\tA\nQ\tB\n','Q\\tA\n','']:
    p.write_text(bad)
    with self.assertRaises(ValueError):inspect_cards(p)
if __name__=='__main__':unittest.main()
