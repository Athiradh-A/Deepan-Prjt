def cls():
    print("="*15)
import mysql.connector                                                                                                      #to connect mysql and python
mydb=mysql.connector.connect(host='localhost',user='root',passwd='admin',database='voting')
cursor=mydb.cursor()
u_p={'admin':'1111','vice':'1000'}
while True:
    u=input('Enter your username to start voting process:')
    p=input('Enter your password:')
    if u not in u_p.keys():
        print("Username not available.")
        
    elif u in u_p.keys() and p not in u_p.values():
        print("Wrong password.")
    elif p==u_p[u]:
        while True:
            op=input("Are you here to vote?(y/n):")
            if op=='y':
                id=int(input("Enter your voting id:"))
                cursor.execute("select voter_id from voters")
                voters=cursor.fetchall()
                for i in voters:
                    if i[0]==id:                                                                                                    #to ensure that the voter exist in the list
                        print("\n\nThe symbols are:")
                        cursor.execute("select symbol from candidates")
                        symbols=cursor.fetchall()
                        for x in symbols:
                            print(x[0])
                        vote=input("\nCast your vote(Enter the symbol of your candidate):")                                       #casting the vote
                        the="update candidates set votes=votes+1 where symbol='%s'"%(vote)
                        try:
                            cursor.execute(the)
                            mydb.commit()
                        except:
                            mydb.rollback()
                        
                        voter='delete from voters where voter_id=%s'%(id)                                                               #remove voter from list to avoid duplicate vote
                        cursor.execute(voter)
                        mydb.commit()
                        cls()
                    else:
                        print("Wrong voter id:")
            elif op=='n':
                u=input("Enter the username:")
                p=input("Enter the password:")
                if p==u_p[u]:
                    ex=input('''Enter 1:To add or delete a candidate
Enter 2:To add or delete a voter 
Enter 3:To finish the voting process\n''')
                    if ex=='1':
                        ex1=input('''Enter 1:To add a candidate
Enter 2:To delete a candidate\n''')
                        if ex1=='1':
                            add='''insert into candidates (candidate_number,name,gender,age,symbol) values (%s,%s,%s,%s,%s)'''
                            no=int(input("Enter the candidate number(10digits):"))                                          #to add candidate
                            name=input("Enter the candidate name:")
                            g=input("Enter the candidate's gender(M/F):")
                            gen=g.upper()
                            age=int(input("Enter the candidate's age(in numbers):"))
                            symbo=input("Enter candidate symbol:")
                            symbol=symbo.lower()
                            candidate=(no,name,gen,age,symbol)
                            cursor.execute(add,candidate)
                            mydb.commit()
                            print("Successful added")
                            cls()
                        if ex1=='2':
                            no=int(input("Enter the candidate number to be deleted:"))
                            cursor.execute("select * from candidates")
                            results=cursor.fetchall()                                                                      #to delete candidate
                            for x in results:
                                if no in x:
                                    dlt='delete from candidates where candidate_number=%s'
                                    candidate=(no,)
                                    cursor.execute(dlt,candidate)
                                    mydb.commit()
                                    print("Deleted successfully.")
                                else:
                                    print("Unavailable candidate number.")
                            cls()        
                    if ex=='2':
                        ex1=input('''Enter 1:To add a voter
Enter 2:To delete a voter\n''')
                        if ex1=='1':
                            add='''insert into voters (voter_id,name,gender,age) values (%s,%s,%s,%s)'''
                            no=int(input("Enter the voter number(10digits):"))
                            name=input("Enter the voter name:")                                                           #to add voter
                            g=input("Enter the voter's gender(M/F):")
                            gen=g.upper()
                            age=int(input("Enter the voter's age(in numbers):"))
                            voter=(no,name,gen,age)
                            cursor.execute(add,voter)
                            mydb.commit()
                            print("Successfully added.")
                            cls()
                        if ex1=='2':
                            no=int(input("Enter the voter number to be deleted:"))
                            cursor.execute("select * from voters")
                            results=cursor.fetchall()                                                                     #to delete voter
                            for x in results:
                                if no in x:
                                    dlt='delete from voters where voter_id=%s'
                                    voter=(no,)
                                    cursor.execute(dlt,voter)
                                    mydb.commit()
                                    print("Deleted successfully.")
                                else:
                                    print("Unavailable voter number.")
                            cls()
                    if ex=='3':
                        confirm_id={'admin':'nimda','vice':'eciv'}
                        c=input("Enter your confirmation id:")
                        if c==confirm_id[u]:
                            print("The voting process is over.")                                                        #to end voting process 
                            break
