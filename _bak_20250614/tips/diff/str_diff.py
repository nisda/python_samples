import difflib

s1 = ['Python', 'Java', 'C++', 'PHP']
s2 = ['Python', 'JavaScript', 'C', 'PHP']

print()
print("===========================================")
print("ndiff")
print("===========================================")
res = difflib.ndiff(s1, s2)
print('\n'.join(res))

print()
print("===========================================")
print("context_diff")
print("===========================================")
res = difflib.context_diff(s1, s2)
print('\n'.join(res))

print()
print("===========================================")
print("unified_diff")
print("===========================================")
res = difflib.unified_diff(s1, s2)
print('\n'.join(res))

