import pandas as pd
import os
import sys


def main():
    # Arguments not equal to 5
    if len(sys.argv) != 5:
        print("ERROR! WRONG NUMBER OF PARAMETERS")
        print("USAGES: $python <programName> <dataset> <weights array> <impacts array> <ResultFileName")
        print(
            "EXAMPLE: $python programName.py inputfile.csv '1,1,1,1' '+,+,-,+' result.csv ")
        exit(1)

    # File Not Found error
    elif not os.path.isfile(sys.argv[1]):
        print(f"File : {sys.argv[1]} Don't exist!!")
        exit(1)

    # File extension not csv
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print(f"The file : {sys.argv[1]} is not csv!!")
        exit(1)

    else:
        df, dd = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[1])
        nCol = len(dd.columns.values)

        # less then 3 columns in input dataset
        if nCol < 3:
            print("Input file have less then 3 columns")
            exit(1)

        # Handeling non-numeric value
        for i in range(1, nCol):
            pd.to_numeric(df.iloc[:, i], errors='coerce')
            df.iloc[:, i].fillna((df.iloc[:, i].mean()), inplace=True)

        # Handling errors of weighted and impact arrays
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("error in weights array please check again")
            exit(1)
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("error in impact array please check again")
                exit(1)

        # Checking number of column,weights and impacts is same or not
        if nCol != len(weights)+1 or nCol != len(impact)+1:
            print("Number of weights, number of impacts and number of columns not same")
            exit(1)

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("Output file extension is wrong")
            exit(1)
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        topsis_algo(dd, df, nCol, weights, impact)


def topsis_algo(dd, df, nCol, weights, impact):
    # normalizing the array
    for i in range(1, nCol):
        temp = 0
        for j in range(len(dd)):
            temp = temp + dd.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(dd)):
            dd.iat[j, i] = (dd.iloc[j, i] / temp)*weights[i-1]

    # Calculating positive and negative values
    p_sln = (dd.max().values)[1:]
    n_sln = (dd.min().values)[1:]
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_sln[i-1], n_sln[i-1] = n_sln[i-1], p_sln[i-1]

    # calculating topsis score
    score = []
    for i in range(len(dd)):
        temp_p, temp_n = 0, 0
        for j in range(1, nCol):
            temp_p = temp_p + (p_sln[j-1] - dd.iloc[i, j])**2
            temp_n = temp_n + (n_sln[j-1] - dd.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    df['Topsis Score'] = score

    # calculating the rank according to topsis score
    df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
    df = df.astype({"Rank": int})
    # Writing the csv
    df.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
    main()


name = "topsis_2508aayushi"
__version__ = "1.0.0"
__author__ = 'Aayushi Gupta'
