import os
from zipfile import ZipFile

l = os.listdir('main')

z = ZipFile('main/o.zip', 'w')
for ll in l:
    z.write(f'main/{ll}', arcname=ll)

print(z.filename)
