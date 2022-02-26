# VIN utils

VIN_PREFIX_SE_WEATHER = 'JTMAB3FVXND'
VIN_PREFIX_XSE_PREMIUM = 'JTMFB3FVXND'

def generate_vins(prefix, start, end):
    """Generate VINs in specified range"""
    result = []
    for postfix in range(start, end):
        result.append(fix_check_digit(f'{prefix}{postfix:06d}'))
    return result

def fix_check_digit(vin):
    """Fix check digit"""
    positional_weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    letter_key = dict(A=1,B=2,C=3,D=4,E=5,F=6,G=7,H=8,J=1,K=2,L=3,M=4,N=5,P=7,R=9,S=2,T=3,U=4,V=5,W=6,X=7,Y=8,Z=9)

    pos = csum = 0
    for char in vin:
        value = int(letter_key[char]) if char in letter_key else int(char)
        weight = positional_weights[pos]
        csum += (value * weight)
        pos += 1

    check_digit = int(csum) % 11

    if check_digit == 10:
        check_digit = 'X'

    return vin[:8] + str(check_digit) + vin[9:]
