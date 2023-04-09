import os

for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'w') as f:
            f.write('')