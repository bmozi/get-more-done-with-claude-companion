"""Read selected local inventory. No network, install, settings changes or serial IDs."""
import argparse
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def command(args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=10)
        return {'command': args, 'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}
    except (OSError, subprocess.TimeoutExpired) as error:
        return {'command': args, 'error': str(error)}


def collect():
    disk = shutil.disk_usage(Path.cwd())
    result = {'observed_at_utc': datetime.now(timezone.utc).isoformat(),
              'evidence': 'current host inventory, not the planned workstation unless separately identified',
              'system': platform.system(), 'architecture': platform.machine(),
              'python': platform.python_version(),
              'workspace_volume_bytes': {'total': disk.total, 'free': disk.free},
              'ollama_executable_present': shutil.which('ollama') is not None,
              'model_inference_executed': False}
    if platform.system() == 'Darwin':
        result['macos'] = command(['sw_vers', '-productVersion'])
        result['memory_bytes'] = command(['sysctl', '-n', 'hw.memsize'])
        result['chip'] = command(['sysctl', '-n', 'machdep.cpu.brand_string'])
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--out', required=True)
    a=p.parse_args()
    with Path(a.out).open('x') as f:
        json.dump(collect(), f, indent=2); f.write('\n')
    print('Wrote current-host inventory; no model run or target-machine claim.')
