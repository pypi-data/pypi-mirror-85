def textMatrix(A):
    msg = '{:>16.5G}'
    txt = ""
    for Ai in A:
        for Aij in Ai:
            txt += msg.format(Aij)
        txt += "\n"
    return txt

def textMatrixWithTitle(A, title=""):
    txt = ""
    if bool(title):
        txt += '{}\n'.format(title)
    for Ai in A:
        txt += "\t"
        for Aij in Ai:
            txt += '{:>16.6G}'.format(Aij)
        txt += "\n"
    return txt

def textVector(A):
    txt = ""
    for Ai in A:
        txt += '{:>16.5G}'.format(Ai)
    txt += "\n"
    return txt

def textVectorWithIndex(A, label="", id=0):
    txt = '{}{:<}'.format(label, str(id))
    for Ai in A:
        txt += '{:>16.5G}'.format(Ai)
    txt += "\n"
    return txt

def textIndent(text, indent=0):
    prefix = " " * indent
    txt = ""
    textlines = text.splitlines()
    for textline in textlines:
        txt += prefix + textline + "\n"
    return txt

def textItem(key, value, width=12, precision=5):
    msgValue = "{:>" + str(width) + "}: "
    if type(value) is str:
        msgValue += "{}\n"
    elif type(value) is int:
        msgValue += "{:<" + str(width) + "d}\n"
    elif type(value) is float:
        msgValue += "{:<" + str(width) + "." + str(precision) + "G}\n"
    txt = msgValue.format(key, value)
    return txt
