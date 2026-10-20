import unittest,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'src'))
from engine import run
from common import read_csv
class EngineTests(unittest.TestCase):
 def sample(self):return json.loads((R/'examples/sample.json').read_text())
 def test_empty_csv_rejected(self):
  with self.assertRaises(ValueError):read_csv('')
 def test_duplicate_headers_rejected(self):
  with self.assertRaises(ValueError):read_csv('a,a\n1,2')
 def test_ragged_csv_rejected(self):
  with self.assertRaises(ValueError):read_csv('a,b\n1')
 def test_quoted_csv_and_bom(self):
  h,r=read_csv('\ufeffid,note\n1,"hello, world"');self.assertEqual(r[0]['note'],'hello, world')
 def test_sample_tolerance_and_missing(self):
  r=run(self.sample());self.assertEqual([m['value']for m in r['metrics']],[2,1,1,1])
 def test_duplicate_keys_rejected(self):
  with self.assertRaises(ValueError):run({'source':'id,v\n1,a\n1,b','target':'id,v\n1,a','keys':'id'})
 def test_blank_keys_rejected(self):
  with self.assertRaises(ValueError):run({'source':'id,v\n,a','target':'id,v\n1,a','keys':'id'})
 def test_composite_key(self):
  data='id,region,v\n1,A,x\n1,B,y';r=run({'source':data,'target':data,'keys':'id,region'});self.assertEqual(r['metrics'][0]['value'],2)
 def test_decimal_boundary(self):
  r=run({'source':'id,v\n1,0.1','target':'id,v\n1,0.3','keys':'id','tolerance':'0.2'});self.assertEqual(r['metrics'][0]['value'],1)
 def test_text_comparison_exact(self):
  r=run({'source':'id,v\n1,Hello','target':'id,v\n1,hello','keys':'id'});self.assertEqual(r['metrics'][1]['value'],1)
 def test_negative_tolerance_rejected(self):
  p=self.sample();p['tolerance']='-1'
  with self.assertRaises(ValueError):run(p)

if __name__=='__main__':unittest.main()
