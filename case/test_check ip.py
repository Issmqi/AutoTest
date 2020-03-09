
import pytest

def check_ip(str):
    l=str.split(".")
    print(l)
    if len(l)==4:
        flag = True
        for i in l:
            print(i)
            if i.isdigit():
                n=int(i)
                if n>=0 and n <256:
                    pass
                else:
                    print('不在0-255之间')
                    flag=False

            else:
                print('不全部由数字组成')
                flag=True

        return flag

    else:
        print('字节长度不为4节')
        return False


# check_ip('111.222.255.223')
data=['123','123.1ab.234.sddf','123.123.111.222.111','111.123.256.111','111.222.255.223']

@pytest.mark.parametrize('param',data)
def test_check_ip(param):
    assert check_ip(param)


if __name__ == '__main__':
    pytest.main()





# check_ip("123.12.45")

