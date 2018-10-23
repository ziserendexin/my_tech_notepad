class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # 法一
        # for i, i_val in enumerate(nums):
        #     nums_2 = nums[i+1:]
        #     for j, j_val in enumerate(nums_2):
        #         sum = i_val + j_val
        #         if sum == target:
        #             return [i, i + j +1]
        # 法二 然而还有重复的。。。就失败喽
        nums_3 = nums.copy()
        nums.sort()
        for i, i_val in enumerate(nums):
            nums_2 = nums[i + 1:]
            for j, j_val in enumerate(nums_2):
                sum = i_val + j_val
                if sum == target:
                    return [nums_3.index(i_val), nums_3.index(j_val)]
                elif sum > target:
                    break
        # 法三 ：但实际上感觉差不多，同样是O(n^2)
        # for idx, i in enumerate(nums):
        #     if target - i in (nums):
        #         if nums.index(target - i) == idx:
        #             continue
        #         return [idx, nums.index(target - i)]
        # return -1
