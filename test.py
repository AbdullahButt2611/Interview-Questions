def rotate_array(nums, n):
    #TODO: Write - Your - Code  
    print(n%len(nums))
    if n < 0:
        for i in range(-(n)):
            start_element = nums[0]
            for j in range(1, len(nums)):
                nums[j-1] = nums[j]
            nums[len(nums) - 1] = start_element
    else:
        for i in range(n):
            last_element = nums[len(nums) - 1]
            for j in range(len(nums) - 2, -1, -1):
                nums[j+1] = nums[j]
            nums[0] = last_element
    return nums
    

      
  
nums = [1, 10, 20, 0, 59, 86, 32, 11, 9, 40]
n = -11
print(rotate_array(nums, n))