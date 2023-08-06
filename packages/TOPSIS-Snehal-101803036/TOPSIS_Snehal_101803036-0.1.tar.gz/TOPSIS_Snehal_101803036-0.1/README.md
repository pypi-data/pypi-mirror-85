# TOPSIS
The Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) is a multi-criteria decision analysis method. It is based on the concept that the chosen alternative should have the shortest geometric distance from the positive ideal solution (PIS) and the longest geometric distance from the negative ideal solution (NIS).


### Necessary installments
  - Pandas should be pre-installed.

### Check Source
Input file checked if it is available in the system or if the format is supported.

### Check weight
Weight must be entered as a string and should contain numeric values only and values must be seperated by ','. This function returns if the syntax is appropriate.

### Check impact

Impact must be entered as a string and should contain either values '+' or '-' only and values must be seperated by ','. This function returns if the syntax is appropriate.

### Square and divide
A normalised table is received with values which are calculated as every element in each collumn is squared and added following which square root of the obtained value is calculated which is further divided by the original elements in each column. 

### multiply weightage
Each column is assigned a weightage and corresponding values are multiplied by this value. Syntax is first checked following which each column is multiplied by its corresponding weight.

### best worst value
Maximum and minimum value for each value is found using this function and according to the impact best value is assigned the maximum or the minimum value

### topsis score
In this function we can calculate the performance scores for each item. Here first each value in the row is subtracted from its corresponding best value and squared and added with the other elements calculated in the same way. Similarly the original elements are also subtracted from the worst value and same calculations are carried. Then the values obtained from both the calculations are added and the second calculation value obtained is divided by this calculated value and we get our performance score and this is done for all rows.


### rank
 In this function all rows are assigned a rank according to their performance/topsis score.

License
----

MIT




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
