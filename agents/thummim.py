import json, os, sys
from urim import load_key, ask_claude, load_memory, MODELS, DEFAULT_MODEL

AGENT_NAME = "THUMMIM"

CRITIC_SYSTEM = ('You are THUMMIM, the adversarial critic of PHOS. Your only '
'job is to attack the reasoning of URIM, the orchestrator. You are given URIM '
'prior findings. Find every weakness: claims stated with more confidence than '
'the data supports, cross-references to literature that may be wrong or '
'fabricated, model artifacts URIM treated as real, and conclusions that do not '
'follow from the data. Be specific and harsh but fair. If a finding is actually '
'sound, say so briefly and move on. Do not invent flaws that are not there. End '
'with a VERDICT: which findings survive scrutiny and which should be discarded.')

def frame_findings(mem):
    if not mem:
        return None
    recent = mem[-3:]
    lines = ['URIM FINDINGS TO CRITIQUE:']
    for m in recent:
        lines.append('\n[mode: ' + m.get('mode','?') + ']')
        lines.append(m.get('summary',''))
    return '\n'.join(lines)

def main():
    api_key = load_key()
    if not api_key:
        print('no API key found'); return
    mem = load_memory()
    findings = frame_findings(mem)
    if not findings:
        print('no URIM findings in memory to critique. run urim first.'); return
    print('\n  THUMMIM // adversarial critic')
    print('  models:', '  '.join(MODELS.keys()), '(enter = ' + DEFAULT_MODEL + ')')
    mk = input('\n  model > ').strip() or DEFAULT_MODEL
    if mk not in MODELS:
        print('  unknown model'); return
    print('\n  attacking URIM findings (' + mk + ')...\n')
    out = ask_claude(CRITIC_SYSTEM, findings, mk, api_key)
    print(out)

if __name__ == '__main__':
    main()
