from random import choice
from random import choices
import csv


class Board:
    def __init__(self,list=[" "," "," "," "," "," "," "," "," "]):
        if len(list)!=9:
            raise ValueError("List lenght must be 9")
        self.list=list


    def __str__(self):
        return  f'''
     {self.list[0]} | {self.list[1]} | {self.list[2]}
    ------------
     {self.list[3]} | {self.list[4]} | {self.list[5]}
    ------------
     {self.list[6]} | {self.list[7]} | {self.list[8]}
'''

    def update(self,info):
        if len(info)!=9:
            raise ValueError("Argument lenght must be 9")
        if type(info)==str:
            auxiliar_list=[]
            for i in info:
                auxiliar_list.append(i)
            self.list=auxiliar_list
        elif type(info)==list:
            self.list=info.copy()
        else:
            raise TypeError("Argument is not a list or string")


    def win(self):
        if self.list[0]==self.list[1]==self.list[2]!=" " or self.list[3]==self.list[4]==self.list[5]!=" " or self.list[6]==self.list[7]==self.list[8]!=" " or self.list[0]==self.list[3]==self.list[6]!=" " or self.list[1]==self.list[4]==self.list[7]!=" " or self.list[2]==self.list[5]==self.list[8]!=" " or self.list[0]==self.list[4]==self.list[8]!=" " or self.list[6]==self.list[4]==self.list[2]!=" ":
            return True


    def reset(self):
        self.list=[" "," "," "," "," "," "," "," "," "]


    def rotate_90(self):
        auxiliar_list=[" "," "," "," "," "," "," "," "," "]
        for position in range(9):
            new=(((position+1)*3)%10)-1
            auxiliar_list[new]=self.list[position]
        self.list=auxiliar_list.copy()


    def flip_h(self):
        auxiliar_list=[" "," "," "," "," "," "," "," "," "]
        for position in range(9):
            if 0<=position<=2:
                a=2
            elif 3<=position<=5:
                a=8
            elif 6<=position<=8:
                a=14
            new=a-position
            auxiliar_list[new]=self.list[position]
        self.list=auxiliar_list.copy()


    def copy(self):
        auxiliar_list=self.list.copy()
        return Board(auxiliar_list)


    def string(self):
        string=""
        for i in self.list:
            string+=i
        return string




def get_options_dic(file):
    options={}
    try:
        with open (file,newline="") as optionsfile:
            optionsfilereader=csv.reader(optionsfile,delimiter=",")
            try:
                for i in optionsfilereader:
                    options[i[0]]=i[1:]
                return options
            except IndexError:
                pass
    except FileNotFoundError:
        return options


def get_weights_dic(file):
    weights={}
    try:
        with open (file,newline="") as weightsfile:
            weightsfilereader=csv.reader(weightsfile,delimiter=",")
            try:
                for i in weightsfilereader:
                    changetoint=[]
                    for p in i[1:]:
                        changetoint.append(int(p))
                    weights[i[0]]=changetoint
                return weights
            except IndexError:
                pass
    except FileNotFoundError:
        return weights


def save_dic(dictionary,file):
    auxiliary_list=[]
    with open (file,"w",newline="") as dictionaryfile:
        filewriter=csv.writer(dictionaryfile,delimiter=",")
        for i in dictionary:
            auxiliary_list.append(i)
            for j in dictionary[i]:
                auxiliary_list.append(j)
            filewriter.writerow(auxiliary_list)
            auxiliary_list.clear()


def list_to_str(list:list):
    string=""
    for i in list:
        string+=i
    return string


def game(options,weights,opponent,repetitions=1):
    for repetition in range(repetitions):
        board=Board()
        decisions=[]
        for turn in range(5):
            #rotate and flip the board to reduce data in options
            string=board.string()
            count=0
            while string not in options:
                count+=1
                board.rotate_90()
                string=board.string()
                if count==4:
                    break
            if string not in options:
                board.flip_h()
                string=board.string()
            while string not in options:
                count+=1
                board.rotate_90()
                string=board.string()
                if count==8:
                    break

            #saving current board and options in the options and weights Dictionaties
            if string not in options:
                string=board.string()
                options_values=[]
                for i in range(9):
                    momentary_list=board.list.copy()
                    if board.list[i]==" ":
                        momentary_list[i]="X"
                        options_values.append(list_to_str(momentary_list))
                options[string]=options_values

                weights_values=[]
                for _ in range(len(options[string])):
                    weights_values.append(6)
                weights[string]=weights_values

            #Self learning machine play
            try:
                machine1=choices(options[string],weights[string])
                board.update(machine1[0])
                string_to_save=board.string()
                #rotate and flipe the board to set back to original
                if count==5:
                    board.flip_h()
                    board.rotate_90()
                elif count==7:
                    board.flip_h()
                    for _ in range(3):
                        board.rotate_90()
                else:
                    if count>=4:
                        board.flip_h()
                    for _ in range(8-count):
                        board.rotate_90()
            except ValueError:
                #No options to play, -1 to decisions weights
                if opponent=="human":
                    print(board)
                    print("        The Machine quits the game,  You Won!")
                for key,value in decisions:
                    index=options[key].index(value)
                    if weights[key][index]>0:
                        weights[key][index]-=1
                break

            decisions.append([string,string_to_save])   #Saving the decisions made in current game

            if opponent=="human":
                print(board)

            if board.win():
                # +3 to decisions weights
                if opponent=="human":
                    print("        The Machine has won!")
                for key,value in decisions:
                    index=options[key].index(value)
                    weights[key][index]+=3
                break

            if turn==4:
                # +1 to decisiona weights
                if opponent=="human":
                    print("        Its a tie!")
                for key,value in decisions:
                    index=options[key].index(value)
                    weights[key][index]+=1
                break
            else:
                if opponent=="human":
                    while True:
                        try:
                            human=int(input("        Choose a position: (numbers from 1 to 9) "))-1
                            if board.list[human]==" ":
                                board.list[human]="O"
                                break
                        except ValueError:
                            continue
                elif opponent=="machine":
                    values2=[]
                    for i in range(9):
                        momentary_list=board.list.copy()
                        if board.list[i]==" ":
                            momentary_list[i]="O"
                            values2.append(list_to_str(momentary_list))
                    machine2=choice(values2)
                    board.update(machine2)

            if board.win():
                # -1 to decisions weights
                if opponent=="human":
                    print(board)
                    print("        You Won!")
                for key,value in decisions:
                    index=options[key].index(value)
                    if weights[key][index]>0:
                        weights[key][index]-=1
                break


def main():
    print("In this program, the machine learns to play Tic Tac Toe through repetition.")
    while True:
        a=input(f'''
        Select the option you want:
        1. Machine self learn
        2. Play against the Machine
        3. Leave the program
        > ''' )
        if a=="1":
            options=get_options_dic("boards_data.csv")
            weights=get_weights_dic("weights_data.csv")
            repetitions=int(input('''
        How many games?
        > '''))
            game(options,weights,"machine",repetitions)
            save_dic(options,"boards_data.csv")
            save_dic(weights,"weights_data.csv")
            print(f'''
        The machine has played {repetitions} games and learned a little more
        ''')
        elif a=="2":
            options=get_options_dic("boards_data.csv")
            weights=get_weights_dic("weights_data.csv")
            game(options,weights,"human",1)
            save_dic(options,"boards_data.csv")
            save_dic(weights,"weights_data.csv")
            print('''
        Thanks for playing
        ''')
        elif a=="3":
            print('''
        Good bye!
        ''')
            break
        else:
            print('''
        Only options 1, 2, or 3''')


if __name__ == "__main__":
    main()