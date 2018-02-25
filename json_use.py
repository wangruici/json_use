#!/usr/bin/python3.5
# -*- UTF-8 -*-
import json
import os
import io
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex,a2b_hex

hard_path="/home/ruici/workspace/Notes/account/accounts/accounts.txt"
class Encryptor:
    def __init__(self,key,absolute_path,after_encrypt_path):
        self.bpath=absolute_path
        self.apath=after_encrypt_path

        self.__key_size__=16
        self.__bin_key__=(key[0:self.__key_size__]).encode("utf-8")
        #constant
        self.__encrypt_mode__=AES.MODE_CFB
        self.__bufsize__=1024*2
        self.__descriptor_mode__="rb"
        self.__iv__=Random.new().read(AES.block_size)
        self.__des_bufsize__=0
    def encrypt_file(self):
        before=open(self.bpath,self.__descriptor_mode__,self.__des_bufsize__)
        after=open(self.apath,"wb")
        after.write(self.__iv__)
        cipher=AES.new(self.__bin_key__,self.__encrypt_mode__,self.__iv__)
        while True:
            plaintext=before.read(self.__bufsize__)
            if not plaintext:
                break
            en_text=cipher.encrypt(plaintext)
            after.write(en_text)
        after.close()
        before.close()
    def decrypt_file(self):
        before=open(self.bpath,"wb")
        after=open(self.apath,self.__descriptor_mode__,self.__des_bufsize__)
        after.read(AES.block_size)
        cipher=AES.new(self.__bin_key__,self.__encrypt_mode__,self.__iv__)
        while True:
            en_text=after.read(self.__bufsize__)
            if not en_text:
                break
            plaintext=cipher.decrypt(en_text)
            before.write(plaintext)
        after.close()
        before.close()
    def get_iv(self):
        after=open(self.apath,self.__descriptor_mode__,self.__des_bufsize__)
        self.__iv__=after.read(AES.block_size)
        after.close()
    def decrypt(self):
        after=open(self.apath,self.__descriptor_mode__,self.__des_bufsize__)
        after.read(AES.block_size)
        cipher=AES.new(self.__bin_key__,self.__encrypt_mode__,self.__iv__)
        plaintext=b""
        while True:
            en_text=after.read(self.__bufsize__)
            if not en_text:
                break
            plaintext=plaintext+cipher.decrypt(en_text)
        after.close()
        return plaintext
    def encrypt(self,text):
        en_text=self.__iv__
        cipher=AES.new(self.__bin_key__,self.__encrypt_mode__,self.__iv__)
        en_text=en_text+cipher.encrypt(text)
        return en_text




class JSoperator:
    def __init__(self,s_data):
        self.pwd="/"  #指明当前路径
        self.data=json.loads(s_data) #必须是符合规定的数据
        self.now_location=self.data
    def exists(self,path):
        flag=True
        if path[0]=="/":
            p_block=path.split("/")
            del p_block[0]
            if path[-1]=="/":
                del p_block[-1]
            dict_location=self.data#python的字典的变量名类似一个引用，只是绑定
            count=0
            for item in p_block:
                count=count+1
                if item in dict_location:
                    if type(dict_location[item])==dict:
                        dict_location=dict_location[item]
                    elif count==len(p_block):
                        flag=True
                    else:
                        flag=False
                        break
                else:
                    flag=False
                    break
        elif path[0]==".":
            p_block=path.split("/")
            del p_block[0]
            if path[-1]=="/":
                del p_block[-1]
            dict_location=self.now_location#python的字典的变量名类似一个引用，只是绑定
            count=0
            for item in p_block:
                count=count+1
                if item in dict_location:
                    if type(dict_location[item])==dict:
                        dict_location=dict_location[item]
                    elif count==len(p_block):
                        flag=True
                    else:
                        flag=False
                        break
                else:
                    flag=False
                    break
        else:
            if path[-1]=="/":
                del p_block[-1]
            dict_location=self.now_location#python的字典的变量名类似一个引用，只是绑定
            count=0
            for item in p_block:
                count=count+1
                if item in dict_location:
                    if type(dict_location[item])==dict:
                        dict_location=dict_location[item]
                    elif count==len(p_block):
                        flag=True
                    else:
                        flag=False
                        break
                else:
                    flag=False
                    break
        return flag
    #相对路径(rpath)一定要以"."开头
    def ls_rpath(self,rpath):
        if not self.exists(rpath):
            return None
        else:
            dict_location=self.now_location
            p_block=rpath.split("/")
            del p_block[0]
            if (len(p_block)>0)and(p_block[-1]==""):
                del p_block[-1]
            for item in p_block:
                if item=="":
                    continue
                else:
                    dict_location=dict_location[item]
        result=""
        if type(dict_location)==dict:
            for item in dict_location.keys():
                result=result+" "+item
        else:
            result=result+" "+dict_location
        return result
    #绝对路径(apath)一定要以"/"开头
    def ls_apath(self,path):
        temp_now=self.now_location
        self.now_location=self.data
        path="."+path
        result=self.ls_rpath(path)
        self.now_location=temp_now
        return result
    def ls_up(self):
        p_block=self.pwd.split("/")
        del p_block[0]
        if len(p_block)>0:
            del p_block[-1]
        ob_path=""
        for item in p_block:
            ob_path=ob_path+"/"+item
        return self.ls_apath(ob_path)
    def ls(self,path):
        if path[0]=="." and len(path)>=2 and path[1]==".":
            return self.ls_up()
        elif path[0]==".":
            return self.ls_rpath(path)
        elif path[0]=="/":
            return self.ls_apath(path)
        else:
            return False
    #一定要注意，最后一个位置上必须是一个文件夹（字典），不能是一个文件，否则出错
    #相对路径一定要以"."开头
    #只能向下
    def cd_rpath_down(self,rpath):
        if not self.exists(rpath):
            return False
        else:
            p_block=rpath.split("/")
            del p_block[0]
            if (len(p_block)>0) and (p_block[-1]==""):
                del p_block[-1]
            for item in p_block:
                if item=="":
                    continue
                else:
                    if(self.pwd[-1]=="/"):
                        self.pwd=self.pwd+item
                    else:
                        self.pwd=self.pwd+"/"+item
                    self.now_location=self.now_location[item]
        return True
    def cd_apath(self,path):
        path="."+path
        self.now_location=self.data
        self.pwd="/"
        return self.cd_rpath_down(path)
    def cd_up(self):
        p_block=self.pwd.split("/")
        del p_block[0]
        if len(p_block)>0:
            del p_block[-1]
        ob_path=""
        for item in p_block:
            ob_path=ob_path+"/"+item
        self.cd_apath(ob_path)
        return True
    def cd(self,path):
        if path[0]=="." and len(path)>=2 and path[1]==".":
            return self.cd_up()
        elif path[0]==".":
            return self.cd_rpath_down(path)
        elif path[0]=="/":
            return self.cd_apath(path)
        else:
            return False
    def _mkdir_now(self,name):
        self.now_location[name]={}
    def mkdir(self,path,dir_name):
        temp_pwd=self.pwd
        self.cd(path)
        self._mkdir_now(dir_name)
        self.cd(temp_pwd)
    def _touch_now(self,key,value):
        self.now_location[key]=value
    def touch(self,path,key,value):
        temp_pwd=self.pwd
        self.cd(path)
        self._touch_now(key,value)
        self.cd(temp_pwd)
    def _rm_now(self,key):
        del self.now_location[key]
    def rm(self,path,key):
        temp_pwd=self.pwd
        self.cd(path)
        self._rm_now(key)
        self.cd(temp_pwd)
    def _show_now(self):
        return json.dumps(self.now_location,sort_keys=True,\
                          indent=4,separators=(",",":"))
    def show_all(self):
        return json.dumps(self.data,sort_keys=True,\
                          indent=4,separators=(",",":"))
    def show(self,path):
        temp_pwd=self.pwd
        self.cd(path)
        result=self._show_now()
        self.cd(temp_pwd)
        return result
    def save(self,path):
        with open(path,"w") as f:
            f.write(self.show_all())
    def encrypt_save(self,path,key):
        en_file=Encryptor(key,path,path)
        en_text=en_file.encrypt(self.show_all())
        with open(path,"wb") as f:
            f.write(en_text)
    def locateto(self,path):
        result=self.data
        p_block=path.strip("/").split("/")
        if len(p_block)==0:
            return self.data
        elif len(p_block)==1 and p_block[0]=="":
            return self.data
        for item in p_block:
            result=result[item]
        return result
    def isDict(self,path):
        p_block=path.strip("/").split("/")
        if len(p_block)==1 and p_block[0]=="":
            return True
        k=self.data
        for item in p_block:
            k=k[item]
        if type(k)==dict:
            return True
        else:
            return False
#绝对路径
    def isFile(self,path):
        return not self.isDict(path)
    def find_key(self,path,key):
        #path是绝对路径而且是文件夹,key是文件或文件夹
        #返回一个路径列表
        result_lst=[]
        item_queue=[(path,self.locateto(path))]
        while(len(item_queue)>0):
            front=item_queue[0]
            del item_queue[0]
            for item in front[1]:
                if(front[0]=="/"):
                    p=front[0]+item
                else:
                    p=front[0]+"/"+item
                if item==key:
                    result_lst.append(p)
                elif type(front[1][item])==dict:
                    item_queue.append((p,front[1][item]))
                else:
                    pass
        return result_lst
    def find_key_value(self,path,key,value):
        lst=self.find_key(path,key)
        result_lst=[]
        for item in lst:
            if self.isDict(item):
                pass
            elif not self.locateto(item)==value:
                pass
            else:
                result_lst.append(item)
        return result_lst
    def include_key(self,path,key):
        lst=self.find_key(path,key)
        result_lst=[]
        for item in lst:
            path_lst=item.strip("/").split("/")
            p=merge(path_lst[:-1])
            result_lst.append(p)
        return result_lst
    def include_key_value(self,path,key,value):
        lst=self.find_key_value(path,key,value)
        result_lst=[]
        for item in lst:
            path_lst=item.strip("/").split("/")
            p=merge(path_lst[:-1])
            result_lst.append(p)
        return result_lst

def find_input_check(cmd_lst,cmd_len):
    #错误1：参数不全
    if cmd_len<3:
        return 1
    #错误2：文件不存在
    elif not jos.exists(cmd_lst[1]):
        return 2
    elif cmd_len==3:
        return -1
    else:
        return -2
def ls_check(jos,cmd,len_cmd):
    pass
def find_output(jos,result,mode):
    if len(result)<=0:
        return False
    elif mode==-1 or mode==-2:
        base=["ls","-a"]
        base.extend(result)
        s=ls_check(jos,base,len(base))
        return s
    else:
        return None
def find_check(jos,cmd_lst,cmd_len):
    if find_input_check(cmd_lst,cmd_len)>0:
        return False
    elif find_input_check(cmd_lst,cmd_len)==0:
        return None
    else:
        if find_input_check(cmd_lst,cmd_len)==-1:
            result=jos.include_key(cmd_lst[1],cmd_lst[2])
            return find_output(jos,result,-1)
        else:
            result=jos.include_key_value(cmd_lst[1],cmd_lst[2],cmd_lst[3])
            return find_output(jos,result,-2)



def parser_cmd(cmd):
    lst=cmd.strip(" ").split(" ")
    return lst
 
#test_path="./accounts.txt"#测试用
##########################################    
key=input("Please input key:")
file_en=Encryptor(key,hard_path,hard_path)
file_en.get_iv()
s_data=file_en.decrypt().decode()

jos=JSoperator(s_data)
###########################################
#必须是绝对路径
def merge(lst):
    if len(lst)<=0:
        result="/"
    elif len(lst)==1 and lst[0]=="":
        result="/"
    else:
        result=""
        for item in lst:
            result=result+"/"+item
    return result

def compute_path(nowpath,s):
    #不考虑文件是否存在
    if s[0]=="/":
        result=s
        return result
    nowpath_lst=nowpath.strip("/").split("/")
    s_lst=s.strip("/").split("/")
    for i in range(0,len(s_lst),1):
        if s_lst[i]==".":
            continue
        elif s_lst[i]=="..":
            if len(nowpath_lst)>=1:
                del nowpath_lst[-1]
            else:
                nowpath_lst=[]
                break
        else:
            nowpath_lst.append(s_lst[i])
    result=""
    for item in nowpath_lst:
        if item=="":
            continue
        result=result+"/"+item
    if result=="":
        result="/"
    return result
#一定要是绝对路径
def exists_lst(jos,path_lst):
    if (len(path_lst)==0) or (len(path_lst)==1 and path_lst[0]==""):
        return True
    else:
        path=""
        for item in path_lst:
            path=path+"/"+item
        return jos.exists(path)
def isDict_lst(jos,p_block):
    if len(p_block)==1 and p_block[0]=="":
        return True
    k=jos.data
    for item in p_block:
        k=k[item]
    if type(k)==dict:
        return True
    else:
        return False
def isFile_lst(jos,path):
    return not isDict_lst(jos,path)
#前提是路径已经存在才可以调用这个函数
def isDict(jos,path):
    p_block=path.strip("/").split("/")
    if len(p_block)==1 and p_block[0]=="":
        return True
    k=jos.data
    for item in p_block:
        k=k[item]
    if type(k)==dict:
        return True
    else:
        return False
#绝对路径
def isFile(jos,path):
    return not isDict(jos,path)
#绝对路径
def locateto(jos,path):
    result=jos.data
    p_block=path.strip("/").split("/")
    for item in p_block:
        result=result[item]
    return result
def exists_check(jos,cmd,len_cmd):
    return False
def ls_check(jos,cmd,len_cmd):
    if len_cmd==1:
        result=jos.ls(".")
    elif len_cmd==2 and cmd[1]=="-a":
        result=jos._show_now()
    elif not cmd[1]=="-a":
        result=""
        for i in range(1,len_cmd):
            result=result+cmd[i]+":"+"\n"
            path=compute_path(jos.pwd,cmd[i])
            if not jos.exists(path):
                result=result+"Not exists.\n"
            elif isFile(jos,path):
                result=result+locateto(jos,path)+"\n"
            else:
                result=result+jos.ls(path)+"\n"
            result=result+"-------------------------------------------------------------\n"
    else:
        result=""
        for i in range(2,len_cmd):
            result=result+cmd[i]+":"+"\n"
            path=compute_path(jos.pwd,cmd[i])
            if not jos.exists(path):
                result=result+"Not exists.\n"
            elif isFile(jos,path):
                result=result+locateto(jos,path)+"\n"
            else:
                result=result+jos.show(path)+"\n"
            result=result+"-------------------------------------------------------------\n"
    return result
def cd_check(jos,cmd,len_cmd):
    if len_cmd<2:
        return False
    else:
        result=""
        path=compute_path(jos.pwd,cmd[1])
        if not jos.exists(path):
            result="Not exists.\n"
        elif isFile(jos,path):
            result="It's a File.\n"
        else:
            jos.cd(path)
            result=""
        return result
def mkdir_check(jos,cmd,len_cmd):
    if len_cmd<2:
        return False
    elif len_cmd==2 and cmd[1]=="-f":
        return False
    else:
        if cmd[1]=="-f":
            for i in range(2,len_cmd):
                path=compute_path(jos.pwd,cmd[i])
                path_lst=path.strip("/").split("/")
                if len(path_lst)<=0 or path_lst[0]=="":
                    return False
                else:
                    if not exists_lst(jos,path_lst[:-1]):
                        return False
                    else:
                        jos.mkdir(merge(path_lst[:-1]),path_lst[-1])
            return True
        else:
            for i in range(1,len_cmd):
                path=compute_path(jos.pwd,cmd[i])
                path_lst=path.strip("/").split("/")
                if len(path_lst)<=0 or path_lst[0]=="":
                    return False
                else:
                    if exists_lst(jos,path_lst):
                        return False
                    elif not exists_lst(jos,path_lst[:-1]):
                        return False
                    else:
                        jos.mkdir(merge(path_lst[:-1]),path_lst[-1])
            return True
        

def touch_check(jos,cmd,len_cmd):
    if len_cmd<=1:
        return False
    elif len_cmd==2 and cmd[1]=="f":
        return False
    else:
        if cmd[1]=="-f":
            for i in range(2,len_cmd):
                item=cmd[i].split(":",1)#只能分裂一次
                if len(item)<2:
                    return False
                path=compute_path(jos.pwd,item[0])
                path_lst=path.strip("/").split("/")
                if len(path_lst)<=0 or path_lst[0]=="":
                    return False
                else:
                    #如果路径不存在，错误
                    if not exists_lst(jos,path_lst[:-1]):
                        return False
                    #如果存在路径，但是是文件
                    elif isFile_lst(jos,path_lst[:-1]):
                        return False
                    else:
                        jos.touch(merge(path_lst[:-1]),path_lst[-1],item[1])
            return True
        else:
            for i in range(1,len_cmd):
                item=cmd[i].split(":",1)
                if len(item)<2:
                    return False
                path=compute_path(jos.pwd,item[0])
                path_lst=path.strip("/").split("/")
                if len(path_lst)<=0 or path_lst[0]=="":
                    return False
                else:
                    #如果存在文件（无论是文件还是文件夹），错误
                    if exists_lst(jos,path_lst):
                        return False
                    #不存在，但是这个路径不存在，错误
                    elif not exists_lst(jos,path_lst[:-1]):
                        return False
                    #路径存在但是不是一个文件夹
                    #错误
                    elif isFile_lst(jos,path_lst[:-1]):
                        return False
                    else:
                        jos.touch(merge(path_lst[:-1]),path_lst[-1],item[1])
            return True
def rm_check(jos,cmd,len_cmd):
    #不管是什么都可以直接删除
    if len_cmd<=1:
        return False
    else:
        for i in range(1,len_cmd):
            path=compute_path(jos.pwd,cmd[i])
            if not jos.exists(path):
                return False
            else:
                path_lst=path.strip("/").split("/")
                if len(path_lst)<=0:
                    return False
                elif len(path_lst)==1 and path_lst[0]=="":
                    return False
                elif len(path_lst)==1:
                    jos.rm("/",path_lst[0])
                else:
                    jos.rm(merge(path_lst[:-1]),path_lst[-1])
        return True
                    

def show_all_check(jos,cmd,len_cmd):
    if len_cmd>1:
        return False
    else:
        return jos.show_all()

def show_check(jos,cmd,len_cmd):
    return False

def save_check(jos,cmd,len_cmd):
    if len_cmd<=1:
        jos.encrypt_save(hard_path,key)
        return True
    elif len_cmd==2 and cmd[1]=="-default":
        jos.save(hard_path)
        return True
    elif len_cmd==2 and cmd[1]=="-encrypt":
        jos.encrypt_save(hard_path,key)
        return True
    elif cmd[1]=="-encrypt":
        for i in range(2,len_cmd):
            try:
                jos.encrypt_save(hard_path,key)
            except:
                return False
        return True
    else:
        for i in range(1,len_cmd):
            try:
                jos.save(cmd[i])
            except:
                return False
        return True
        
cmd_dict={"exists":jos.exists,"ls":jos.ls,"cd":jos.cd,\
            "mkdir":jos.mkdir,"touch":jos.touch,"rm":jos.rm,\
            "show_all":jos.show_all,"show":jos.show,"save":jos.save}
cmd_check={"exists":exists_check,"ls":ls_check,"cd":cd_check,\
            "mkdir":mkdir_check,"touch":touch_check,"rm":rm_check,\
            "show_all":show_all_check,"show":show_check,"save":save_check,"find":find_check}
#测试时关闭
###########################################################################
while True:
    cmd=input(jos.pwd+"$")
    cmd_lst=parser_cmd(cmd)
    cmd_len=len(cmd_lst)
    if cmd_lst[0] in cmd_check:
        result=cmd_check[cmd_lst[0]](jos,cmd_lst,cmd_len)
        if result==False or result==None:
            print("Wrong\n")
        elif result==True:
            print("")
        else:
            print(result)
    else:
        if cmd_lst[0]=="q!":
            break
        else:
            print("Not Found")
