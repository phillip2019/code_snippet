#!/usr/bin/python
# -*- coding: utf-8 -*-

def bracket(s):
    stk = []
    for c in s:
        if c == '(':
            stk.append(c)
        elif c == ')':
            stk.pop()
    return False if stk else True

if __name__ == "__main__":
    tests = [ ("()","YES"),
            ("(()","NO"),
            (")(","NO"),
            ("(A(((B)","NO"),
            ("(a)(b)","YES"),
            ("aa()","YES"),
            ("((acs))","YES"),]
    for t in tests:
        s, r = t[0], t[1]
        try:
            ret = bracket(s)
        except Exception as _:
            ret = "NO"
        print(r)
        # if  str(ret) == r.lower():
        #     print('YES')
        # else:
        #     print('NO')