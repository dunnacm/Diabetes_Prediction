"""Run from any working directory; no participant rows are exported."""
from pathlib import Path
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from diabetes_workflow import run_analysis

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=ROOT/'data/raw/NHANES_age_prediction.csv')
    parser.add_argument('--output',type=Path,default=ROOT/'reports/generated/reproduction.json')
    parser.add_argument('--expected-sha256',help='Fail before fitting if the supplied file differs.')
    args=parser.parse_args()
    result=run_analysis(args.data,expected_sha256=args.expected_sha256)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(f"Saved aggregate results to {args.output}")
    print(f"Selected from training CV: {result['selected_family']}")
    print('Retrospective holdout matrix:',result['holdout_selected']['confusion_matrix'])
if __name__=='__main__':main()
