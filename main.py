import numpy as np
from typing import Dict


def simul(n_promo: int, n: int, n_simu: int, n_days: int) -> float:
    c = 0

    for _ in range(n_simu):
        tmp = np.random.randint(0, high=n_days, size=n_promo)
        unique, counts = np.unique(tmp, return_counts=True)
        d = dict(zip(unique, counts))
        if n in set(d.values()):
            c += 1

    return c / n_simu


def fact_wrapper(n: int, memory: Dict) -> int:
    '''
        Wrap the fact() function in order to store in memory in the
        memory' dictionary the factorials already computed.

        args:
        - n: int: the number from which to calculate the factorial
        - memory: dict: the dictionary in which are stored the
        already computed factorials (format: {key: fact(key)})

        return: int: the factorial of n
    '''
    if n not in memory.keys():
        memory[n] = fact(n)
    return memory[n]


def fact(n: int) -> int:
    '''
        Computes the factorial of n.

        args:
        - n: int: the number from which to calculate the factorial

        return: int: the factorial of n
    '''
    if n <= 1:
        return 1
    return n * fact(n - 1)


def comb(n: int, p: int, memory: Dict) -> float:
    '''
        Compute the number of combinations of k elements among n. 

        args:
        - n: int: cardinal of a set
        - p: int: the number of elements in each subset
        - memory: dict: dictionary of computed factorials

        return: float: the number of combinations of k elements among n
    '''
    if n < p:
        raise ValueError('N cannot be < P: ', n, p)
    return fact_wrapper(n, memory) / (fact_wrapper(n - p, memory) * fact_wrapper(p, memory))


def partition(n: int, selective_n: int) -> float:
    '''
        Computes and returns the proper partitions of the integer n 
        if they contain at least one selective_n.
        The algorithm used is from the following research paper:
        https://arxiv.org/pdf/0909.2331.pdf

        args:
        - n: int: the number from which to compute the partitions

        return: list of list of int: the proper partitions of n
    '''
    if n < 1:
        raise ValueError('N cannot be less than 1')

    list_partitions = []
    buf = [0 for _ in range(n)]
    index = 1
    buf[1] = n
    
    while index != 0:

        x = buf[index - 1] + 1
        y = buf[index] - 1
        index -= 1

        while x <= y:

            buf[index] = x
            y -= x
            index += 1

        buf[index] = x + y

        new_partition = buf[:index + 1]
        if selective_n in new_partition:
            list_partitions += [new_partition]

    return list_partitions


def birthday_probability(n_promo:int , n: int) -> float:
    '''
        Computes and returns the probability that exactly n students of a class
        of n_promo students share the same day of birth.

        In the case where n < (n_promo/2), 
        the computation of the proper partitions of n_promo and the computations that are applied on them
        can lengthen the execution time of the function.

        The larger the difference between n_promo and n, the longer the function will take to return the result.
        This is due to the amount of eigenpartitions which grows dramatically. (p(x) > 10^12 for x=200)
        Examples:
        - 112s for n_promo=75 and n=1 (7000000 processed scores)
        - 10s  for n_promo=75 and n=20 (450000 processed partitions)
        - 0.2s for n_promo=75 and n=40
        To reduce this time it is possible to simulate the distribution of birthdays over 365 days, 
        this over a large number of iterations, and to deduce the probability that n students share the same day of birth.
        However, the calculated probability will only be an approach of the real probability.

        Here, given enough time and computing power, proba_anniversary() returns an exact probability.

        agrs:
        - n: int: the number of students who share the same date of birth
        - n_promo: int: total number of students in the class

        return: float: the probability that exactly n students in a class
        of n_promo students share the same day of birth.
    '''

    # Keeps track of factorial calculations
    fact_dict_memory = {}
    n_days = 365

    if n > n_promo:
        return 0.0

    # In the case where n > (n_promo/2), it is no longer possible to have 
    # n other students also born on the same day. The calculation is simpler and
    # especially faster.
    if n > n_promo // 2:
        # Proba n students on the same day
        pmj = n_days / (n_days ** n)
        # Proba n_promo - n on other days
        paj = ((n_days - 1) / n_days) ** (n_promo - n)
        # number of groups of n in n_promo students
        nb_grp = comb(n_promo, n, fact_dict_memory)

        return pmj * paj * nb_grp

    # In the case where n < (n_promo/2), it is possible to have n other students
    # born on another day. So we have to use another reasoning
    # to avoid counting these repetitions.

    # Generates all partitions of n_promo, including at least once n
    list_partitions = partition(n_promo, n)

    product_list = []
    for p in list_partitions:

        # Generates a dictionary of occurrences of each number for the partition p
        dict_partition = {v: p.count(v) for v in set(p)}
        product_combin = 1
        product_fact = 1
        occurences_count = 0

        for day_with_student, occurence in dict_partition.items():
            # Calculates the number of ways to repeat a partition of n_promo on n_days 
            product_combin *= comb(n_days - occurences_count, occurence, fact_dict_memory)
            product_fact *= fact_wrapper(day_with_student, fact_dict_memory) ** occurence
            occurences_count += occurence

        product_list.append(product_combin / product_fact)

    # Computes the number of ways to distribute n_promo in n_days discernible locations
    # according to a partition (p1, p2, ..., pn_days), with some pk zero.
    final_proba = sum(product_list) * fact_wrapper(n_promo, fact_dict_memory) / (n_days ** n_promo)

    return final_proba


if __name__ == '__main__':
    n_promo = 30
    n = 4

    print("n: ", n)
    print("n_promo: ", n_promo)
    print(birthday_probability(n_promo, n))
    print(simul(n_promo, n, 100000, 365))
