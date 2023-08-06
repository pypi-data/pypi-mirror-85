import pandas as pd
import os

args=[]
rep=[]

# Error Handling Block
class NotFound(FileNotFoundError):
    def __init__(self, message="No such file exists in specified Directory!"):
        self.msg=message
        print(message)
        exit(0)

class FileType_Error(Exception):
    def __init__(self, message="File Format Unacceptable!"):
        self.msg=message
        print(message)
        exit(0)

class Less_Columns(Exception):
    def __init__(self, message="No. of columns are less than 3 in Input .csv file!"):
        self.msg=message
        print(message)
        exit(0)

def topsis(Input=None,Weights=None,Impacts=None,Output=None):
    args=[Input,Weights,Impacts,Output]

    if args[0]==None:
        print("Enter the Input (.csv) file name as First Argument in topsis()")
        exit(0)
    elif args[1] == None:
        print("Enter the Weights of Columns as Second Argument in topsis()")
        exit(0)
    elif args[2] == None:
        print("Enter the Impacts of Columns as Third Argument in topsis()")
        exit(0)
    elif args[3] == None:
        print("Enter the Output (.csv) file name as Fourth Argument in topsis()")
        exit(0)

    if args[0][-4:]!='.csv':
        print("For Input File name:")
        raise FileType_Error()
    elif os.path.isfile(args[0])==False:
        print("For Input File name:")
        raise NotFound()
    else:
        df_temp = pd.read_csv(str(args[0]))
        if len(df_temp.columns)<3:
                raise Less_Columns()
    df=pd.read_csv(str(args[0]))
    for col in df.columns[1:]:
        for i in df[col]:
            try:
                float(i)
            except ValueError as Non_Numeric:
                print("Column values are Non-Numeric!")
                exit(0)

    weights=args[1]
    for i in weights:
        if i.__str__().isnumeric() or i==",":
            continue
        else:
            print("Enter Weights Correctly. Use Numeric Values separated by ','.")
            exit(0)
    if weights[-1:]==",":
        print("Do Not End Weights in a ','!")
        exit(0)

    impacts=args[2]
    for i in impacts:
        if i=='+' or i=='-' or i==",":
            continue
        else:
            print("Enter Impacts Correctly. Use either '+' or '-' separated by ','.")
            exit(0)
    if impacts[-1:]==",":
        print("Do Not end Impacts in a ','!")
        exit(0)

    weights=weights.split(",")
    weights=[float(i) for i in weights]

    impacts=impacts.split(",")

    if len(weights)!=len(df_temp.columns[1:]) or len(impacts)!=len(df_temp.columns[1:]):
        print("Enter " + str(len(df_temp.columns[1:])) + " Weights/Impacts!")

    res_file=args[3]
    if res_file[-4:]!='.csv':
        print("For Output File name:")
        raise FileType_Error()

    #Code Block
    v_pos=[]
    v_neg=[]
    s_pos=[]
    s_neg=[]
    performance=[]

    s=0
    for i in weights:
        s+=i
    for i in range(len(weights)):
        weights[i]=weights[i]/s

    j=0
    for col in df_temp.columns[1:]:
        sq_sum = 0
        curr_col = []

        for x in df_temp[col]:
            sq_sum=sq_sum+pow(x,2)
            sq_sum=pow(sq_sum,0.5)

        for i in range(len(df_temp[col])):
            df_temp.at[i,col]=(df_temp[col][i]/sq_sum)*weights[j]
            curr_col.append(df_temp[col][i])

        if impacts[j]=='+':
            v_pos.append(max(curr_col))
            v_neg.append(min(curr_col))
        elif impacts[j]=='-':
            v_pos.append(min(curr_col))
            v_neg.append(max(curr_col))

        j=j+1

    for i in range(len(df_temp.index)):
        sum_pos=0
        sum_neg=0
        j=0
        for col in df_temp.columns[1:]:
            sum_pos=sum_pos+pow((df_temp[col][i]-v_pos[j]),2)
            sum_neg=sum_neg+pow((df_temp[col][i]-v_neg[j]),2)
            j += 1
        s_pos.append(pow(sum_pos,0.5))
        s_neg.append(pow(sum_neg,0.5))

        performance.append(s_neg[i]/(s_pos[i]+s_neg[i]))

    df["TOPSIS Score"]=performance
    df["Rank"]=df["TOPSIS Score"].rank(method='max',ascending=False)
    df.set_index(df.columns[0],inplace=True)
    df.to_csv(args[3])