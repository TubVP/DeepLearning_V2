def sum_of_two_largest(nums):
    nums.sort()
    return nums[-1] + nums[-2]
