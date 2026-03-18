#!/usr/bin/env python3
import os

# Path to the app.py file
app_path = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')

# Read the file
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count original occurrences
original_count = content.count('cursor(dictionary=True)')

# Replace all occurrences
content = content.replace('cursor(dictionary=True)', 'cursor()')

# Count remaining occurrences
remaining_count = content.count('cursor(dictionary=True)')

# Write back to file
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Replaced {original_count} occurrences of 'cursor(dictionary=True)' with 'cursor()'")
print(f"✓ Remaining occurrences: {remaining_count}")