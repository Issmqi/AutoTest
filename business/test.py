# -*- coding: utf-8 -*-
# !/bin/bash
import pytest
from functools import reduce
def nearStr(s):
    a = []
    re = ''
    for i in range(len(s)):
        if s[i] not in a:
            re += s[i]
            if s[i] != ' ':
                a.append(s[i])
    print(re)
    return re


# s = "aabb cccg h iii"
# nearStr(s)

def findnums(nums):
    if not nums:
        return None
    l,r=0,len(nums)-1
    while l<r:
        temp=(l+r)//2
        if (nums[temp]>nums[temp-1]) and (nums[temp]>nums[temp+1]):
            return  nums[temp]
        elif  nums[temp]<nums[temp-1]:
            r=temp
        elif nums[temp]<nums[temp+1]:
            l=temp+1
# nums=[1,1,1]
# print(findnums(nums))

def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """

    st = {}
    i = 0
    ans = 0
    for j in range(len(s)):
        if s[j] in st:
            i = max(i, st[s[j]]+1)
        ans = max(ans, j - i + 1)
        st[s[j]] = j
    return ans
# a=lengthOfLongestSubstring("aaa")
# print(a)

def threeSum(nums):
    n = len(nums)
    nums.sort()  # 先排序
    ans = []
    for first in range(n - 2):  # 枚举第一个元素
        if nums[first] > 0: break  # 数组里最小的都大于0 不可能有答案
        if first > 0 and nums[first] == nums[first - 1]: continue  # 保证first不会有重复
        # 以下作为标准双指针写法
        second, third = first + 1, n - 1
        while second < third:
            target = 0 - nums[first]
            s = nums[second] + nums[third]
            if s > target:  # 当前数值太大 做出决策：右指针左移
                third -= 1  # 左移后有重复没关系 重复的就肯定又回来这里减1啦
            elif s < target:  # 当前数值太小 做出决策：左指针右移
                second += 1
            else:  # 前数值正合适 做出决策：左指针右移且右指针左移 注意不能重复
                ans.append([nums[first], nums[second], nums[third]])
                second += 1
                third -= 1
                while third > second and nums[third] == nums[third + 1]: third -= 1
                while third > second and nums[second] == nums[second - 1]: second += 1
    print(ans)
    return ans
# threeSum( [-1, 0, 1, 2, -1, -4])
def check_ipv4(s):
    try:
        ip_list=s.split('.')
        if len(ip_list) !=4:
            return False
        for ip in ip_list:
            if ip[0]=='0' and len(ip)>1:
                return False
            if int(ip)<0 or int(ip)>255:
                return False
        return True
    except:
        return False

# a=check_ipv4('255.255.255.001')
# print(a)
def findLocation(nums,target):
    # res=[0]*2
    if not nums:
        return None
    l,r=0,len(nums)-1
    # while l<=r:
    #     if nums[l]==target:
    #         res[0]=l
    #     else:
    #         l+=1
    #     if nums[r]==target:
    #         res[1]=r
    #     else:
    #         r-=1
    # return res
    while l <=r:
        mid=l+(r-l)//2
        if nums[mid]>target:
            r=mid
        elif nums[mid]<target:
            l=mid+1

        else:
            while nums[l]!=target:
                l+=1
            while nums[r] !=target:
                r-=1
            return (l,r)
    return (-1,-1)



# a=findLocation([1,2,3,4,4,4,6],4)
# print(a)
def findPre(nums):
    print(list(zip(*nums)))
    s=list(map(set,zip(*nums)))
    print(s)
    res=[]
    for x in s:
        x=list(x)
        if len(x)>1:
            break
        res+=x
    print(res)
# findPre(['flow','flawer','float'])
def sortodd(nums):
    # l1=[i for i in nums if i%2!=0]
    # l2=[j for j in nums if j%2==0]
    # return l1+l2
    n=len(nums)
    # odd,even=0,1
    # while odd<=l and even<=l:
    #     if nums[odd]%2==1:
    #         odd+=1
    #     elif nums[even]%2==0:

    # for i in range(n):
    #     if nums[i]%2==0:
    #         nums.append(nums.pop(i))
    # return nums
    # l,r=0,n-1
    # while l <=r:
    #     if nums[l]%2==1:
    #         l+=1
    #     elif nums[r]%2==0:
    #         r-=1
    #     else:
    #         nums[l],nums[r]=nums[r],nums[l]
    # return nums
    # odd=0
    # for i in range(n):
    #     if nums[i]%2==1:
    #         nums[i],nums[odd]=nums[odd],nums[i]
    #         odd += 1
    # return nums
    # for i in range(n):
    #     temp=nums[i]
    #     for j in range(i,-1,-1):
    #         if nums[j-1]>temp:
    #             nums[j]=nums[j-1]
    #         else:
    #             break
    #     nums[j]=temp
    # return nums

    for i in range(n-1):
        temp=nums[i]
        for j in range(n-i-1):
            if nums[j]>nums[j+1]:
                nums[j],nums[j+1]=nums[j+1],nums[j]
        return nums



# re=sortodd([1,2,22,3,19,4,5,6,7,8,9,11,20,30,21])
# print(re)

def bubble_sort(nums):
    n=len(nums)
    # for i in range(n):
    #     for j in range(i+1,n):
    #         if nums[j]<nums[j-1]:
    #             nums[j],nums[j-1]=nums[j-1],nums[j]
    # return nums
    n = len(nums)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums

def select_sort(nums):
    n=len(nums)
    for i in range(n-1):
        temp=nums[i]
        for j in range(i,n-1):
            if nums[j]<temp:
                nums[j],temp=temp,nums[j]
    return nums



# nums=[1,2,22,3,19,4,5,6,7,8,9,11,20,30,21]
# print(bubble_sort(nums))
# print(select_sort(nums))
def findLengthOfLCIS(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    if not nums:
        return 0
    res = []
    for i in range(len(nums) - 1):
        count = 1
        for j in range(i, len(nums) - 1):
            if nums[j + 1] > nums[j]:
                count += 1
            else:
                break
        res.append(count)
    return max(res)
# findLengthOfLCIS([1])
# def sum_1(nums):
# a=list(filter(lambda x:x%2==1,range(1,20)))
# print(a)
# def f(x,y):
#     return x+y
# b=reduce(lambda x,y:x+y ,[1, 3, 5, 7, 9, 11])
# print(b)
# c=list(map(lambda x:x*2,[1,3,5,7]))
# print(c)
def countSubstrings(s):
    """
    :type s: str
    :rtype: int
    """
    if not s:
        return 0
    n = len(s)
    count = 0
    for i in range(n):
        for j in range(i, n):
            temp=s[i:j+1]
            if temp == temp[::-1]:
                count += 1
    return count
# print(countSubstrings('aaa'))
# print(sum(range(101)))
# print(reduce(lambda x,y:x+y,range(101)))
# print(list(filter(lambda x:x%2==0,range(21))))
#
# def fib(max):
#     n,a,b=0,0,1
#     while n<max:
#         yield b
#         a,b=b,a+b
#         n+=1
#     return 'done'
# f=fib(6)
# print(next(f))
# print(next(f))
# print(next(f))
# print(next(f))
# def fib():
#     a,b=0,1
#     while True:
#         yield b
#         a,b=b,a+b
# f=fib()
# for i in range(6):
#     print(next(f))

# for i in range(1,10):
#     for j in range(1,i+1):
#         print (j,'*',i,'=',i*j,end=' ')
#     print('\n')

import time,random
# def heapify(arr, node, end):
#     root = node
#     #print(root,2*root+1,end)
#     while True:
#         # 从root开始对最大堆调整
#         child = 2 * root +1  #left child
#         if child  > end:
#             #print('break',)
#             break
#         print("v:",root,arr[root],child,arr[child])
#         print(arr)
#         # 找出两个child中较大的一个
#         if child + 1 <= end and arr[child] < arr[child + 1]: #如果左边小于右边
#             child += 1 #设置右边为大
#         if arr[root] < arr[child]:
#             # 最大堆小于较大的child, 交换顺序
#             tmp = arr[root]
#             arr[root] = arr[child]
#             arr[child]= tmp
#             # 正在调整的节点设置为root
#             #print("less1:", arr[root],arr[child],root,child)
#             root = child #
#             #[3, 4, 7, 8, 9, 11, 13, 15, 16, 21, 22, 29]
#             #print("less2:", arr[root],arr[child],root,child)
#         else:
#             # 无需调整的时候, 退出
#             break
#     #print(arr)
#     print('-------------')
#
# def heap_sort(arr):
#     # 从最后一个有子节点的孩子开始调整最大堆
#     first = len(arr) // 2 -1
#     for i in range(first, -1, -1):
#         heapify(arr, i, len(arr) - 1)
#     #[29, 22, 16, 9, 15, 21, 3, 13, 8, 7, 4, 11]
#     print('--------end---',arr)
#     # 将最大的放到堆的最后一个, 堆-1, 继续调整排序
#     for end in range(len(arr) -1, 0, -1):
#         arr[0], arr[end] = arr[end], arr[0]
#         heapify(arr, 0, end - 1)
#         # print(arr)
# l=[11,78,23,54,2,6,24]
# heap_sort(l)
# print(l)

# def heapify(nums,node,end):
#      #左子树
#     while True:
#         child = node * 2 + 1
#         if child>end:
#             break
#         if child+1<=end and nums[child]<nums[child+1]:
#             child+=1
#         if nums[child]>nums[node]:
#             nums[child],nums[node]=nums[node],nums[child]
#         else:
#             break



# def heapSort(nums):
#     n=len(nums)
#     last=n//2-1
#     for i in range(last,-1,-1):
#         heapify(nums,i,n-1)
#     for end in range(n-1,0,-1):
#         nums[0],nums[end]=nums[end],nums[0]
#         heapify(nums,0,end-1)
# l=[11, 78, 23, 54, 2, 6, 24]
# heapSort(l)
# print(l)

def heap_adjust(L, start, end):
    temp = L[start]

    i = start
    j = 2 * i

    while j <= end:
        if (j < end) and (L[j] < L[j + 1]):
            j += 1
        if temp < L[j]:
            L[i] = L[j]
            i = j
            j = 2 * i
        else:
            break
    L[i] = temp
l=[1,4,2,78,34,23,67]
# heapSort(l)
# print(l)
def merge(l_nums,r_nums):
    l,r=0,0
    res=[]
    while l<len(l_nums) and r<len(r_nums):
        if l_nums[l]<r_nums[r]:
            res.append(l_nums[l])
            l+=1
        else:
            res.append(r_nums[r])
            r+=1
    res+=l_nums[l:]
    res+=r_nums[r:]
    return res


def merge_sort(nums):

    if len(nums)<=1:
        return nums
    mid=len(nums)//2
    l_nums=merge_sort(nums[:mid])
    r_nums=merge_sort(nums[mid:])
    return merge(l_nums,r_nums)
n1=[12,3,6,4,24,57,35]
nums=[45,12,32,4,5,80,14]
n=merge_sort(nums)
print(merge_sort(n1))
print(merge_sort(nums))
# def middleordersort(root):
#     node=root
#     res=[]
#     stack=[]
#     while node or stack:
#         if node:
#             stack.append(node.left)
#             node=node.left
#         else:
#             node=stack.pop()
#             res.append(node.val)
#             node=node.right
def preordersort(root):
    node=root
    res=[]
    stack=[]
    while node or stack:
        if node:
            res.append(node.val)
            stack.append(node.right)
            node=node.left
        else:
            node=stack.pop()
    return res

def postordertraversal(root):
    node=root
    res=[]
    stack=[]
    while node or stack:
        if node:
            res.append(node.val)
            stack.append(node.left)
            node=node.right
        else:
            node=stack.pop()
    return res[::-1]
def levelorder(root):
    if not root:
        return []
    node=root
    res=[]
    queue=[node]
    while queue:
        node=queue.pop(0)
        res.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return res


def adjest(nums):
    return nums==list(set(nums))
# print(adjest([1,5,6,7,8,9]))
# def findDisappearedNumbers(nums):
#     for num in nums:
#         nums[abs(num) - 1] = -abs(nums[abs(num) - 1])
#     res=[]
#     for i in range(len(nums)):
#         if nums[i]>0:
#             res.append(i+1)
#     print(res)
# findDisappearedNumbers([4,3,2,7,8,2,3,1])




# dict1={'a':2,'e':3,'f':8,'d':4}
# print(list(dict1.keys()))
# print(list(dict1.values()))
# print(list(dict1.items()))
# print(sorted(dict1.items()))
# dic2=sorted(dict1.items(),key=lambda kv:(kv[1]))
# print(dic2)
# print(id(dict1),id(dic2))
# print(sorted(dict1.items(),key=lambda kv:(kv[1])))

def countWords(s):
    print('被测字符串为',s)
    if not s:
        return ''
    s=s.replace(',','')
    s=s.replace('.','')
    s = s.replace('\n', '')
    s=s.replace('\xa0',' ')
    print('处理异常字符后字符串为', s)
    word_list=s.split(' ')
    dic={}
    for word in word_list:
        word=word.lower()
        if word in dic:
            dic[word]+=1
        else:
            dic[word]=1
    print('词频统计字典是',dic)
    dic_sorted=sorted(dic.items(), key=lambda kv:(kv[1],kv[0]),reverse=True)
    # dic_sorte= sorted(dict1.items(), key=lambda kv: (kv[1]))
    print('根据value排序后',dic_sorted)
    result=dic_sorted[:3]
    print('前三个单词是',result)
    res=[]
    for i in result:
        res.append(i[0])
    print(res)

# if __name__=='__main__':
#     with open('/Users/wushishi/Python/HarryPotter.txt','r',encoding='utf-8') as f:
#         ss=f.read()
#
#     countWords(ss)
# print('a'*5)
def tuzi(n):

    x=0
    while n%2==0 and x<=n and 0<=(n-3*x)//2<=n:
        print(x,(n-3*x)//2)
        x+=2
# tuzi(12)
def longestConsecutive(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    hash_dict = {}
    ans = 0
    for num in nums:
        if num not in hash_dict:
            left = hash_dict.get(num - 1, 0)
            right = hash_dict.get(num + 1, 0)

            cur_length = 1 + left + right
            if cur_length > ans:
                ans = cur_length
            hash_dict[num] = cur_length
            hash_dict[num - left] = cur_length
            hash_dict[num + right] = cur_length
    return ans
a=longestConsecutive([100,4,200,1,3,2])
print(a)

# def test_a():
#     print('执行测试用例')
#     assert 1==1
#     # assert longestConsecutive([100,4,200,1,3,2])==4
# if __name__=='__main__':
#     pytest.main()

def test_b():
     print("------->test_b")
     assert 0
if __name__ == '__main__':
    pytest.main()