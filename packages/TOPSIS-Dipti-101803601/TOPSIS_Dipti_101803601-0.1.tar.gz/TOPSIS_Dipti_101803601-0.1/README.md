# TOPSIS_Dipti_101803601
With this you can calculate the TOPSIS score and RANK of the data provided in '.csv' format.
- Input file:
  - contain three or more columns
  - First column is the object/variable name.
  - From 2nd to last column contain numeric values only

# Overview
  - You can check intermediate steps as well as the final score i.e it provides functions to calculate normalized matrix, weight normalized decision matrix , ideal best , ideal worst lists and so on.

## Usage

In the following paragraphs, I am going to describe how you can get and use TOPSIS for your own projects.

### Getting it
To download TOPSIS, either fork this github repo or simply use Pypi via pip.

    $ pip install TOPSIS_Dipti_101803601

### Using it
TOPSIS was programmed with ease-of-use in mind. Just, import topsis from TOPSIS-Aditi-101803650

    from TOPSIS_Dipti_101803601 import topsis

And you are ready to go! 

## topsis
There are 5 functions in this:
  - normalized_matrix
  - weight_normalized
  - ideal_best_worst
  - euclidean_distance
  - topsis_score

### normalized_matrix()
This function takes location of the input file as parameter and returns normalized decision matrix.

### weight-normalized()
This function takes location of the input file as well as the weights corresponding to columns in file. No. of weights should be equal to the no. of columns(from 2nd to last column). It returns weight normalized decision matrix.

### ideal_best_worst()
This takes location of input file, weights and impacts as parameters. Impact should either be "+" or "-" and should be separated by ",". No. of impacts should also be equal to the no. of columns(from 2nd to last column). It return two lists: one with ideal best values and the other with ideal worst values corresponding to every column.

### euclidean_distance()
This takes same input as that of ideal_best_worst() function but returns two lists:

  1) Euclidean distance from ideal best
  2) Euclidean distance from ideal worst
  
### topsis_score()
This also takes the same input as the previous function but returns matrix with the same columns as input file and two more columns named 'Topsis Score' and 'Rank'.

So any function can be used in the below format:

    topsis.function_name(parameters)
