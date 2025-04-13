# def ismatch(s: str, p: str):
#     print(p.index('*'))
    
# ismatch('aa', 'a*')

"""
aaa*gg.*d.f
h = f 
A = aa gg d f
B = a* .* . 


s = aaggyddfdfdfd

for i in l:
    for j in range(len(s))
    if i==s[:len(i)]: 
        l.del(i)
        s.del(i)


-------
    a = a
        => l = gg ddfd fd
        => s = aggyddfdfdfd
    
    gg = ag false
    
    
    
[a] a [gg] y [ddfd] [fd]
"""
occ = lambda str, occ: len(list(filter(lambda i: i==occ, str)))
cmp = lambda a, b:  b=='.*' or (b =='.' and len(a)==1) or (b[1]=='*' and (len(a) < 1 or occ(a, b[0]) == len(a)))


print(cmp('adadadfdsf', 'a*'))