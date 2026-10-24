def sum_of_two_largest(nums):
    ...
def sum_of_two_largest(nums):
    largest_1 = largest_2 = -float('inf')
    for num in nums:
        if num > largest_1:
            largest_2 = largest_1
            largest_1 = num
        elif num > largest_2:
            largest_2 = num
    return largest_1 + largest_2