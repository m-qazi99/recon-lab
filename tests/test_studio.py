import unittest, sys, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run

class StudioTests(unittest.TestCase):
 def sample(self):return json.loads((R/'examples/studio.json').read_text())
 def execute(self,**changes):
  p=self.sample();p.update(changes);return run(p)['lab']
 def test_preview_metrics_match_python(self):
  source=(R/'docs/sample-result.js').read_text();preview=json.loads(source.removeprefix('window.SAMPLE_RESULT=').removesuffix(';'));self.assertEqual(preview['metrics'],run(self.sample())['metrics'])
 def test_json_serializable(self):json.dumps(run(self.sample()),allow_nan=False)
 def test_frontier_monotonic(self):
  vals=[x['matching'] for x in self.execute()['frontier']];self.assertEqual(vals,sorted(vals))
 def test_relative_tolerance_source_based(self):
  l=self.execute(source='id,n\n1,100',target='id,n\n1,110',compare='n',tolerance=0,relative=10,keys='id');self.assertEqual(l['records'][0]['status'],'matched')
 def test_decimal_exact_boundary(self):
  l=self.execute(source='id,n\n1,0.1',target='id,n\n1,0.3',compare='n',tolerance='.2',keys='id');self.assertEqual(l['records'][0]['status'],'matched')
 def test_text_normalization_is_explicit(self):
  p={'source':'id,s\n1,Hello','target':'id,s\n1, hello ','compare':'s','keys':'id'}
  self.assertEqual(self.execute(**p,normalize=False)['records'][0]['status'],'changed');self.assertEqual(self.execute(**p,normalize=True)['records'][0]['status'],'matched')
 def test_missing_and_extra_not_tolerance_fixed(self):
  a=self.execute(tolerance=0);b=self.execute(tolerance=100000)
  self.assertEqual(a['counts']['missing'],b['counts']['missing']);self.assertEqual(a['counts']['target_only'],b['counts']['target_only'])
 def test_control_totals_use_all_records(self):
  l=self.execute(source='id,n\n1,10\n2,20',target='id,n\n1,15',compare='n',keys='id');t=next(x for x in l['totals'] if x['column']=='n');self.assertEqual(t['delta'],'-15')
 def test_blank_key_rejected(self):
  with self.assertRaises(ValueError):self.execute(source='id,n\n,10',keys='id',compare='')
 def test_relative_bounds(self):
  with self.assertRaises(ValueError):self.execute(relative=101)
 def test_mismatch_contains_exact_values(self):
  l=self.execute(source='id,n\n1,10',target='id,n\n1,13',compare='n',keys='id',tolerance=0);self.assertEqual(l['records'][0]['cells'][0]['delta'],'3')
