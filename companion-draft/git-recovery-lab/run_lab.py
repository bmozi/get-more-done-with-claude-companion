"""Execute a local-only Git recovery rehearsal in a new disposable directory."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1] / 'builder' / 'maintenance-practice'
ROOT = Path(tempfile.mkdtemp(prefix='claude-book-git-recovery-'))
WORK = ROOT / 'working'
RECOVERY = ROOT / 'recovered'
EVIDENCE = ROOT / 'evidence'
EVIDENCE.mkdir()
shutil.copytree(SOURCE, WORK, ignore=shutil.ignore_patterns('__pycache__', '.git'))
(WORK / '.gitignore').write_text('__pycache__/\n*.pyc\n')
steps = []
env = os.environ.copy()
# Prevent caller Git routing variables from pointing this lab at another checkout.
for key in tuple(env):
    if key.startswith('GIT_'):
        del env[key]
env['PYTHONDONTWRITEBYTECODE'] = '1'


def run(label, command, cwd=WORK, expected=0):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=30)
    row = {'step':label, 'cwd':str(cwd), 'command':command, 'expected_exit':expected,
           'exit_code':result.returncode, 'stdout':result.stdout, 'stderr':result.stderr}
    steps.append(row)
    (EVIDENCE / 'steps.json').write_text(json.dumps(steps, indent=2)+'\n')
    if result.returncode != expected:
        raise RuntimeError(f'{label}: expected exit {expected}, observed {result.returncode}; inspect {EVIDENCE}')
    return result.stdout.strip()


# Explicit commit-local identity does not change Git account configuration.
COMMIT = ['git', '-c', 'user.name=Fictional Lab Author',
          '-c', 'user.email=lab@example.invalid', '-c', 'commit.gpgsign=false',
          '-c', 'core.hooksPath=/dev/null', 'commit']
source_hash = hashlib.sha256((SOURCE/'tracker.py').read_bytes()).hexdigest()
run('git-version', ['git', '--version'])
run('python-version', [sys.executable, '--version'])
run('initialize-only-the-copy', ['git', 'init', '-b', 'main'])
run('inspect-files', ['git', 'status', '--short'])
run('baseline-tests', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
run('stage-known-files', ['git', 'add', 'README.md', 'CLAUDE.md', '.gitignore', 'tracker.py', 'tests', 'data'])
run('commit-working-version', COMMIT + ['-m', 'Practice: preserve working due-date boundary'])
good = run('record-working-commit', ['git', 'rev-parse', 'HEAD'])
run('create-investigation-branch', ['git', 'switch', '-c', 'practice/boundary-bug'])
# This exact command is retained so a reader can reproduce the one-line mutation.
mutation = "from pathlib import Path; p=Path('tracker.py'); s=p.read_text(); assert s.count('due <= as_of') == 1; p.write_text(s.replace('due <= as_of', 'due < as_of'))"
run('introduce-deliberate-bug', [sys.executable, '-c', mutation])
run('inspect-deliberate-diff', ['git', 'diff', '--', 'tracker.py'])
run('observe-failing-tests', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], expected=1)
run('observe-incomplete-report', [sys.executable, '-B', 'tracker.py', 'data/maintenance.csv', '--as-of', '2026-10-17'])
run('stage-deliberate-bug', ['git', 'add', 'tracker.py'])
run('preserve-bug-for-investigation', COMMIT + ['-m', 'Practice only: preserve deliberately failing boundary'])
bad = run('record-bug-commit', ['git', 'rev-parse', 'HEAD'])
# Clone only the lab repository, with independent object files. Never the book repo.
run('copy-local-history', ['git', 'clone', '--no-hardlinks', '--no-checkout', str(WORK), str(RECOVERY)], cwd=ROOT)
run('remove-local-origin-label', ['git', 'remote', 'remove', 'origin'], cwd=RECOVERY)
run('select-known-working-commit', ['git', 'checkout', '--detach', good], cwd=RECOVERY)
run('verify-recovered-commit', ['git', 'rev-parse', 'HEAD'], cwd=RECOVERY)
run('recovered-tests', [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=RECOVERY)
run('recovered-report', [sys.executable, '-B', 'tracker.py', 'data/maintenance.csv', '--as-of', '2026-10-17'], cwd=RECOVERY)
run('confirm-investigation-preserved', ['git', 'rev-parse', 'HEAD'])
run('verify-no-working-remote', ['git', 'remote', '-v'])
run('verify-no-recovery-remote', ['git', 'remote', '-v'], cwd=RECOVERY)
assert hashlib.sha256((SOURCE/'tracker.py').read_bytes()).hexdigest() == source_hash
assert json.loads(next(r['stdout'] for r in steps if r['step']=='observe-incomplete-report'))['due'][0]['id'] == 'M01'
assert [r['id'] for r in json.loads(next(r['stdout'] for r in steps if r['step']=='recovered-report'))['due']] == ['M01','M02']
summary = {'evidence_kind':'executed local Git rehearsal; no network, model or remote backup',
           'scratch_root':str(ROOT), 'source_tracker_sha256_unchanged':source_hash,
           'known_working_commit':good,'preserved_bug_commit':bad,
           'steps_file':str(EVIDENCE/'steps.json'),
           'result':'baseline passes; deliberate mutation fails; separate recovery passes'}
(EVIDENCE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
