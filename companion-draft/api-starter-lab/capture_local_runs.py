"""Print raw local CLI evidence; caller chooses a NEW output file."""
import json
from pathlib import Path
import platform
import subprocess
import sys
import threading
from fixture_server import FIXTURES, make_server

server = make_server()
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
records = []
try:
    for name, case in FIXTURES.items():
        command = [sys.executable, str(Path(__file__).with_name('app.py')),
                   '--endpoint', f'http://127.0.0.1:{server.server_port}/draft',
                   '--case', name, '--note', case['note']]
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        records.append({'case':name, 'command':command, 'exit_code':result.returncode,
                        'stdout':result.stdout, 'stderr':result.stderr})
finally:
    server.shutdown()
    server.server_close()
    thread.join()
print(json.dumps({'evidence_kind':'local fixed HTTP fixtures; no model or paid call',
                  'python':platform.python_version(), 'runs':records},indent=2))
