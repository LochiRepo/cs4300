#% value calculator
def calcDisc(price, discount):

#Finds value removed by discount
    final = price - (price * discount / 100)
    return final
