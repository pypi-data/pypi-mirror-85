import f2format

a = 'test'
print(f2format.convert("f'{a:=}'"))
print(f'{a:=}')
print(eval(f2format.convert("f'{a:=}'")))
