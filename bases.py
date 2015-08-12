#From http://stackoverflow.com/questions/2288482/how-can-i-work-with-base-5-numbers-in-python

import math

def ibase(n, radix=2, maxlen=None):
    r = []
    while n:
        n,p = divmod(n, radix)
        r.append('%d' % p)
        if maxlen and len(r) > maxlen:
            break
    r.reverse()
    return ''.join(r)

def fbase(n, radix=2, maxlen=8):
    r = []
    f = math.modf(n)[0]
    while f:
        f, p = math.modf(f*radix)
        r.append('%.0f' % p)
        if maxlen and len(r) > maxlen:
            break
    return ''.join(r)

def base(n, radix, maxfloat=8):
    if isinstance(n, float):
        return ibase(n, radix)+'.'+fbase(n, radix, maxfloat)
    elif isinstance(n, (str, unicode)):
        n,f = n.split('.')
        n = int(n, radix)
        f = int(f, radix)/float(radix**len(f))
        return n + f
    else:
        return ibase(n, radix)

if __name__=='__main__':
    pi = 3.14
    print 'pi:', pi, 'base 10'

    piBase3 = base(pi, 3)
    print 'pi:', piBase3, 'base 3'

    piFromBase3 = base(piBase3, 3)
    print 'pi:', piFromBase3, 'base 10 from base 3'

# From http://stackoverflow.com/questions/5110177/how-to-convert-floating-point-number-to-base-3-in-python

def convert_base(x, base=3, precision=None):
    length_of_int = int(math.log(x, base))
    iexps = range(length_of_int, -1, -1)
    if precision == None: fexps = itertools.count(-1, -1)
    else: fexps = range(-1, -int(precision + 1), -1)

    def cbgen(x, base, exponents):
        for e in exponents:
            d = int(x // (base ** e))
            x -= d * (base ** e)
            yield d
            if x == 0 and e < 0: break

    return cbgen(int(x), base, iexps), cbgen(x - int(x), base, fexps)
    
    
