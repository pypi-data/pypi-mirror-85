class evaluate:
    def __init__(self):
        self.__num_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        self.__char_arr = ['+', '-', '*', '/', '^']
        self.__priority = ['^', '/', '*', '+', '-']
        self.__i_arr = []
        self.__c_arr = []

    def give(self, inp: str):
        self.__i_arr = []
        self.__c_arr = [] 
        ini_state = True
        for i in range(0, len(inp)):
            if i == 0:
                if (inp[i] in self.__num_arr) or inp[i] == '-' :
                    if ini_state:
                        ini = i
                        ini_state = False
            else:
                if inp[i] in self.__num_arr:
                    if ini_state:
                        ini = i
                        ini_state = False
                elif inp[i] in ['+','-','*','/','^']:
                    self.__i_arr.append(float(inp[ini:i]))
                    ini = 0
                    ini_state = True
                    self.__c_arr.append(inp[i])
        self.__i_arr.append(float(inp[ini:]))

    def __pri_find(self):
        for i in self.__priority:
            for j in range(0,len(self.__c_arr)):
                if i == self.__c_arr[j]:
                    return j

    def __calculator(self, first: int, second: int, operator: str):
        try:
            if operator == '+':
                return first + second
            elif operator == '-':
                return first - second
            elif operator == '*':
                return first * second
            elif operator == '/':
                return first / second
            elif operator == '^':
                return first ** second
        except:
            print('[ERROR] invalid operator')

    def __inserter(self, ind: int, to_insert: int):
        self.__i_arr[ind],self.__i_arr[ind+1] = "goingtoremove","goingtoremove"
        self.__c_arr[ind] = "goingtoremove"
        self.__i_arr.remove("goingtoremove")
        self.__i_arr.remove("goingtoremove")
        self.__c_arr.remove("goingtoremove")
        self.__i_arr.insert(ind, 0)
        self.__i_arr[ind] = to_insert

    def eval(self):
        cond = True
        while cond:
            if self.__c_arr == []:
                cond = False
                return self.__i_arr[0]
            self.__inserter(self.__pri_find(),self.__calculator(self.__i_arr[self.__pri_find()],self.__i_arr[self.__pri_find()+1],self.__c_arr[self.__pri_find()]))

class braces(evaluate):
    __raw_str = ''
    before = ['0','1','2','3','4','5','6','7','8','9',')']
    after = ['0','1','2','3','4','5','6','7','8','9','(']

    def __init__(self,inp: str):
        self.__raw_str = inp

    def checker(self):
        while True:
            open_pos, open_cnt, clos_pos, clos_cnt = 0,0,100000,0
            for i in range(0, len(self.__raw_str)):
                if self.__raw_str[i] == '(':
                    open_pos = i
                    open_cnt += 1
                elif self.__raw_str[i] == ')':
                    clos_pos = i
                    clos_cnt += 1
            if open_pos > clos_pos:
                self.__raw_str = '(' + self.__raw_str + ')'
            elif open_cnt == clos_cnt:
                break
            elif open_cnt == 0 and clos_cnt == 0:
                self.__raw_str = '(' + self.__raw_str + ')'
            elif open_cnt > clos_cnt:
                self.__raw_str += ')'
            elif clos_cnt > open_cnt:
                self.__raw_str = '(' + self.__raw_str

    def caller(self,send: str):
        obj = evaluate()
        obj.give(send)
        return obj.eval()

    def arith(self):
        while True:
            count = 0
            for i in self.__raw_str:
                if i == '(' or i == ')':
                    count += 1
            if count == 0:
                return self.caller(self.__raw_str)
            else:
                fin_found = False
                for i in range(0, len(self.__raw_str)):
                    if self.__raw_str[i] == '(':
                        ini = i
                        fin_found = True
                    elif self.__raw_str[i] == ')':
                        if fin_found:
                            fin = i
                            fin_found = False
            if ini-1 == -1 and fin+1 == len(self.__raw_str):
                self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]
            
            elif ini-1 == -1 :
                if self.__raw_str[fin+1] in self.after:
                    self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + '*' +self.__raw_str[fin+1:]
                else:
                    self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]
            
            elif fin+1 == len(self.__raw_str):
                if self.__raw_str[ini-1] in self.before:
                    self.__raw_str = self.__raw_str[:ini] + '*' + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]
                else:
                    self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]

            else:
                if (self.__raw_str[ini-1] in self.before) and (self.__raw_str[fin+1] in self.after):
                    self.__raw_str = self.__raw_str[:ini] + '*' + str(self.caller(self.__raw_str[ini+1:fin])) + '*' +self.__raw_str[fin+1:]
                elif self.__raw_str[ini-1] in self.before:
                    self.__raw_str = self.__raw_str[:ini] + '*' + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]
                elif self.__raw_str[fin+1] in self.after:
                    self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + '*' +self.__raw_str[fin+1:]
                else:
                    self.__raw_str = self.__raw_str[:ini] + str(self.caller(self.__raw_str[ini+1:fin])) + self.__raw_str[fin+1:]

def calc(input:str):
    reference = braces(input)
    reference.checker()
    return reference.arith()
