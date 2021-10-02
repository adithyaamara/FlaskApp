import random
import string

class pwd_gen:
    def __init__(self,p_length:int):
        self._p_length = p_length
    def genarate(self):
        #-------password generator-------#
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        all = lower + upper + num
        length = self._p_length
        temp = random.sample(all,length)
        randompass = "".join(temp)
        return randompass