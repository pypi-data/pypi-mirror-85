# ds4se
> Data Science for Software Engieering (ds4se) is an academic initiative to perform exploratory analysis on software engineering artifacts and metadata. Data Management, Analysis, and Benchmarking for DL and Traceability.


This documentation composed of 4 parts: 

1)architecture

2)deployment

3)installation 

4)usage

## Architecture

Below is the Architecture diagram of the DS4Se library.

![DS4SE.png](ds4se\model\DS4SE.png)

Users of the DS4SE API will pass in either strings or pandas dataframes that consist of content of either source or target artifacts as input, and get different analytical results of the input depending on the function user called.  

The DS4SE library is divided into two parts: Traceability and Analysis, corresponind to different usages of the API. 



#### Traceability

The traceability part consists only one method: TraceLinkValue(), that will process strings with user-specified technique. This method intends to support 6 different techniques: 


VSM

orthogonal

JS

LDA

LSA

word2vec

doc2vec

>Currently only word2vec and doc2vec are inplementated. The implementations are in notebook 3.4_facade.ipynb and corresponind generated facade.py file. Actual implementation of word2vec and doc2vec are in the notebook 3.2_mining.unsupervised.eval.ipynb and corresponding nbdev generated eval.py. As the diagram shows, 3.4_facade.ipynb imports eval.py for instantiation of either word2vec or doc2vec class object. Those object then load "*.model" file and start calculation. 

To further add implementations for other techniques, programmers should modify notebook 3.4_facade.ipynb. 

#### Analysis
The analysis part of the API consists 9 methods: 

NumDoc()

VocabShared()

VocabSize()

Vocab()

SharedVocabSize()

AverageToken()

CrossEntropy()

KLDivergence()

MutualInformation()



Currently only KLDivergence() and MutualInformation() are NOT inplementated. The implementations are in notebook 3.4_facade.ipynb and corresponind generated facade.py file. 

All methods in this section takes in pandas dataframe(s) as input. 

>NumDoc() method are simple enough to stand on its own, it just count the number of rows in dataframes. 

>Functions VocabShared(), VocabSize(), Vocab(), SharedVocabSize(), AverageToken() only need a sentencepiece processor bpe model to function. All these methods instantiate a processor by a "*.model" file and receive a Counter object, in which results are stored.

>Actual implementation of CrossEntropy() is in notebook 1.0_exp.i.ipynb as dit_shannon(). CrossEntropy() simply combines two user-provided dataframes and process it through sentencepiece processor and calls this method with resulting Counter object. 

To further add implementations for KLDivergence() and MutualInformation(), notebook 3.4_facade.ipynb should be modified. 

## Deployment

The API is deployed to pypi at https://pypi.org/project/ds4se/. 

To deploy future version of the API, follow steps listed below:

    1) open setting.ini and increment the version number. 
    
    2) open terminal and run following commmad to package the library:
> python3 setup.py sdist bdist_wheel 
    
    3) run following command to upload the package:>twine upload dist/*  
    4) when promoted for username, type in username:
> ds4se
   
    5) when promoted for password, type in username:>ds4seCS435   
   
Note: you might need to run the following commands to make sure you have the latest version of setuptools, wheel and twine:
> python3 -m pip install --user --upgrade setuptools wheel
  
>python3 -m pip install --user --upgrade twine

To include non-".py" file in the package, modified package_data variable in setup.py. For example, if you want to include "hello.model" and "world.csv" in the package, package_data should be:>package_data={'': ['hello.model','world.csv']},


## Install

To install the API, run following commmand:
> pip install ds4se

If you need to upgrade DS4SE, run:> pip install DS4SE --upgrade
The library requires several other libraries, to install/upgrade them, run these command:
> pip install --upgrade gensim

>pip install nbdev

>pip install sentencepiece

>pip install dit

After installing/upgrading above libraries, DS4SE is ready to use!

## How to use

After installing the API, import ds4se.facade to use its functionalities.

```python
import ds4se.facade as facade
```

## Traceability

To use the ds4se library to calculate trace link value of proposed trace link with given.The function will takes in two strings for contents for source file and target file, feed two strings into a model that user specifies, and return traceability value.

    Supported technique model:
        VSM
        LDA
        orthogonal 
        LSA
        JS
        word2vec
        doc2vec

The function returns a tuple of two integers, with the first element as distance between two artifacts and the second element be the similarity between two artifacts, which is the traceability value.

```python
facade.TraceLinkValue("source_string is a string of entire content of one source file","target_string is a string of entire content of one targetfile","word2vec")
```

    2020-11-01 22:55:01,937 : INFO : adding document #0 to Dictionary(0 unique tokens: [])
    2020-11-01 22:55:01,947 : INFO : built Dictionary(1815 unique tokens: ['@return', 'Converts', 'The', 'a', 'and']...) from 153 documents (total 5769 corpus positions)
    2020-11-01 22:55:01,949 : INFO : loading Word2Vec object from c:\users\admin\desktop\fall2020\software engineering\project\github desktop\ds4se\ds4se\model\word2vec_libest.model
    2020-11-01 22:55:01,997 : INFO : loading wv recursively from c:\users\admin\desktop\fall2020\software engineering\project\github desktop\ds4se\ds4se\model\word2vec_libest.model.wv.* with mmap=None
    2020-11-01 22:55:01,998 : INFO : setting ignored attribute vectors_norm to None
    2020-11-01 22:55:01,999 : INFO : loading vocabulary recursively from c:\users\admin\desktop\fall2020\software engineering\project\github desktop\ds4se\ds4se\model\word2vec_libest.model.vocabulary.* with mmap=None
    2020-11-01 22:55:01,999 : INFO : loading trainables recursively from c:\users\admin\desktop\fall2020\software engineering\project\github desktop\ds4se\ds4se\model\word2vec_libest.model.trainables.* with mmap=None
    2020-11-01 22:55:02,001 : INFO : setting ignored attribute cum_table to None
    2020-11-01 22:55:02,002 : INFO : loaded c:\users\admin\desktop\fall2020\software engineering\project\github desktop\ds4se\ds4se\model\word2vec_libest.model
    2020-11-01 22:55:02,015 : INFO : precomputing L2-norms of word weight vectors
    2020-11-01 22:55:02,019 : INFO : constructing a sparse term similarity matrix using <gensim.models.keyedvectors.WordEmbeddingSimilarityIndex object at 0x000001F77D3A65B0>
    2020-11-01 22:55:02,020 : INFO : iterating over columns in dictionary order
    2020-11-01 22:55:02,022 : INFO : PROGRESS: at 0.06% columns (1 / 1815, 0.055096% density, 0.055096% projected density)
    2020-11-01 22:55:02,167 : INFO : PROGRESS: at 55.15% columns (1001 / 1815, 0.140033% density, 0.209102% projected density)
    2020-11-01 22:55:02,227 : INFO : constructed a sparse term similarity matrix with 0.173668% density
    2020-11-01 22:55:02,235 : INFO : Removed 7 and 7 OOV words from document 1 and 2 (respectively).
    2020-11-01 22:55:02,236 : INFO : adding document #0 to Dictionary(0 unique tokens: [])
    2020-11-01 22:55:02,238 : INFO : built Dictionary(4 unique tokens: ['content', 'file', 'one', 'string']) from 2 documents (total 7 corpus positions)
    2020-11-01 22:55:02,239 : INFO : Computed distances or similarities ('source', 'target')[[0.12804699828021432, 0.88648788705131]]
    




    (0.12804699828021432, 0.88648788705131)



word2vec_metric is an optional parameter when using word2vec as technique, available metrics are: 
   <br> WMD
  <br>  SCM

## Analysis

This is the data analysis part of ds4se library, users can use the library to conduct analysis on artifacts with information theory and statistical analysis

For all functions in analysis part, input should be pandas dataframe with following structure

```python
d = {'contents': ["hello world", "this is a content of another file"]}
df = pd.DataFrame(data=d)
print(df)
```

                                contents
    0                        hello world
    1  this is a content of another file
    

### Usage of ds4se model to calculate the number of documents of either source or target class

    The method can process dataframes for artifacts contents and return the number of documents each artifacts class contains. 
    It takes in two parameters, a pandas dataframe for source artifacts and a pandas data frame for target artifacts, and it will do calculation for both classes.
    
    The method returns a list of 4 integers:
    1: number of documents for source artifacts;
    2: number of documents for target artifacts;
    3: source difference (difference between previous two results);
    4: target difference (same as above, but opposite sign).

```python
result = facade.NumDoc(source_df, target_df)
source_doc = result[0]
target_doc = result[1]
difference_source = result[2]
difference_target = result[3]
print("The number of documents for source is {} , with {} source difference".format(source_doc, difference_source))
print("The number of documents for target is {} , with {} target difference".format(target_doc, difference_target))
```

    The number of documents for source is 2 , with 0 source difference
    The number of documents for target is 2 , with 0 target difference
    

### Usage of ds4se model to calculate the vocabulary size of either source or target class

    The method can process dataframes for artifacts contents and return the total number of vocab contained in each artifact class. 
    The method takes in two parameters, source artifacts and target artifacts, and it will do calculation for both classes.
    
    The method returns a list of 4 integers:
    1: vocabulary size for source artifacts;
    2: vocabulary size for target artifacts;
    3: source difference;
    4: target difference.

```python
vocab_result = facade.VocabSize(source_df, target_df)
source = vocab_result[0]
target = vocab_result[1]
difference_source = vocab_result[2]
difference_target = vocab_result[3]
print("The vocabulary size for source is {} , with {} target difference".format(source, difference_source))
print("The vocabulary size for target is {} , with {} target difference".format(target, difference_target))
```

    The vocabulary size for source is 10 , with 0 target difference
    The vocabulary size for target is 10 , with 0 target difference
    

### Usage of ds4se model to calculate the average number of token of either source or target class

    The method can process dataframes for artifacts contents and return the average number of tokens in each artifact class. 
    It does calculation by first finding the total number of token for each artifact class, and then divide each of them by the number of documents present in each artifacts.
    The method takes in two parameters, source artifacts and target artifacts, and it will do calculation for both classes.
    
    The method returns a list of 4 integers:
    1: average number of token for source artifacts;
    2: average number of token for target artifacts;
    3: source difference;
    4: target difference.

```python
token_result = facade.AverageToken(source_df, target_df)
source = token_result[0]
target = token_result[1]
difference_source = vocab_result[2]
difference_target = vocab_result[3]
print("The number of average token for source is {} , with {} source difference".format(source, difference_source))
print("The number of average token for target is {} , with {} target difference".format(target, difference_target))
```

    The number of average token for source is 107 , with 35 source difference
    The number of average token for target is 143 , with -35 target difference
    

### Usage of ds4se model to retriev term frequency

    The method can process dataframes for artifacts contents and return the top three most frequent terms that appears in artifact class. It employs bpe model to precess the contents in each dataframe

    The method takes in two parameters, 
    1: source artifacts,
    2: target artifacts, 
    and it will do calculation for both classes.
    
    The method returns a dictonary with 
    key: token
    value: a list of count and frequency

```python
facade.VocabShared(source_df,target_df)
```




    {'est': [160, 0.16], 'http': [136, 0.136], 'frequnecy': [124, 0.124]}



If user only need the term frequency of one of two classes, they can choose to use Vocab() function, which is exactly the same except Vocab only processes one dataframe for one artifact class

```python
facade.Vocab(artifacts_df)
```




    {'est': [141, 0.141], 'http': [136, 0.136], 'frequnecy': [156, 0.156]}



### For Shared Metrics

Using the following metrics to compute using both source and target artifacts, use the following funtions. 

For all methods below, two parameters are required: source and target artifacts, they are all in form of dataframes

They all return one integer value

Shared vocabulary size

return the totla vocab size of source and target combined

```python
facade.SharedVocabSize(source_df, target_df)
```




    112



Mutual information

```python
facade.MutualInformation(source_df, target_df)
```




    127



CrossEntropy

CrossEntropy calculates shanno entropy of combind source and target artifacts, it returns a integers.

```python
facade.CrossEntropy(source_df, target_df)
```




    171



KL Divergence

```python
facade.KLDivergence(source_df, target_df)
```




    152


