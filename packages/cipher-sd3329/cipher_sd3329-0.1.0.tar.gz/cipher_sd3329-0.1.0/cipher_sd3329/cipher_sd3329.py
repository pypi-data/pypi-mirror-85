def cipher(text, shift, encrypt=True):
    """
    This function is a substitution cipher in which each letter in the plaintext is shifted a certain number of places

    Parameters
    ----------
    text : str
      A plaintext that you wish to encrypt or decrypt.
    shift : int
      The number of characters that you wish to shift the cipher alphabet.
    encrypt: boolean
       A boolean that controls between encryption and decryption. 
      

    Returns
    -------
    str
      The encoded or decoded text.

    Examples
    --------
    >>> text = 'DOG'
    >>> shift = 3
    >>> encrypt = True
    >>> cipher(text, shift, encrypt)
    'GRJ'

    >>> text = 'Gdkkn'
    >>> shift = -1
    >>> encrypt = False
    >>> cipher(text, shift, encrypt)
    'Hello'
    """  
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_text = ''
    for c in text:
        index = alphabet.find(c)
        if index == -1:
            new_text += c
        else:
            new_index = index + shift if encrypt == True else index - shift
            new_index %= len(alphabet)
            new_text += alphabet[new_index:new_index+1]
    return new_text
