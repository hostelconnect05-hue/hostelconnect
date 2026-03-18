#!/usr/bin/env python
import os

filepath = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original_count = content.count('cursor(dictionary=True)')
content = content.replace('cursor(dictionary=True)', 'cursor()')
new_count = content.count('cursor(dictionary=True)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Replaced {original_count} occurrences of cursor(dictionary=True)")
print(f"✓ Remaining occurrences: {new_count}")
