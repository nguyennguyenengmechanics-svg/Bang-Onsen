"""Create a fresh video project without overwriting existing user files."""
import argparse,pathlib,shutil
parser=argparse.ArgumentParser();parser.add_argument('destination');args=parser.parse_args()
source=pathlib.Path(__file__).resolve().parents[1]/'assets/template'
dest=pathlib.Path(args.destination).expanduser().resolve()
if dest.exists():parser.error(f'Destination already exists: {dest}')
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.hyperframes'))
print(f'Created: {dest}\nEdit content.py, then run synthesize.py, mix_audio.py and generate.py. See references/workflow.md.')
