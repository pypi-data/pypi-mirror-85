# define a function and apply it to each element of an attribute
def getNat(s):
    parts = s.split(' ')
    return parts[0]

data['Nat'] = data['Nat'].apply(getNat)