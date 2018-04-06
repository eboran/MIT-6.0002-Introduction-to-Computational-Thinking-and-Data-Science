###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1

def fast_helper(eggs , egg_weights , target_weight, memo):
    try:
        return memo[len(egg_weights),target_weight]
    except KeyError:
        if target_weight == 0:
            return (0,{key: 0 for key in eggs})
        elif egg_weights[-1] > target_weight:
            a,b = helper(eggs,egg_weights[:-1],target_weight,memo)
            result = (a,b.copy())
        else:
            next_value = egg_weights[-1]
            withValue, resultWith = fast_helper(eggs,egg_weights[:], target_weight - next_value, memo)
            resultWith_ = resultWith.copy()
            resultWith_[next_value] += 1
            withValue += 1
            if next_value != 1:
                withoutValue, resultWithout = fast_helper(eggs,egg_weights[:-1], target_weight, memo)
                resultWithout_ = resultWithout.copy()
                if withValue < withoutValue:
                    result = (withValue, resultWith_)
                else:
                    result = (withoutValue, resultWithout_)
            else:
                result = (withValue, resultWith_)
        memo[len(egg_weights),target_weight] = result
        return result

def fast_dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    eggs = egg_weights[:]
    sum_, result_ = fast_helper(eggs, egg_weights, target_weight, memo)
    result_ = ConverToString(result_)
    return str(sum_) + " " + result_

def helper(eggs, egg_weights, target_weight, memo):
    if target_weight == 0:
        return (0, {key: 0 for key in eggs})
    elif egg_weights[-1] > target_weight:
        a, b = helper(eggs, egg_weights[:-1], target_weight, memo)
        result = (a, b.copy())
    else:
        next_value = egg_weights[-1]
        withValue, resultWith = helper(eggs, egg_weights[:], target_weight - next_value, memo)
        resultWith_ = resultWith.copy()
        resultWith_[next_value] += 1
        withValue += 1
        if next_value != 1:
            withoutValue, resultWithout = helper(eggs, egg_weights[:-1], target_weight, memo)
            resultWithout_ = resultWithout.copy()
            if withValue < withoutValue:
                result = (withValue, resultWith_)
            else:
                result = (withoutValue, resultWithout_)
        else:
            result = (withValue, resultWith_)
    return result

def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    eggs = egg_weights[:]
    sum_, result_ = helper(eggs, egg_weights, target_weight, memo)
    result_ = ConverToString(result_)
    return str(sum_) + " " + result_


def ConverToString(d):
    ans = "("
    cpy = []
    sum_ = 0
    for key_ in d:
        cpy.append(key_)
    cpy = sorted(cpy,reverse = True)
    for key_ in cpy:
        if d[key_]:
            ans += str(d[key_]) + " * " + (str(key_)) + " + "
            sum_ += d[key_] * key_
    ans = ans[:-3]
    ans += " = " + str(sum_) + ")"
    return ans

import time
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10,25)
    n = 99
    print(egg_weights)
    print(str(n))
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    now = time.clock()
    print("Actual output with fast:", fast_dp_make_weight(egg_weights, n))
    print("with dict: ", time.clock()-now)
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    now = time.clock()
    print("Actual output:", dp_make_weight(egg_weights, n))
    print("without dict: ", time.clock()-now)
