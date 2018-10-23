class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        s_position = 0
        p_position = 0



    def get_new_s(self,s_postion):
        pass

    def check_poossible_of_pp(self,a_s,a_p):
        if True:    # 存在后续检查的可能性
            pass    # sp++
        elif True:  # 不存在后续检查的可能性
            pass    # sp--
        elif s_position is end:  # sp达到末尾
            if True:    # pp也到末尾
                return True
            else:
                return False
        elif p_position is end: # pp达到末尾
            pass    # 同上一个判断
        else:       # 没有任何a_p的可能性
            return False






if __name__ == "__main__":
    s = "aa"
    p = "a"
    reslut = Solution.isMatch(s, p)
    assert reslut == False
    s = "aa"
    p = "a*"
    reslut = Solution.isMatch(s, p)
    assert reslut == True
    s = "aab"
    p = "c*a*b"
    reslut = Solution.isMatch(s, p)
    assert reslut == False
    s = "mississippi"
    p = "mis*is*p*."
    reslut = Solution.isMatch(s, p)
    assert reslut == False
    s = "mississippi"
    p = "mis*is*ip*."
    reslut = Solution.isMatch(s, p)
    assert reslut == True