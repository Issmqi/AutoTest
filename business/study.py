import json
def add():
    b = '12343'
    a = '991232'
    l = max(len(a), len(b))
    a = a.zfill(l)
    b = b.zfill(l)
    res = [0] * l
    flag = 0
    # temp = "0" * max(l_a,l_b)
    for i in range(l - 1, -1, -1):
        temp = int(a[i]) + int(b[i]) + flag
        if temp > 9:
            flag = temp // 10
            temp = temp % 10
        res[i] = temp
    if res[0] == 0:
        res.insert(0, 1)
    print(res)
    return res


# add()
def findUnsortedSubarray(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    m = sorted(nums)
    l, r = 0, len(nums) - 1
    while l < r and nums[l] == m[l]:
        l += 1
    while l < r and nums[r] == m[r]:
        r -= 1
    return r - l + 1


# findUnsortedSubarray([1,2,3,4])
def nthUglyNumber(n):
    """
    :type n: int
    :rtype: int
    """
    res = [1]
    p2 = 0
    p3 = 0
    p5 = 0
    for i in range(n - 1):
        # temp = min(res[p2] * 2, res[p3] * 3, res[p5] * 5)
        # res.append(temp)
        res.append(min(res[p2] * 2, res[p3] * 3, res[p5] * 5))
        if res[-1] == res[p2] * 2:
            p2 += 1
        if res[-1] == res[p3] * 3:
            p3 += 1
        if res[-1] == res[p5] * 5:
            p5 += 1
    print(res[-1])
    print(res)
    return res[-1]


# nthUglyNumber(30)


def isUgly(num):
    """
    :type num: int
    :rtype: bool
    """
    if num < 1:
        return False

    while num % 2 == 0:
        num = num // 2
    while num % 3 == 0:
        num = num // 3
    while num % 5 == 0:
        num = num // 5
    return num == 1


# isUgly(27)
def reverseString(s):
    """
    :type s: List[str]
    :rtype: None Do not return anything, modify s in-place instead.

    """
    l, r = 0, len(s) - 1
    while l < r:
        s[l], s[r] = s[r], s[l]
        l += 1
        r -= 1
    print(s)
    return s
    # i=len(s)-1
    # while i>=0:
    #     s.append(s.pop(i))
    #     i-=1
    # return s


# reverseString(["h","e","l","l","o"])
def removeElement(nums, val):
    """
    :type nums: List[int]
    :type val: int
    :rtype: int
    """
    for i in range(len(nums) - 1, -1, -1):
        # for i in range(len(nums)):
        if nums[i] == val:
            nums.pop(i)
    return nums


# removeElement([0,1,2,2,3,0,4,2],2)
def findErrorNums(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    ss = sum(range(len(nums) + 1))
    re = sum(nums) - sum(set(nums))
    S = sum(set(nums))
    return [sum(nums) - S, len(nums) * (len(nums) + 1) // 2 - S]


# findErrorNums([3,2,3,4,6,5])

def shortestToChar(S, C):
    cc = [i for i in range(len(S)) if C == S[i]]
    print(cc)
    re = [min(abs(x - i) for i in cc) for x in range(len(S))]
    print(re)
    return re


# S = "loveleetcode"
# C = 'e'
# shortestToChar(S,C)
def uniqueOccurrences(arr):
    """
    :type arr: List[int]
    :rtype: bool
    """
    num_dict = {}
    for a in arr:
        if a not in num_dict:
            num_dict[a] = 1
        else:
            num_dict[a] += 1
    nums_list = list(num_dict.values())
    return len(nums_list) == len(set(nums_list))


def isPalindrome(s):
    s = s.lower()
    ss = []
    for i in s:
        if i.isalnum():
            ss.append(i)
    return ss == ss[::-1]


# isPalindrome(' abc ba ')
def singleNumber(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    # return sum(set(nums))*2-sum(nums)
    a = 0
    for num in nums:
        a = a ^ num
    # print(a)
    return a


# singleNumber([2,1,2])
def findDuplicates(nums):
    res = []
    for i in range(len(nums)):
        loc = abs(nums[i]) - 1
        if nums[loc] < 0:
            res.append(loc + 1)
        nums[loc] = -nums[loc]
    return res


# findDuplicates([4,3,2,7,8,2,3,1])


# def findDuplicate(self, nums):
#
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     # for i in range(len(nums)):
#     #     loc = abs(nums[i]) - 1
#     #     if nums[loc] < 0:
#     #         return loc + 1
#     #     nums[loc] = -nums[loc]
#     for i in range(len(nums)):
#         loc = abs(nums[i]) - 1
#         if nums[loc] < 0:
#             return loc + 1
#         nums[loc] = -nums[loc]
# findDuplicate([1,3,4,2,2])


def sortArrayByParityII(A):
    i, j = 0, 1
    while i < len(A) - 1:
        if A[i] % 2 == 0:
            i += 2
        elif A[j] % 2 == 1:
            j += 2
        else:
            temp = A[i]
            A[i] = A[j]
            A[j] = temp
    print(A)
    return A


# sortArrayByParityII([4,2,5,7])
def addDigits(num):
    # if num > 9:
    #     num = num % 9
    #     if num == 0:
    #         return 9
    # return num
    return (num - 1) % 9 + 1


def findDuplicate(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    # for i in range(len(nums)):
    #     loc = abs(nums[i]) - 1
    #     if nums[loc] < 0:
    #         return loc + 1
    #     nums[loc] = -nums[loc]

    # left = 1
    # right = len(nums)
    # while left < right:
    #     mid = int(left + (right - left) / 2)
    #     cnt = 0
    #     for num in nums:
    #         if num <= mid:
    #             cnt += 1
    #     if cnt <= mid:
    #         left = mid + 1
    #     else:
    #         right = mid
    # return right

    s = 0
    f = 0
    while True:
        s = nums[s]
        f = nums[nums[f]]
        if s == f:
            f = 0

            while nums[s] != nums[f]:
                f = nums[f]
                s = nums[s]
            return nums[s]


# findDuplicate([1,3,4,2,2])
def plusPne(digits):
    flag = 1
    for i in range(len(digits) - 1, -1, -1):
        temp = digits[i] + flag
        if temp > 9:
            flag = 1
            digits[i] = temp % 10
        else:
            flag = 0
            digits[i] = temp
    if digits[0] == 0:
        digits.insert(0, 1)
    return digits


# plusPne([1,2,4])

def cal_num(*args):
    ax = 0
    for i in args:
        ax = ax + i
    return ax

# 返回函数
def lazy_sum(*args):
    def sum():
        ax=0
        for i in args:
            ax=ax+i
        return ax
    return sum

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

# f1, f2, f3 = count()
def createCounter():
    ax=0
    def counter():
        return ax+1
    return counter
# createCounter()

def singleton(cls):
    _instance={}
    def _singleton(*args,**kwargs):
        if cls not in _instance:
            _instance[cls]=cls(*args,**kwargs)
        return _instance[cls]
    return singleton

@singleton
class A():
    def __init__(self,x=0):
        self.x=x
# a=A(2)
# b=A(3)
# print(a)
# print(b)
desired_cap_android = \
    {
    'platformName': 'Android',
    'platformVersion': '8.0.0',
    'deviceName': '小米手机',
    # 'appPackage': 'com.tencent.mm',
    'appPackage':'com.ximalaya.ting.android',
    # 'appActivity': '.ui.LauncherUI',
    'appActivity': 'com.ximalaya.ting.android.host.activity.WelComeActivity',
    'unicodeKeyboard': True,
    'resetKeyboard': True,
    'noReset': True,
    'recreateChromeDriverSessions': True,
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
    #'newCommandTimeout':'60'  #设置未接受到新命令的超时时间，默认60s，说明：如果60s内没有接收到新命令，appium会自动断开，
    }
