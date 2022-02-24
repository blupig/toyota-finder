# VIN utils

VIN_PREFIX_SE_WEATHER = 'JTMAB3FVXND'
VIN_PREFIX_XSE_PREMIUM = 'JTMFB3FVXND'

def generateVINs(prefix, start, end):
    result = []
    for postfix in range(start, end):
        result.append(fixCheckDigit(f'{prefix}{postfix:06d}'))
    return result

def fixCheckDigit(vin):
    POSITIONAL_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    LETTER_KEY = dict(A=1,B=2,C=3,D=4,E=5,F=6,G=7,H=8,J=1,K=2,L=3,M=4,N=5,P=7,R=9,S=2,T=3,U=4,V=5,W=6,X=7,Y=8,Z=9)

    pos = sum = 0
    for char in vin:
        value = int(LETTER_KEY[char]) if char in LETTER_KEY else int(char)
        weight = POSITIONAL_WEIGHTS[pos]
        sum += (value * weight)
        pos += 1

    check_digit = int(sum) % 11

    if check_digit == 10:
        check_digit = 'X'

    return vin[:8] + str(check_digit) + vin[9:]
