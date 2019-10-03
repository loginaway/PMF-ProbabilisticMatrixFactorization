# Probabilistic Matrix Factorization

This is an implementation of PMF algorithm.

For the idea of this algorithm, please see *Probabilistic Matrix Factorization*, Ruslan Salakhutdinov and Andriy Mnih.

If you meet any problem while running the code, please file an issue or contact me by loginaway@gmail.com.

## Dependencies

Only *numpy* is needed to be installed manually. Try

`pip install numpy`

or by *conda*, try

`conda install numpy`

## Usage

##### Example Usage

1, modify the configuration in pmf.conf. For the details, see **Configuration**.

2, run `python -m PMF` in the parent directory of PMF.

##### Dataset

Your dataset should be formulated into a .txt file, with each row being an item of data like 0, 1, 5 , where 0 is the index of a certain user, and 1 is that of a movie, and 5 the rating user-0 gives on movie-1. 

##### Configuration

You are required to modify pmf.conf if you want to personalize the settings. There are some explanations for the options.

> trainset_name
>
> testset_name

​	The training dataset name and the testing dataset name. 

> stepsize

​	The step size used in Stochastic Gradient Descent method.

> embedding_dimension

​	The column size of matrix U and V.  (The row sizes are the number of users and number of movies, respectively, set by UVsize.)

> epoch_num	

​	The maximal number of iteration you want the optimizing algorithm to run.

> k_u
>
> k_v

​	The weights of the regularization.

> UVsize

​	The row size of matrix U and V, it is a tuple of dimension 2. For example

​	`UVsize=(5, 6)`  will assign 5 rows to U and 6 rows to V.

> ndcg_top

​	Return ndcg evaluation results. For example

​	`ndcg_top=1, 3, 5` will generate NDCG@1, 3, 5.

> rmse

​	Whether or not to generate RMSE evaluation. `rmse=True / rmse=False`



## References

[1] Ruslan Salakhutdinov and Andriy Mnih, *Probabilistic Matrix Factorization*, 2007.

​	
