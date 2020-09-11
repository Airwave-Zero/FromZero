import random

lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
num = '0123456789'
special = '!@#$%^&*()'

collection = [lower, upper, num, special]

allpasswords = []

#Creates a random password based off size
def password_generator(size):
    password = ""
    for x in range(size):
        randomNum = random.randint(0,3)
        charType = collection[randomNum]
        password += charType[random.randint(0, len(charType)-1)]

    #Prevent duplicate passwords by some miracle
    if password not in allpasswords:
        allpasswords.append(password)



if __name__ == "__main__":

    #Generate as many as you want
    for x in range(10000):
        password_generator(6)
        password_generator(7)
        password_generator(8)
        password_generator(9)
        password_generator(10)
        
    
    
        
        
