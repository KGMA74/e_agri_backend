class Solution:

    def twoSum(self, nums, target: int) :
        hashmap = {}
        for i in range(len(nums)):
            complement = target - nums[i] 
            if complement in hashmap:
                return [i, hashmap[complement]]
            hashmap[nums[i]] = i
        return []
    
print(Solution().twoSum([2, 11, 15, 7], 9))