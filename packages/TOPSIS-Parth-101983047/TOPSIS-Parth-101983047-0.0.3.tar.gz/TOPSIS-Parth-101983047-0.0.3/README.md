<h1 style="text-align: justify; color: black">TOPSIS</h1>

<h5 style="text-align: justify; color: black">TOPSIS is an acronym that stands for ‘Technique of Order Preference Similarity to the Ideal Solution’ and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those. It was presented in Hwang and Yoon (Multiple attribute decision making: methods and applications. Springer, Berlin, 1981) and Chen and Hwang (Fuzzy multiple attribute decision making methods. Springer, Berlin, 1992), and can be considered as one of the classical MCDA methods that has received a lot of attention from scholars and researchers.
</h5>
<h2 style="text-align: justify; color: black">Dependencies</h2>

```
• OS
• Pandas
```

<h2 style="text-align: justify; color: black">Installation
</h2>

```
pip install TOPSIS-Parth-101983047==0.0.2
```

<h2 style="text-align: justify; color: black">Usage
</h2>

```
perform_Topsis(source, weights, impacts, result)
```

<h2 style="text-align: justify; color: black">Parameters
</h2>

```
source : Input data file in .csv format
weights : List of weights for columns except first column
impacts : list of impacts for columns except first column
result : Output file name to store results in .csv format
```

<h2 style="text-align: justify; color: black">Constraints / Exceptions handled
</h2>

```
1. Correct number of parameters (source, weights, impacts, result)
2. Handling of “File not Found” exception
3. Input file must contain three or more columns.
4. From 2 nd to last columns must contain numeric values only (Handling of non-numeric values)
5. Number of weights, number of impacts and number of columns (from 2 nd to last columns) must
be same.
6. Impacts must be either +ve or -ve.
7. Impacts and weights must be separated by ‘,’ (comma).
8. Output "File already exists" condition
```

<h2 style="text-align: justify; color: black">Example
</h2>

```
>>>python
>>>from Topsis-Parth-101983047.Topsis import topsis
>>>topsis.perform_Topsis('data.csv', [1,2,1,2], [+,-,-,+], 'result.csv')
```
