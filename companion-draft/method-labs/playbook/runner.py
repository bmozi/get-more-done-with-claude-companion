"""Deterministic Chapter 42 teaching reference; prepares drafts only."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def classify(policy, request):
    for field in ('capacity', 'confirmed'):
        value = policy[field]
        if type(value) is not int or value < 0:
            raise ValueError(f'{field} must be a nonnegative integer')
    if policy['confirmed'] > policy['capacity']:
        raise ValueError('confirmed exceeds capacity; resolve policy snapshot')
    status = request['registration_status']
    if status not in ('confirmed', 'new', 'unknown'):
        raise ValueError('invalid registration_status')
    count = request.get('requested_count')
    if count is not None and (type(count) is not int or count <= 0):
        raise ValueError('requested_count must be a positive integer or null')
    for key in ('directions_only', 'access_requested', 'access_confirmed'):
        if type(request[key]) is not bool:
            raise ValueError(f'{key} must be boolean')
    remaining = policy['capacity'] - policy['confirmed']
    branches, missing, blockers, evidence, sentences = [], [], [], [], []

    def add(branch, refs, sentence):
        branches.append(branch)
        for ref in refs:
            if ref not in evidence:
                evidence.append(ref)
        sentences.append(sentence)

    if status == 'unknown':
        add('clarify_registration', ['B06'],
            'Please clarify your registration status for this workshop.')
        missing.append('current_registration_status')
        blockers.append('registration_unknown')
    if request['directions_only']:
        if status == 'confirmed':
            address = policy.get('approved_address')
            if isinstance(address, str) and address.strip():
                add('directions_draft', ['B06'],
                    f'The approved address is {address.strip()}.')
            else:
                add('missing_address', ['B06'],
                    'The approved address is missing; ask the coordinator for it.')
                missing.append('approved_address')
                blockers.append('address_unknown')
        elif status == 'new':
            add('registration_review', ['B06'],
                'This directions request needs current registration confirmation.')
            missing.append('current_registration_confirmation')
            blockers.append('registration_unconfirmed')
    else:
        # Count and access checks accumulate even when another branch blocks completion.
        if count is None:
            add('clarify_count', ['B03', 'B04'],
                'Please state how many places you are requesting.')
            missing.append('requested_count')
            blockers.append('count_unknown')
        elif count <= remaining:
            add('capacity_review', ['B01', 'B02', 'B03'],
                f'Your request for {count} places awaits a coordinator check of the current register.')
        else:
            add('capacity_conflict', ['B01', 'B02', 'B03', 'B04'],
                f'Your request for {count} places exceeds apparent availability and needs coordinator review. No partial allocation is proposed.')
            blockers.append('capacity_conflict')
        blockers.append('coordinator_register_check_required')
    if request['access_requested'] and not request['access_confirmed']:
        add('access_review', ['B05'],
            'The requested access arrangement also needs individual coordinator confirmation.')
        missing.append('coordinator_access_confirmation')
        blockers.append('access_unconfirmed')
    return {
        'request_id': request['id'],
        'snapshot_id': policy['snapshot_id'],
        'apparent_remaining': remaining,
        'branches': branches,
        'policy_references': evidence,
        'missing_facts': missing,
        'blocking_conditions': blockers,
        'allocated_places': 0,
        'confirmation_authorized': False,
        'sent': False,
        'status': 'review_required' if blockers else 'directions_draft_ready',
        'draft': ' '.join(sentences),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--policy', type=Path, default=HERE / 'policy.json')
    parser.add_argument('--cases', type=Path, default=HERE / 'cases.json')
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text())
        cases = json.loads(args.cases.read_text())
        # Validate all cases before publishing any result.
        results = [classify(policy, case) for case in cases]
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f'Input error: {error}\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
