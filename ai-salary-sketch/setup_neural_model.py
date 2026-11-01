"""Fetch the exact official model used for the user-approved neural sample."""
from pathlib import Path
import urllib.request,hashlib,tarfile
P=Path(__file__).parent;cache=P/'neural-models';cache.mkdir(exist_ok=True)
url='https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-vi_VN-vais1000-medium.tar.bz2'
archive=cache/'vais1000.tar.bz2';expected='fa1367710767d36ed5cf13b4a449e20c35ffd12791c2e47c2e64142bfa55551a'
if not archive.exists():
 with urllib.request.urlopen(url,timeout=120) as r,archive.open('wb') as f:
  while chunk:=r.read(1024*1024):f.write(chunk)
assert hashlib.sha256(archive.read_bytes()).hexdigest()==expected,'Model archive checksum differs from the approved sample; investigate the publisher release.'
with tarfile.open(archive) as t:t.extractall(cache,filter='data')
model=cache/'vits-piper-vi_VN-vais1000-medium/vi_VN-vais1000-medium.onnx'
assert hashlib.sha256(model.read_bytes()).hexdigest()=='df1512ef3265609f147ae23726b8c8867c6d28e60acb9ffca3545e11783b809f'
print('Approved Vietnamese neural model is ready.')
