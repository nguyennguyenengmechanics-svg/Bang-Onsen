"""Download the approved voice, verify its published checksum, and extract safely."""
import argparse,hashlib,pathlib,subprocess,tarfile
URL='https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-vi_VN-vais1000-medium.tar.bz2'
SHA='fa1367710767d36ed5cf13b4a449e20c35ffd12791c2e47c2e64142bfa55551a'
NAME='vits-piper-vi_VN-vais1000-medium'
p=argparse.ArgumentParser();p.add_argument('cache_dir');args=p.parse_args()
cache=pathlib.Path(args.cache_dir).expanduser().resolve();cache.mkdir(parents=True,exist_ok=True)
archive=cache/(NAME+'.tar.bz2')
if not archive.exists():
 temporary=cache/(NAME+'.download')
 subprocess.run(['curl','--fail','--location','--show-error','--output',str(temporary),URL],check=True)
 if hashlib.sha256(temporary.read_bytes()).hexdigest()!=SHA:
  temporary.unlink();raise SystemExit('Voice checksum mismatch; stopped without using the download.')
 temporary.rename(archive)
if hashlib.sha256(archive.read_bytes()).hexdigest()!=SHA:raise SystemExit('Cached archive checksum mismatch; stopped.')
model=cache/NAME
if not model.exists():
 with tarfile.open(archive,'r:bz2') as tf:tf.extractall(cache,filter='data')
for file in ['vi_VN-vais1000-medium.onnx','tokens.txt','espeak-ng-data','MODEL_CARD']:
 if not (model/file).exists():raise SystemExit(f'Incomplete model: {file}')
print(model)
