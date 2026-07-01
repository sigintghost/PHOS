import sys

def bar(current, total, label='', width=24):
    frac = current / total if total else 1
    filled = int(width * frac)
    b = '#' * filled + '-' * (width - filled)
    pct = frac * 100
    sys.stdout.write(f'\r  {label} [{b}] {pct:5.1f}%')
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write('\n')
