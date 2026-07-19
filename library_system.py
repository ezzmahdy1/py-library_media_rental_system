from rich.box import ROUNDED
from rich.console import Console, JustifyMethod
from rich.panel import Panel
from rich.table import Table
import os
import re
from datetime import datetime
import sys
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
console=Console()


def clear_console():
    print('\033[2J\033[H')

####################################################################################### Items classes and functs

class Item:
    """ the parent class of items """
    def __init__(self,_title,_id,_total_copies,_creator,checked_out):
        self.title=_title
        self.i_d=_id                        #id fromatting for items the first digit is its type then a space then its year release date
        self.total_copies=int(_total_copies)     #then a space and then a special 3digit random number           
        self.creator=_creator
        self.no_checkedout=checked_out
    

class Book(Item):            #1
    def __init__(self,_title,_id,_total_copies,_creator,checked_out=0):
        super().__init__(_title,_id,_total_copies,_creator,checked_out)
        self.loanperiod="14 days"
        self.latefee="5 pounds per day"

class DVD(Item):            #2
    
    def __init__(self,_title,_id,_total_copies,_creator,checked_out=0):
        super().__init__(_title,_id,_total_copies,_creator,checked_out)
        self.loanperiod="7 days"
        self.latefee="20 pounds per day"

class Game(Item):          #3
    
    def __init__(self,_title,_id,_total_copies,_creator,checked_out=0):
        super().__init__(_title,_id,_total_copies,_creator,checked_out)
        self.loanperiod="30 days"
        self.latefee="50 pounds per day"

def item_read():
    """funct responsible for reading items from database"""
    console.print('loading...',style='bold',justify='center')
    
    try :
        file=open("items.txt",'r')
        items={}
        for line in file:
            if len(line)<2:
                continue
            t_itle=re.search(r'"([^"]*)"',line).group(1)
            id__=re.search(r'\d\s\d{4}\s\d{3}',line).group()
            tot_cpy=re.search(r':(\d+)',line).group(1)
            creat_or=re.search(r'made by ([^.]+)',line).group(1)

            if(id__[0]=='1'):
                items.update({id__:Book(t_itle,id__,tot_cpy,creat_or)})
            elif(id__[0]=='2'):
                items.update({id__:DVD(t_itle,id__,tot_cpy,creat_or)})
            elif(id__[0]=='3'):
                items.update({id__:Game(t_itle,id__,tot_cpy,creat_or)})
        file.close()
        clear_console()
        return items
    except FileNotFoundError:
        file=open("items.txt",'w')
        file.close()
        items={}
        return items

def search(searh_in,items,mode,fil):
    """  search for items search_in is the input to search for   """
    console.print('loading...',style='bold',justify='center')
    srch={} 
    if fil=='1':
        if mode=='1':
            for _id,item in items.items():
                if re.search(searh_in.upper(),item.title.upper())!=None and item.total_copies-item.no_checkedout>0:
                    srch[_id]=item
        if mode=='2':
            for _id,item in items.items():
                if item.i_d.startswith(searh_in) and item.total_copies-item.no_checkedout>0:
                    srch[_id]=item
        if mode=='3':
            for _id,item in items.items():
                if re.search(searh_in.upper(),item.creator.upper())!=None and item.total_copies-item.no_checkedout>0:
                    srch[_id]=item
    else:
       if mode=='1':
           for _id,item in items.items():
               if re.search(searh_in.upper(),item.title.upper())!=None:
                   srch[_id]=item
       if mode=='2':
           for _id,item in items.items():
               if item.i_d.startswith(searh_in):
                   srch[_id]=item
       if mode=='3':
           for _id,item in items.items():
               if re.search(searh_in.upper(),item.creator.upper())!=None:
                    srch[_id]=item
    clear_console()
    return srch

####################################################################################### Member classes and functs

class Member:
    """  the parent class of member classes """
    def __init__(self,_name,_ID,_borrowed,_datejoined,_pendingfees,_status,_perfees,_runfees):
        self.name=_name
        self.ID=_ID
        self.borrowed=_borrowed
        self.date_joined=_datejoined
        self.pending_fees=_pendingfees
        self.status=_status
        self.per_fees=_perfees
        self.run_fees=_runfees

class Student(Member):
    def __init__(self, _name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees):
        super().__init__(_name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees)
        self.borrow_lmt=3

class Staff(Member):
    def __init__(self, _name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees):
        super().__init__(_name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees)
        self.borrow_lmt=5

class Vip(Member):
    def __init__(self, _name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees):
        super().__init__(_name, _ID, _borrowed, _datejoined,_pendingfees,_status,_perfees,_runfees)
        self.borrow_lmt=10

def member_read(items):
    """ the funct responsible for reading member info from database """
    try :
        file=open("members.txt",'r')
        members={}
        borrowed_items=[]
        for line in file:
            if len(line)<2:
                continue
            borrowed_items=[]
            name=re.search(r'"([^"]*)"',line).group(1)
            ID=re.search(r'ID:\ *?(\d{5})',line).group(1)
            borrowed=re.search(r'\(([^)]*)\)',line).group(1).split('/')
            for item in borrowed:
                i=item.strip().split(',')
                try: 
                    items[i[0].strip()].no_checkedout+=1
                    borrowed_items.append([i[0],i[1]])
                except KeyError:
                    pass
            datejoined=re.search(r'\d{4}-\d.-\d.',line).group()
            per_fees=re.search(r'fees:\ +?(\d+)P?(\d+)?',line).group(1)
            run_fees=re.search(r'fees:\ +?(\d+)P?(\d+)?',line).group(2)
            fees=str(int(per_fees)+int(run_fees))
        
        
            if(ID[0]=='1'):
                if int(fees)>500:
                    status="suspended"
                else:
                    status="active"
                members.update({ID:Student(name,ID,borrowed_items,datejoined,fees,status,per_fees,run_fees)})
            elif(ID[0]=='2'):
                if int(fees)>500:
                    status="suspended"
                else:
                    status="active"
                members.update({ID:Staff(name,ID,borrowed_items,datejoined,fees,status,per_fees,run_fees)})
            elif(ID[0]=='3'):
                if int(fees)>500:
                    status="suspended"
                else:
                    status="active"
                members.update({ID:Vip(name,ID,borrowed_items,datejoined,fees,status,per_fees,run_fees)})

        file.close()
        return members
    except FileNotFoundError:
        file=open("members.txt",'w')
        file.close()
        members={}
        return members

def search_member(members):
    """ search for a member """
    srch={}
    while True:
        console.print(Panel("1.name\t2.id"),justify='center')
        opt=input().strip()
        if opt=='1':
            name=console.input('please enter the name ')
            console.print('loading...',style='bold',justify='center')
            for id_,member in members.items():
                if member.name.upper().startswith(name.upper()):
                    srch[id_]=member
            break


        elif opt=='2':
            id_srch=console.input('please eneter the id ')
            try:
                members[id_srch]
                console.print('loading...',style='bold',justify='center')
                for id_,member in members.items():
                    if id_==id_srch:
                        srch[id_]=member
                break

            except KeyError:
                pass

        else:
            console.print("Error:invalid option please try again",style='bold red')
    clear_console()
    return srch

def join_borrowed(member):
    """ generate a string for a specific member """
    x=[]
    sen=''
    for list_ in member.borrowed:
        x.append(','.join(list_))
    sen='/'.join(x)
    x=None
    return sen 

#######################################################################################   #some imp functs

def delay(timein_seconds):
    """ delay the code for a period of time """
    t=datetime.now().second
    while datetime.now().second-t<timein_seconds:
        pass



def item_table(it):
    """ display the details of it which is supposed to be a dict {id of item:item object}  """
    table= Table(show_lines=True)
    table.add_column('ID',justify='center')
    table.add_column('title',justify='center')
    table.add_column('total copies',justify='center')
    table.add_column('available in store',justify='center')
    table.add_column('creator',justify='center')

    for item_id,item in it.items():
        table.add_row(item_id,item.title,str(item.total_copies),str((item.total_copies-item.no_checkedout)),item.creator)

    console.print(table,justify='center')

def member_table(mem):
    """ display the details of mem which is supposed to be a dict {id of member:member object}  """
    table= Table(show_lines=True)
    table.add_column('ID',justify='center')
    table.add_column('name',justify='center')
    table.add_column('date joined',justify='center')
    table.add_column('borrowed items',justify='center')
    table.add_column('pending fees',justify='center')
    table.add_column('confirmed fees',justify='center')
    table.add_column('status',justify='center')

    for mem_id,member in mem.items():
        table.add_row(mem_id,member.name,member.date_joined,join_borrowed(member),member.pending_fees,member.per_fees,member.status)

    console.print(table,justify='center') 


def fees_calc():
    """ calculate the pending fees of all members and stores them in database   """
    items=item_read()
    members=member_read(items)

    for id_,member in members.items():
        member.run_fees=0
        for list_ in member.borrowed:
            if -datetime.fromisoformat(list_[1]).toordinal()+datetime.now().toordinal()>7:
                member.run_fees+=50*(-datetime.fromisoformat(list_[1]).toordinal()+datetime.now().toordinal()-7)
                
    file=open('members.txt','w')
    for iD_,member in members.items():
        s=join_borrowed(member)
        file.write(f'name: "{member.name.title().strip()}" ID:{member.ID} date joined: {member.date_joined} borrowed: ({s}) pending fees: {member.per_fees}P{member.run_fees}\n')
    file.close()

def fees_calc_ind(member_borrowed_list):
    """ calculate individual fees for a member """
   
    if -datetime.fromisoformat(member_borrowed_list[1]).toordinal()+datetime.now().toordinal()>7:
        return str(50*(-datetime.fromisoformat(member_borrowed_list[1]).toordinal()+datetime.now().toordinal()-7))            
    else:
        return '0'

def filewrite_item(items,sentence):
    """ funct that stores items dict in database """ 

    console.print('loading...',justify='center')
    file=open('items.txt','w')
    for key,value in items.items():
        file.write(f'{value.i_d} "{value.title.title()}" total copies:{value.total_copies} made by {value.creator.capitalize()} .\n')
    file.close()
    console.print(f'the item/s were {sentence} succesfuly press enter to continue',style='bold green',justify='center')
    input()

def filewrite_member(members,sentence):
    """ funct that stores items dict in database """ 

    file=open('members.txt','w')
    for iD_,member in members.items():
        s=join_borrowed(member)
        file.write(f'name: "{member.name.title().strip()}" ID:{member.ID} date joined: {member.date_joined} borrowed: ({s}) pending fees: {member.per_fees}P{member.run_fees}\n')
    file.close()
    console.print(f"the member's info was {sentence} succesfully press enter to continue",style='bold green',justify='center')
    input()

###################################################################################################################################### menu functs

def add_item():     
    """  input -> database  """
    no=0
    clear_console()
    while True: #entry input and validation 
        no_=console.input('enter number of items to be added').strip()
        try:
            no_=int(no_)
            break
        except ValueError:
            console.print("error:invalid number please try again",style='bold red')
    while no!=no_: #added items input and validation and storing in data base 
        while True: 
            ans=console.input('please enter (title-id-total copies-creator )').strip().split('-')
            if len(ans)!=4:
                console.print('Error: invalid entry please try again ',style='bold red')
            elif re.search(r'\d\s\d{4}\s\d{3}',ans[1])==None:
                console.print('Error: invalid ID please try again ',style='bold red')
            elif re.search(r'(\d+)',ans[2])==None:
                console.print("Error: invalid copies number please try again ",style='bold red')
            else:
                break

        file=open('items.txt','a')
        file.write(f'\n{ans[1].strip()} "{ans[0].strip().title()}" total copies:{ans[2].strip()} made by {ans[3].strip()} .')
        file.close()
        no=no+1  
        console.print('the item/s were added succesfuly press enter to continue',style='bold green',justify='center')
        input()
        clear_console()


        """   database->stored as dict (items)->input->database   """

def remove_item(items):
    """   stored valuefrom data base (items) + input -> action -> database   """
    while True: #id input and validation
            id_item=console.input("enter the item's id").strip()
            try: 
                items[id_item.strip()]
                no=int(console.input('please enter number of copies to be removed').strip())

                if (items.get(id_item).total_copies-items.get(id_item).no_checkedout-no)<0:
                    console.print("Error:action isnt available copies available in store aren't sufficient",style='bold red',justify='center')
                        
                else:
                    break
            except KeyError:
                console.print("Error:invalid id please try again",style='bold red')
            except ValueError:
                console.print("Error:invalid number",style='bold red')

    items.get(id_item).total_copies-=no  #action and validation
    if items.get(id_item).total_copies-items.get(id_item).no_checkedout==0 and items.get(id_item).no_checkedout==0:
        console.print("do you want to remove the item entirely y/n",style='bold white',justify='center')
        while True:
            a=input().strip()
            if a=='y':
                del items[id_item]
                break
            elif a=='n':
                items[id_item].total_copies=0
                break
            else:
                console.print("Error:invalid number",style='bold red')

    filewrite_item(items,'removed') #storing in database
    clear_console()

def update_item(items):
    """  stored valuefrom data base (items) + input -> action -> database   """
    while True:#id input and validation 
        id_item=console.input("enter the item's id ").strip()
        try:
           items[id_item]
           break
        except KeyError:
            console.print("invalid id please try again !",style='bold red') 
        
    console.print(Panel ("1.title   2.total copies     3.creator"),justify='center')
    while True: #action and validation 
        a=input().strip()
        if a=='1':
            items[id_item].title=console.input("enter the title ").strip()
                        
            break
        elif a=='2':
            while True:
                try:
                    num=int(console.input('enter the new count ').strip())
                    break
                except ValueError:
                    console.print("Error:invalid number",style='bold red')
            items[id_item].total_copies=num
                        
            break
        elif a=='3':
            items[id_item].creator=console.input("enter the creator ").strip()
                       
            break

        else :
            console.print("Error:invalid option please try again",style='bold red') 
                
    filewrite_item(items,"updated") #storing in database

    clear_console()

def searchitem(items):
    """  stored valuefrom data base (items) + input -> action -> display  """
    console.print(Panel ("1.title   2.id     3.creator",title='search by'),justify='center')
    while True: #mode selection and validation 
        mode=input().strip()
        if mode!='1' and mode!='2' and mode!='3':
            console.print("Error:invalid option please try again",style='bold red')
        else:
            break

    console.print(Panel ("1.avilable in store  2.None ",title='filters'),justify='center')
    while True:#filter selection and validation 
        fil=input().strip()
        if fil!='1' and fil!='2':
            console.print("Error:invalid option please try again",style='bold red')
        else:
            break
                
    while True: #search input and validation 
        i=console.input('enter your search ').strip()
        if mode=='2':
            try:
                items[i]
                break
            except KeyError:
                console.print("Error:invalid id fromat please try again",style='bold red')
        else:
            break

    item_table(search(i,items,mode,fil)) #action and displaying
    console.print('press enter to continue',justify='center')
    input()
##########################################################################
def add_member():
    """  input -> database   """
    while True: #number of members to be added input and validation 
        try:
            no_=int(input('please enter number of members to be added ').strip())
            counter=0
            break
        except ValueError:
            console.print("Error:invalid number please try again",style='bold red')
                    
    while counter!=no_:  
        console.print("please enter the member's info (name-id)")
        while True: #member info input and validation 
            try:
                info=input().split('-')
                if len(info)!=2:
                    console.print("Error:invalid entry please try again",style='bold red')
                if re.search(r'(^\d{5}$)',info[1].strip())==None:
                    console.print("Error:invalid id please try again",style='bold red')
                else:
                    break
            except :
                pass

        file=open('members.txt','a') #storing in database
        file.write(f'name: "{info[0].title().strip()}" ID:{info[1].strip()} date joined: {datetime.now().date()} borrowed: () pending fees: 0P0')
        file.close()
        console.print('the member is added succesfully press enter to continue',style='bold green',justify='center')
        input()
        clear_console()
        counter+=1

def remove_member(members): 
    """  stored valuefrom data base (members) + input -> action -> database   """
    while True: #id input and validation 
        id_=console.input("enter member's id ").strip()
        try:
            members[id_]
            if len(members[id_].borrowed)!=0:
                console.print("Error:action isnt available as the member have items",style='bold red')
            else:
                break
                              
        except KeyError:
            console.print("Error:invalid id please try again",style='bold red')
                
    del members[id_] #action
                

    filewrite_member(members,'removed') #database
    clear_console()

def update_member(members):
    """  stored valuefrom data base (members) + input -> action -> database   """
    while True: #id input and validation 
        id_=console.input("enter member's id ").strip()
        try:
            members[id_]
            break
        except KeyError:
            console.print("Error:invalid id please try again",style='bold red')


    while True:# action 
            console.print(Panel("1.name    2.date joined"),justify='center')
            in_=input().strip()
            if in_=='1':
                new_name=console.input('please enter new name ').strip().capitalize()
                members[id_].name=new_name
                break

            elif in_=='2':
                while True:
                    date=console.input("please enter the date in the format YYYY-MM-DD for ex 2007-11-06 ").strip()
                    try :
                        re.search(r'^(\d{4}-\d{2}-\d{2})$',date).group(1)
                        if int(date.split('-')[2])>31:
                            console.print("Error:invalid date please try again",style='bold red')
                        elif int(date.split('-')[1])>12:
                            console.print("Error:invalid date please try again",style='bold red')
                        else:
                            break
                    except AttributeError:
                        console.print("Error:invalid date format please try again",style='bold red')
                members[id_].date_joined=date
                break
              
            else:
                console.print("Error:invalid option please try again",style='bold red')
                delay(2)
                clear_console()


    filewrite_member(members,"updated") #database
    clear_console()

def member_checkout(members,items):
    """  stored valuefrom data base (members,items) + input -> action -> database   """
    while True:#members id and validation 
        id_mem=console.input("enter member's id ").strip()
        try:
            members[id_mem]
            if len(members[id_mem].borrowed)<members[id_mem].borrow_lmt:
                if members[id_mem].status=="suspended":
                    console.print("Error:Action isn't available the member's suspended please try again",style='bold red',justify='center')
                else:
                    break
            else:
                console.print("Error:Action isn't available the member hit borrow limit please try again",style='bold red',justify='center')
                delay(2)
        except KeyError:
                console.print("Error:invalid id please try again",style='bold red')

    while True:#items id and validation
        id_it=console.input("enter the item's id ").strip()
        try:
            items[id_it]
            if items[id_it].total_copies-items[id_it].no_checkedout>0:
                break
            else:
                console.print("Error:Action isn't available item isnt available please try again",style='bold red',justify='center')
        except KeyError:
            console.print("Error:invalid id please try again",style='bold red')
                        
    members[id_mem].borrowed.append([id_it,datetime.now().date().isoformat()]) #action

    filewrite_member(members,"updated") #database
    clear_console()

def member_return(members,items):
    """  stored valuefrom data base (members,items) + input -> action -> database   """
    while True:#members id and validation 
        id_mem=console.input("enter member's id ").strip()
        try:
            members[id_mem]
            if len(members[id_mem].borrowed)!=0:
                break
            else:
                console.print("Error:Action isn't available the member has no borrowed items please try again",style='bold red',justify='center')
                delay(2)
        except KeyError:
                console.print("Error:invalid id please try again",style='bold red')

    while True:#items id and validation 
        id_it=console.input("enter the item's id ").strip()
        try:
            items[id_it]                        
            if id_it in join_borrowed(members[id_mem]):
                break
            else:
                console.print("Error:Action isn't available the member doesnt have this item please try again",style='bold red',justify='center')
                delay(2)
        except :
            console.print("Error:invalid id please try again",style='bold red')

    for ind,inc in enumerate(members[id_mem].borrowed):#action
        if id_it.strip()==inc[0].strip():
            members[id_mem].per_fees=str(int(fees_calc_ind(inc))+int(members[id_mem].per_fees))
            del members[id_mem].borrowed[ind]
                        
                        
    filewrite_member(members,"updated") #database
    clear_console()
     
def pending_fees_pay(members):
    """  stored valuefrom data base (members) + input -> action -> database   """
    while True: #members id and validation 
        id_mem=console.input("enter member's id ")
        try:
            members[id_mem]
            if int(members[id_mem].per_fees)==0:
                console.print("Error:the member doesnt have outstanding confirmed fees please try again",style='bold red',justify='center')
            else: 
                break
        except KeyError:
            console.print("Error:invalid id please try again",style='bold red')

    while True: #amount to be paid and validation 
        amount=console.input('please enter the amount to be payed ')
        try:
            int(amount)
            if int(amount)>int(members[id_mem].per_fees):
                    console.print("Error:the member's confirmed fee is smaller than the amount please try again",style='bold red',justify='center')
            else:
                break
        except ValueError:
            console.print("Error:invalid amount please try again",style='bold red')
            
    members[id_mem].per_fees=str(int(members[id_mem].per_fees)-int(amount)) #action

    filewrite_member(members,"updated") #database
    clear_console()

######################################################################################################################################################## main code
console.print("Welcome",style="bold",justify="center")
delay(1.5)
while True:
    clear_console()
    fees_calc()
    items=item_read()
    members=member_read(items)

    

    console.print(Panel("1.item managment\n2.member managment\n3.quit",title="pick an option",title_align="center"),justify="center")
    o=input().strip()

    if o=='1':
        clear_console()
        while True:
            console.print(Panel("1.add an item\n2.remove an item\n3.update an item\n4.search for an item\n5.display all items\n6.back",title="pick an option",title_align="center"),justify="center")
            o=input().strip()
            
            if o=='1':
                add_item()
    

            elif o=='2':
                remove_item(items)
    

            elif o=='3':
                update_item(items)

    
            elif o=='4':
                searchitem(items)

            elif o=='5':
                clear_console()
                item_table(items)
                console.print('press enter to continue',justify='center')
                input()

            elif o=='6':
                break

            else:
                console.print("Error:invalid option please try again",style='bold red')
                delay(2)
            items=item_read()
            members=member_read(items)
    
    elif o=='2':
        while True:
            console.print(Panel("1.add a member\n2.remove a member\n3.edit member's info\n4.checkout an item\n5.return an item\n6.display all members\n7.search for members\n8.member's fee payed\n9.back"),justify='center')
            ans=input().strip()


            if ans=='1':
                add_member()

            elif ans=='2':
               remove_member(members)
            
            elif ans=='3':
                update_member(members)
                
            elif ans=='4':
                member_checkout(members,items)

            elif ans=='5':
                member_return(members,items)
                
            elif ans=='6':
                clear_console()
                member_table(members)
                console.print('press enter to continue',justify='center')
                input()

            elif ans=='7':
                clear_console()
                member_table(search_member(members))
                console.print('press enter to continue',justify='center')
                input()

            elif ans=='8':
               pending_fees_pay(members)

            elif ans=='9':
                break

            else:
                console.print("Error:invalid option please try again",style='bold red')
                delay(2)
            
            fees_calc()
            items=item_read()
            members=member_read(items)
               
    elif o=='3':
        break

    else:
        console.print("Error:invalid option please try again",style='bold red')
        delay(2)
        