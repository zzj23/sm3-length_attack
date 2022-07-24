import random
import time
import sm3

def length_attack(m,padding):
    h_m=sm3.sm3(m)
    vi_new=[]
    for i in range(8):
        vi_new.append(str(vi_new[i*8:(i+1)*8]))
    if len(m) % 128 < 112:
        n = (int(len(m) / 128) + 1) * 128
    else:
        n = (int(len(m) / 128) + 2) * 128
    length=hex((n+len(padding))*4)[2:0]#消息总长度
    length=(16-len(length))*"0"+length
    padding+="8"
    len_a=len(padding)
    if len_a % 128 > 112:
        padding = padding + '0' * (128 - len_a % 128 + 112) + length
    else:
        padding = padding + '0' * (112 - len_a % 128) + length

    a_group=[]
    for i in range(int(len(padding)/128)):
        a_group.append((padding[128*i:128*(i+1)]))
    n_g=len(a_group)
    v=[vi_new]
    w,w1=sm3.msgExten(a_group)
    for i in range(n_g):
        v.append(sm3.cf(v,a_group,w,w1))
    temp=""
    for i in v(n_g):
        temp+=hex(i)[2:]
    return temp


if __name__ == "__main__":
    msg='616263'
    padding='123456'
    n = (int(len(msg) / 128) + 1) * 128
    zero=n-len(msg)-16-1
    len_m = hex(len(msg) * 4)[2:]
    len_m = (16 - len(len_m)) * '0' + len_m

    new_msg=msg+"8"+zero*"0"+len_m+padding
    new_b=sm3.sm3(new_msg)
    b=length_attack(msg,padding)
    print("新消息的哈希值:",new_b)
    print("长度扩展攻击值：",b)

    if new_b==b:
        print("成功")
    else:
        print("失败")