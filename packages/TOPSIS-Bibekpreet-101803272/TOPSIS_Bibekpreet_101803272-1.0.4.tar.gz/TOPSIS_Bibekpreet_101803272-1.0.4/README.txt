This is a package to find topsis score and rank of a dataframe with only numerical values.

command line usage

python topsis.py "input.csv" "1,1,1,2" "+,+,+,-" "out.csv"

To import :-

1) create a virtual env
2) use command "from TOPSIS_Bibekpreet_101803272.topsis import Topsis"
3) obj = Topsis(df) # here the df is the dataframe in which all the numerical values of columns are present.
4) res = obj.topsis(weights, impact) # here weights and impact are a list