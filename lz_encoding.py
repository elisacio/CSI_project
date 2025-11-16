# Python program for LZ encoding
# code copied from https://www.inference.org.uk/mackay/python/compress/ 

import sys

verbose=0
class node:
    def __init__(self,substring,pointer):
        self.child = []
        self.substring = substring
        self.pointer = pointer
        if verbose:
            print(f"{pointer}  is pointer for  {substring}")
        pass

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): 
            return item
    return None

def ceillog( n ) : ## ceil( log_2 ( n ))   [Used by LZ.py]
    """
    >>> print ceillog(3), ceillog(4), ceillog(5)
    2 2 3
    """
    assert n>=1
    c = 0
    while 2**c<n :
        c += 1
    return c

def dec_to_bin( n , digits ):
    """ n is the number to convert to binary;  digits is the number of bits you want
    Always prints full number of digits
    >>> print dec_to_bin( 17 , 9)
    000010001
    >>> print dec_to_bin( 17 , 5)
    10001
    
    Will behead the standard binary number if requested
    >>> print dec_to_bin( 17 , 4)
    0001
    """
    if(n<0) :
        sys.stderr.write( "warning, negative n not expected\n")
        pass
    i=digits-1
    ans=""
    while i>=0 :
        b = (((1<<i)&n)>0) 
        i -= 1
        ans = ans + str(int(b))
        pass
    return ans

def bin_to_dec( clist , c , tot=0 ):
    """Implements ordinary binary to integer conversion if tot=0
    and HEADLESS binary to integer if tot=1
    clist is a list of bits; read c of them and turn into an integer.
    The bits that are read from the list are popped from it, i.e., deleted

    Regular binary to decimal 1001 is 9...
    >>> bin_to_dec(  ['1', '0', '0', '1']  ,  4  , 0 )
    9

    Headless binary to decimal [1] 1001 is 25...
    >>> bin_to_dec(  ['1', '0', '0', '1']  ,  4  , 1 )
    25
    """
    while (c>0) :
        assert ( len(clist) > 0 ) ## else we have been fed insufficient bits.
        tot = tot*2 + int(clist.pop(0))
        c-=1
        pass
    return tot

def encode ( c ): ## c is a list of characters (0/1) ; p is whether to print out prettily
    """
    Encode using Lempel-Ziv, as in MacKay (2003) Chapter 6. page 119
    
    >>> print encode(list("000000000000100000000000"))
    010100110010110001100
    """
    output =[]
    
    #initialize dictionary
    dic = [] 
    dic.append( node("",0) )
    
    while(len(c)>0): # point G
        substring = "";         latest = -1
        # read bits from c until we DON'T get a match with the dictionary
        while(len(c)>=0):
            ans = find( lambda p: p.substring == substring , dic )
            if ((ans == None) or (len(c)==0)):
                assert latest != -1 ## we should have gone round this loop once already
                # print out prevanswer's pointer and latest bit
                digits = ceillog ( len(dic) )
                output.append( dec_to_bin( prevanswer.pointer , digits ) + latest)
                # append new string to dictionary
                dic.append( node(substring, len(dic) ) )
                break # go back to G
            else:
                prevanswer = ans
                latest=c.pop(0)
                substring = substring+latest
            pass
        pass
    return "".join(output)

def printout( pointerstring, latest):
    return pointerstring+latest

def decode( c ):
    """
    >>> print decode(list("100011101100001000010"))
    1011010100010
    """
    output = [] 
    #initialize dictionary
    dic = [] 
    dic.append( node("",0) )
    while(len(c)>0):
        digits = ceillog ( len(dic) )
        pointer = bin_to_dec( c , digits )
        # find the dictionary entry with that pointer
        ans = find( lambda p: p.pointer == pointer , dic )
        substring = ans.substring
        output.append( substring )
        if (len(c)>0):
            latest=c.pop(0)
            output.append( latest )
            substring = substring+latest
            dic.append( node(substring, len(dic) ) )
            pass
        pass
    return "".join(output)
            
