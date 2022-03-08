# BirthdayProbabilty

What is the probabilty that N students in a M students class were born the same day ?

The code in this repository computes and returns the probability that exactly n students of a class of n_promo students share the same day of birth.
In the case where n < (n_promo/2), the computation of the proper partitions of n_promo and the computations that are applied on them can lengthen the execution time of the function.

The larger the difference between n_promo and n, the longer the function will take to return the result.
This is due to the amount of eigenpartitions which grows dramatically. (p(x) > 10^12 for x=200)

Examples:
- 112s for n_promo=75 and n=1 (7000000 processed scores)
- 10s  for n_promo=75 and n=20 (450000 processed partitions)
- 0.2s for n_promo=75 and n=40

To reduce this time it is possible to simulate the distribution of birthdays over 365 days, this over a large number of iterations, and to deduce the probability that n students share the same day of birth. However, the calculated probability will only be an approach of the real probability.

The provided script, given enough time and computing power, will return an exact probability.

