# TOPSIS Implementation by Ayush Jain 101803690	
This package will get topsis score for selected csv file.

## Important Details
Input/Output Files:

Input File

-> Input file contain three or more columns

-> First column is the object/variable name (e.g. M1, M2, M3, M4...)

-> From 2nd to last columns contain numeric values only

Output Files
-> Result file contains all the columns of input file and two additional columns having TOPSIS SCORE and RANK

The parameters for the topsis functions are as follows:
-> The input file name. It must end with .csv or .txt. You can give the complete file path if you want to read a file from some specific place

-> The weights string which is comma seperated for each weight.
   Example: "1,1,2,3"

-> The impact string which is comma seperated for each impact and determines if weight at that index is to be taken positive or negative.
   Example: "-,+,+,+"

-> The output file name. It must end with .csv or .txt. You can give the complete path along with file name to save the file at specific place. Otherwise, it will save it as default where the package is installed.

The package has only one function topsis(4 parameters(all necessary else exceptions occur)). 

Sample Use case:

```
import TOPSIS_AyushJain_101803690 as t
t.topsis("input.csv","1,1,1,1","+,+,+,+","output.csv")