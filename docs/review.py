"""Deterministic review priorities derived from an existing studio result.

No network calls, generated answers, or automatic operational changes.
"""
import json
PROJECT = 'recon-lab'
NAME = 'Recon Lab'

def attach(request, result):
    lab = result['lab']
    items = []

    def add(key, severity, title, detail):
        items.append({'id': key, 'severity': severity, 'title': title, 'detail': detail})
    for status in ['missing', 'target_only', 'changed']:
        n = lab['counts'].get(status, 0)
        if n:
            add(status, 'high' if status != 'changed' else 'review', str(n) + ' ' + status.replace('_', ' ') + ' record(s)', 'Inspect the business-key exception ledger; changing a numeric tolerance cannot resolve absent keys.')
    for field, count in sorted(lab['field_counts'].items(), key=lambda x: (-x[1], x[0])):
        add('field-' + field, 'review', field + ': ' + str(count) + ' mismatching record(s)', 'Review units, precision, text normalization and business policy before widening tolerances.')
    add('scope', 'info', 'Compare keys before totals', 'Equal control totals can hide offsetting differences. Neither source nor target is modified.')
    items.sort(key=lambda x: {'high': 0, 'review': 1, 'info': 2}[x['severity']])
    review = {'version': '2.1.0', 'project': PROJECT, 'name': NAME, 'items': items, 'summary': {level: sum((x['severity'] == level for x in items)) for level in ['high', 'review', 'info']}, 'scope': 'Deterministic review aid from this experiment. Checklist completion does not certify correctness, safety, production readiness, or privacy.'}
    report = '# ' + NAME + ' — review handoff\n\n' + review['scope'] + '\n\n'
    for item in items:
        title = item['title'].replace('\n', ' ').replace('\r', ' ')
        detail = item['detail'].replace('\n', ' ').replace('\r', ' ')
        report += '- [ ] [' + item['severity'].upper() + '] ' + title + '\n  ' + detail + '\n'
    result['review'] = review
    result['artifacts'] += [{'name': 'review-handoff.md', 'content': report}, {'name': 'review-priorities.json', 'content': json.dumps(review, indent=2)}]
    return result
