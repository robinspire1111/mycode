import tkinter as tk
import tkinter.font
from tkinter import ttk,messagebox
import time
import json

users = {
         "yzh":{
                "password":"123",
                "count":1000,
                "events":[]
               },
          "admin":{
                "password":"admin",
                "count":10000000,
                "events":[]
               }
         }


# with open("users.txt","w",encoding = "utf-8")as f:
#     content =  json.dumps(users)
#     f.write(content)

def outcome2Text(name,things,value):
    global app
    if value.get() != "":
        users_data = {}
        with open("users.txt","r",encoding = "utf-8") as f:
            users_data = json.loads(f.read())
            data = users_data[name]
            
            if int(value.get()) > data["count"]:
                count = 0
            else:
                count = data["count"] - int(value.get())
                
            count = data["count"] - int(value.get())
            data["count"] = count
            local_time = time.strftime('%y-%m-%d %H:%M:%S')
            thing = "{:>14}{:>20}{:^23}{:^27}\n".format(local_time,things.get(),-int(value.get()),count)
            data["events"].append(thing)
            users_data[name] = data
        with open("users.txt","w",encoding = "utf-8") as f:
            content = json.dumps(users_data)
            f.write(content)
            messagebox.showinfo("记账","记账成功")
            app.entry_money.delete(0,tk.END)

def income2Text(name,things,value):
    global app
    if value.get() != "":
        users_data = {}
        with open("users.txt","r",encoding = "utf-8") as f:
            users_data = json.loads(f.read())
            data = users_data[name]
            count = data["count"] + int(value.get())
            data["count"] = count
            local_time = time.strftime('%y-%m-%d %H:%M:%S')
            thing = "{:>14}{:>20}{:^21}{:^25}\n".format(local_time,things.get(),value.get(),count)
            data["events"].append(thing)
            users_data[name] = data
        with open("users.txt","w",encoding = "utf-8") as f:
            content = json.dumps(users_data)
            f.write(content)
            messagebox.showinfo("记账","记账成功")
            app.entry_money.delete(0,tk.END)
   
def Income2Counter():
    global app
    name = app.name
    app.window.destroy()
    app = Counter(name)
    app.show()
    app.window.mainloop() 

def Counter2Income():
    global app
    name = app.name
    app.window.destroy()
    app = Income(name)
    app.show()
    app.window.mainloop()

def Outcome2Counter():
    global app
    name = app.name
    app.window.destroy()
    app = Counter(name)
    app.show()
    app.window.mainloop() 

def Counter2Outcome():
    global app
    name = app.name
    app.window.destroy()
    app = Outcome(name)
    app.show()
    app.window.mainloop()
    
def Counter2Inqurty():
    global app
    name = app.name
    app.window.destroy()
    app = Inqurty(name)
    app.show()
    app.window.mainloop()
    
def Inqurty2Counter():
    global app
    name = app.name
    app.window.destroy()
    app = Counter(name)
    app.show()
    app.window.mainloop()
    
def login(name,password):
    global app
    m_name = name.get()
    m_password = password.get()
    if m_name in users:
       user_info = users[m_name]
       dict_password = user_info["password"]
       if m_password == dict_password:
         messagebox.showinfo("提示","登陆成功")
         app.window.destroy()
         app = Counter(m_name)
         app.show()
         app.window.mainloop()
       else:
           messagebox.showwarning("警告","密码错误")
    else:
        messagebox.showwarning("警告","用户名不存在")
        
        
class initWindow():
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("快乐记账")
        ww = 450
        wh = 360

        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - ww)/2
        y = (sh - wh)/2
        self.window.geometry("%dx%d+%d+%d"%(ww,wh,x,y))

        self.window.resizable(width = False,height = False)
        
class Login(initWindow):
    def __init__(self):
       super().__init__()
       
       
    def show(self):

        fontstyle = tk.font.Font(family = "微软雅黑",size = 16)
        label_info = tk.Label(self.window,text = "请登录",bg = "lightgreen",
                          font =  fontstyle,borderwidth = 20)
        label_info.pack(fill = tk.X,side = tk.TOP)
        _name = tk.StringVar()
        label_name = tk.Label(self.window,text = "用户名:",font = "微软雅黑")
        label_name.place(relx=0.05,rely = 0.34)
        entry_name = tk.Entry(self.window,width=21,show = None,textvariable = _name
                              ,font = ("宋体",12))
        entry_name.place(relx = 0.2,rely = 0.34)

        _password = tk.StringVar()
        label_password = tk.Label(self.window,text = "密码:",font = "微软雅黑")
        label_password.place(relx=0.09,rely = 0.5)
        entry_password = tk.Entry(self.window,width=21,font = ("宋体",12),show="*",
                                  textvariable = _password)
        entry_password.place(relx = 0.2,rely = 0.5)

        button_inqury = tk.Button(self.window,text = "登录",bg = "lightgreen",width = 6,
                                  command =lambda:login(_name,_password))
        button_inqury.place(relx = 0.6,rely = 0.65)

class Counter(initWindow):
    def __init__(self,name):
        super().__init__()
        self.name = name
        
    def show(self):
        fontstyle = tk.font.Font(family = "微软雅黑",size = 16)
        label_info = tk.Label(self.window,text = "快乐记账",bg = "lightgreen",
                          font =  fontstyle,borderwidth = 20)
        label_info.pack(fill = tk.X,side = tk.TOP)
        income_button = tk.Button(self.window,text = "收入",bg = "lightblue",
                                  width = 10,height = 4,command = Counter2Income)
        income_button.place(relx = 0.05,rely = 0.35)
        income_button = tk.Button(self.window,text = "花销",bg = "lightblue",
                                  width = 10,height = 4,command = Counter2Outcome)
        income_button.place(relx = 0.35,rely = 0.35)
        income_button = tk.Button(self.window,text = "查询",bg = "lightblue",
                                  width = 10,height = 4,command = Counter2Inqurty)
        income_button.place(relx = 0.65,rely = 0.35)
        
class Income(initWindow):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.entry_money = tk.Entry(self.window)
        
       
    def show(self):  
        kind_label = tk.Label(self.window,text = "进账类别:",font = ("微软雅黑",10))
        kind_label.place(relx = 0.05,rely = 0.2)
        
        income_var = tk.StringVar()
        kind_combobox = ttk.Combobox(self.window,textvariable = income_var,
                                     width = 25,font = "微软雅黑")
        kind_combobox["value"] = ("劳务所得","金融理财","他人赠与","遗产继承","奖金")
        kind_combobox.current(0)                              
        kind_combobox.place(relx = 0.25,rely = 0.2)
        
        
        money_label = tk.Label(self.window,text = "金额:",font = ("微软雅黑",10))
        money_label.place(relx = 0.14,rely = 0.3)
        self.entry_money = tk.Entry(self.window,width = 28,font = "微软雅黑")
        self.entry_money.place(relx = 0.25,rely = 0.3)
        button_back = tk.Button(self.window,text = "返回",bg = "lightblue",width = 6,
                                command = Income2Counter)
        button_back.place(relx = 0.2,rely = 0.55)
        button_income = tk.Button(self.window,text = "确定",bg = "lightblue",width = 6,
                                command = lambda:income2Text(self.name,income_var,self.entry_money))
        button_income.place(relx = 0.6,rely = 0.55)

class Outcome(initWindow):
    def __init__(self,name):
        super().__init__()
        self.name = name
        self.entry_money = tk.Entry(self.window)
       
    def show(self):  
        kind_label = tk.Label(self.window,text = "花销类别:",font = ("微软雅黑",10))
        kind_label.place(relx = 0.05,rely = 0.2)
        
        outcome_var = tk.StringVar()
        kind_combobox = ttk.Combobox(self.window,textvariable = outcome_var,
                                     width = 25,font = "微软雅黑")
        kind_combobox["value"] = ("购物","投资","赠与他人","捐赠")
        kind_combobox.current(0)
        kind_combobox.place(relx = 0.25,rely = 0.2)
        
        money_label = tk.Label(self.window,text = "金额:",font = ("微软雅黑",10))
        money_label.place(relx = 0.14,rely = 0.3)
        self.entry_money = tk.Entry(self.window,width = 28,font = "微软雅黑")
        self.entry_money.place(relx = 0.25,rely = 0.3)
        button_back = tk.Button(self.window,text = "返回",bg = "lightblue",width = 6,
                                command = Outcome2Counter)
        button_back.place(relx = 0.2,rely = 0.55)
        
        button_back = tk.Button(self.window,text = "确定",bg = "lightblue",width = 6,
                                command = lambda:outcome2Text(self.name,outcome_var,self.entry_money))
        button_back.place(relx = 0.6,rely = 0.55)
        
        
class Inqurty(initWindow):
    def __init__(self,name):
        super().__init__()
        self.name = name
    def show(self):
        listbox_show = tk.Listbox(self.window,width = 420)
        listbox_show.pack()
        with open("users.txt","r",encoding = "utf-8") as f:
            users_data = json.loads(f.read())
            data = users_data[self.name]["events"]
        first_item =  "{:>16}{:>26}{:^26}{:^26}\n".format("时间","事项","收支","盈余")
        listbox_show.insert("end",first_item)
        for item in data:
            listbox_show.insert("end",item)
        button_back = tk.Button(self.window,text = "返回",bg = "lightblue",width = 6,
                                command = Inqurty2Counter)
        button_back.place(relx = 0.75,rely = 0.75)
app = Login()
app.show()
app.window.mainloop()
