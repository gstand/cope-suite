from datetime import datetime

class DecodeError(Exception):
    '''The COPE² decoding engine ran into some sort of error that has been documented to occur with faulty input.'''
    def __init__(self, exception):
        self.exception = exception
        self.message = "The COPE² decoding engine experienced an error typically associated with an improper pagesize overrunning the input string index or an improper offset resulting in negative values being present.\nThe error was: " + exception.__class__.__name__ + ". Consult documentation for any remedies, if they exist. Otherwise, check your valules."
        super().__init__(self.message)

def decode(todecode: str, offset: int, pagesize: int) -> str:
    '''Decode the following COPE² hexstring with the provided offset and pagesize.
    Throws a DecodeError if something that has been documented to go wrong goes wrong.'''
    decoded = ''
    bad = False
    try:
        for i in range(0, len(todecode), pagesize):
            decoded += chr(int(todecode[i:i+pagesize], 16)-offset)
    except (IndexError, OverflowError, ValueError) as e:
        bad = True
        whatHappened = e

    exec("raise DecodeError(whatHappened)") if bad else None # if i try to do this without exec wrapping it it thinks i try to throw None
                                                             # i dont want to expand such a simple logic statement into a full if statement
    return decoded

def encode(toencode: str, offset: int, pagesize: int) -> [str, int, int, bool]:
    '''Encode the following string into a COPE² hexstring with the provided offset and pagesize.
    Returns the encoded string, the offset and page size if its automatically changed to ensure safety, and a bool to show if these changes have happened.'''
    safe = validateValues(toencode, offset, pagesize)
    tampered = False
    if not safe:
        vals = findLimits(data, pagesize)
        offset = vals[0] 
        pagesize = vals[1]
        tampered = True
    encoded = ''
    for i in toencode:
        encoded += hex(ord(i)+offset)[2:].zfill(pagesize)
    return [encoded, offset, pagesize, tampered]

def compile(toencode: str, offset: int, pagesize: int) -> str:
    '''Compile a provided Python script or pre-encoded (hopefully) encoded & executable hexstring into an executable script with the appropriate wrapper and debug information, if desired.'''
    try:
        int(toencode, 16)
        try:
            decode(toencode, offset, pagesize)
        except:
            raise ValueError("A hexstring was provided, but it is not a valid COPE² hexstring, or the offset or pagesize values are incorrect. Check your inputs.")
        compiled = toencode
    except ValueError:
        encoded = encode(toencode, offset, pagesize)
        compiled = encoded[0]
        offset = encoded[1] if encoded[3] else offset
        pagesize = encoded[2] if encoded[3] else pagesize
    dataline = f'z1,z2 = \'{compiled}\', \'\''
    interpreter = f'for i in range(0x0, len(z1), {hex(pagesize)}): z2 += chr(int(z1[i:i+{hex(pagesize)}], 0x10)-{hex(offset)}); exec(z2) if len(z2) == len(z1)/{hex(pagesize)} else None'
    return dataline + '\n' + interpreter

def validateValues(data: str, offset: int, pagesize: int) -> bool:
    '''Validate the provided offset and pagesize combination to ensure that it will not result in negative values being present in the encoded string.
    Returns a bool for whether the values are safe.'''
    limits = findLimits(data, pagesize)
    highestOffset = limits[0]
    lowestPagesize = limits[1]
    return offset <= highestOffset and pagesize >= lowestPagesize
    
def findLimits(data: str, presetPagesize: int = None) -> [int, int]:
    '''Find the highest allowable offset and lowest allowable page size values in a string. Set presetPagesize to a value to force the offset calculations to that page size. If you specify a page size that is too small, the routine will override it.
    Returns a [int, int], values respective.
    This works by calculating the highest ordinal value in the string, finding the lowest page size that can hold that value (unless predefined), finding the integer ceiling of that page size, and subtracting the ceiling from the ordinal.'''
    highestOffset = 0
    highestPoint = 0
    lowestPagesize = 0

    for char in data:
        ref = ord(char)
        highestPoint = ref if ref > highestOffset else highestOffset

    lowestPagesize = len(hex(highestPoint)[2:])
    lowestPagesize = presetPagesize if presetPagesize != None and presetPagesize >= lowestPagesize else lowestPagesize
    ceil = int(hex(0)[2:].zfill(lowestPagesize).replace('0','f'), 16)
    highestOffset = ceil-highestPoint

    return [highestOffset, lowestPagesize]

