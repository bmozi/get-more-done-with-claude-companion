"""Copy the book's practice skill into a fresh temporary project; no model call."""
from pathlib import Path
import hashlib,json,shutil,tempfile
SOURCE=Path(__file__).resolve().parent/'meeting-record'

def stage():
    project=Path(tempfile.mkdtemp(prefix='claude-book-skill-'))
    target=project/'.claude/skills/meeting-record'
    shutil.copytree(SOURCE,target)
    hashes={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file()}
    for name,digest in hashes.items():
        if hashlib.sha256((target/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Copied content differs: '+name)
    return {'project':str(project),'package':str(target),'copied_files_sha256':hashes,
            'evidence':'Verified local copy and hashes only; Claude discovery/invocation not exercised.'}

if __name__=='__main__':
    print(json.dumps(stage(),indent=2))
