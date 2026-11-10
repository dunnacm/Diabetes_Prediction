import unittest
from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from diabetes_workflow import prepare_data, make_pipeline, wilson_interval, run_analysis

def sample_frame():
    n=30
    return pd.DataFrame({'SEQN':range(n),'age_group':['Adult']*n,'RIDAGEYR':np.arange(n)+20,
        'RIAGENDR':[1,2]*15,'PAQ605':[1,2]*15,'BMXBMI':np.arange(n)/10+20,
        'LBXGLU':np.arange(n)+70,'DIQ010':[1,2]*15,'LBXGLT':np.arange(n)+80,'LBXIN':[5]*n})

class WorkflowTests(unittest.TestCase):
    def test_checksum_fails_before_loading_or_fitting(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'input.csv'
            path.write_text('invalid input',encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'SHA-256'):
                run_analysis(path,expected_sha256='0'*64)
    def test_schema_and_duplicate_id_fail(self):
        f=sample_frame()
        with self.assertRaisesRegex(ValueError,'Missing required'):prepare_data(f.drop(columns='DIQ010'))
        f.loc[1,'SEQN']=0
        with self.assertRaisesRegex(ValueError,'unique'):prepare_data(f)
    def test_unknown_codes_not_guessed(self):
        f=sample_frame();f.loc[0,'PAQ605']=5
        with self.assertRaisesRegex(ValueError,'Unexpected PAQ605'):prepare_data(f)
    def test_target_exclusion_and_refused_separate(self):
        f=sample_frame();f.loc[0,'PAQ605']=7;f.loc[1,'DIQ010']=9;f.loc[2,'DIQ010']=3
        X,y,q=prepare_data(f)
        self.assertTrue(pd.isna(X.loc[0,'PAQ605']))
        self.assertNotIn(1,y.index)
        self.assertEqual(y.loc[2],1)
        self.assertEqual(q['excluded_target_rows'],1)
        self.assertNotIn('DIQ010',X)
        self.assertNotIn('SEQN',X)
    def test_fit_imputation_cannot_see_test_extreme(self):
        X,y,_=prepare_data(sample_frame())
        p=make_pipeline(LogisticRegression(solver='liblinear'))
        p.fit(X.iloc[:24],y.iloc[:24])
        median=p.named_steps['prepare'].named_transformers_['numeric'].named_steps['impute'].statistics_[0]
        self.assertEqual(median,np.median(X.iloc[:24].RIDAGEYR))
        test=X.iloc[24:].copy();test['RIDAGEYR']=1e9;p.predict(test)
        self.assertEqual(median,p.named_steps['prepare'].named_transformers_['numeric'].named_steps['impute'].statistics_[0])
    def test_smotenc_keeps_valid_categories(self):
        X,y,_=prepare_data(sample_frame());y.iloc[:8]=0
        p=make_pipeline(LogisticRegression(solver='liblinear'),resample=True)
        prepared=p.named_steps['prepare'].fit_transform(X,y)
        resampled,_=p.named_steps['resample'].fit_resample(prepared,y)
        for col in [4,5]:self.assertTrue(set(resampled[:,col]) <= {1.0,2.0})
        self.assertGreater(len(resampled),len(X))
    def test_wilson_known_case(self):
        lo,hi=wilson_interval(10,16)
        self.assertAlmostEqual(lo,0.3864104,places=6)
        self.assertAlmostEqual(hi,0.8151877,places=6)
        self.assertIsNone(wilson_interval(0,0))

if __name__=='__main__':unittest.main()
