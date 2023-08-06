
def cipher(text, shift, encrypt=True):
    """
    This function is used to encrypt the code. Each letter is replaced by a letter some fixed number of positions down the alphabet. 

    Parameters
    ----------
    text: the letters that are in the alphabet
    shift: the number of positions down the aphabet


    Returns
    -------
    The encrypted text based on the parameters

    Examples
    --------
    >>> from cipher_wl2722 import cipher_wl2722
    >>> cipher("Homeland", 2, encrypt=True)
    ["Jqogncpf"]
    >>> cipher("Jqogncpf", 2, encrypt=False)
    ["Homeland"]
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
