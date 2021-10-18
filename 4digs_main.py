import random
import operator
import pandas as pd
import os

# operator lists
ops = [operator.add, operator.sub, operator.truediv, operator.mul]
ops_str = [" + ", " - ", "/", " x "]

def trimDict(d):

    #for timming duplicate formula results in each iteration
    new_d = {}
    temp = []
    for key, val in d.items():
        if val not in temp:
            temp.append(val)
            new_d[key] = int(val)
    return new_d

class FormChallenge:

    def __init__(self, no_digs, int_range, digs=None):
        self.no_digs = no_digs
        self.int_range = int_range
        self.digs = digs
        self.running_dict = {}
        self.form_dict = {}
        self.ints = list(range(self.int_range + 1))

    def getRanDigs(self):
        self.digs = []
        while len(self.digs) < self.no_digs:
            integer = random.randint(1, 9)
            if integer not in self.digs:
                self.digs.append(integer)
                self.running_dict[integer] = integer
        return self.running_dict

    def getForms(self, dictionary):

        self.running_dict = dictionary
        running_list = list(dictionary.values())
        running_keys = list(dictionary.keys())

        for operations in range(4):
            for k in range(len(self.digs)):
                if self.digs[k] in self.ints and self.digs[k] not in self.form_dict.values():
                    self.form_dict[str(self.digs[k])] = self.digs[k]
                for j in range(len(running_keys)):
                    result = ops[operations](running_list[j], self.digs[k])
                    self.running_dict[
                        "(" + str(running_keys[j]) + ops_str[operations] + str(self.digs[k]) + ")"] = result
                    if result in self.ints and result not in self.form_dict.values():
                        self.form_dict[
                            "(" + str(running_keys[j]) + ops_str[operations] + str(self.digs[k]) + ")"] = result
                    if len(self.form_dict) >= self.int_range+1:
                        break

        self.running_dict = trimDict(self.running_dict)
        return self.running_dict

    def getFormDict(self):
        temp_0 = dict(sorted(self.form_dict.items(), key=lambda item: item[1]))
        temp = dict([(int(val), key) for key, val in temp_0.items()])
        df = pd.DataFrame.from_dict(temp, orient='index', columns=[self.getDigsStr()])
        return df

    def getDigsStr(self):
        digits = ""
        for i in self.digs:
            digits = digits + str(i)
        return digits

def Run(no_digs, first_x_integers, digits=None):

    temp_dict = {}
    if digits:
        for dig in digits:
             temp_dict[dig] = dig
        x = FormChallenge(no_digs, first_x_integers, digits)
        x.running_dict = temp_dict
    else:
        x = FormChallenge(no_digs, first_x_integers, digits)
        temp_dict = (x.getRanDigs())

    i = x.getForms(temp_dict)

    count = 0

    while True:

        output = x.getFormDict()
        count += 1

        if len(output.index) >= first_x_integers+1:

            print("operators used:", count)
            print("digits used:", x.digs)

            if os.path.getsize("output.csv") < 10:
                output.to_csv("output.csv")
            else:
                df = pd.read_csv("output.csv")
                df[x.getDigsStr()] = output
                df.to_csv("output.csv", index=False)
            break
        else:
            i = x.getForms(i)

def main():
    f = open("output.csv", "w")
    f.truncate()
    f.close()
    
    int_range = int(input("What number would you like to go up to? "))

    no_digs = 0
    while True:
        if no_digs > 0 and no_digs < 10:
            break
        else:
            no_digs = int(input("Enter number of digits(1-9) "))

    while True:
        
        j = input("Would you like to pick your digits?(y/n) ")
        if j == "y" or j == "Y":
            digs = []
            y = 1
            while y <= no_digs:
                d = int(input("Enter digit "+str(y)+" "))
                digs.append(d)
                y += 1
            Run(no_digs,int_range, digs)
            break
        elif j == "n" or j == "N":
            check = True
            Run(no_digs, int_range)
            break

main()



