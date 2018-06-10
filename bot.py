# bot.py
# The code for our bot

import cfg
import time
import sql
from twitch import TwitchClient
from time import sleep
from twitchobserver import Observer
import psycopg2 as db
import threading
from collections import Counter


sql.create_viewer_list(cfg.CHAN)



# enable messages that the bot sends to be displayed in the terminal
def botmsg(message):
    bot = str(cfg.NICK)
    message = message
    print(bot, ": ", message)





def main():
    # Networking functions, joins channel and sends a message, retrieves modlist
    # To do:
    # add custom commands
    obs = Observer(cfg.NICK, cfg.PASS)
    obs.start()
    obs.join_channel(cfg.CHAN)
    #obs.send_message("Hi everyone <3", cfg.CHAN)
    obs.send_message("/mods", cfg.CHAN)

    def get_votes():        
        if event.type == 'TWITCHCHATMESSAGE':
            votes = {}
            votes.clear()
            
            timeout = 70
            timeout_start = time.time()
            while time.time() < timeout_start + timeout:
                time.sleep(0.25)

                try:
                    if event.message in str(voteOptions):
                        votes[event.nickname] = event.message
                    
                    
                except:
                    'do nothing'

                
            c = Counter(votes.values())
            c = str(c)
            c = c.split('{')
            c = c[1]
            c = c.split('}')
            c = c[0]


            c = str(c)            
            results = c.split(',')
            for result in results:
                i = result.split(':')
                message = 'the result of option '+i[0]+ ' is a total of '+ i[1]+ ' votes'
                botmsg(message)
                obs.send_message(message, cfg.CHAN)

                
                
                        
                
            #botmsg('The results of the voting is: ' + str(message))


            print(votes)
            print(c)

    


    
     




########################################################################

############ Log, Modlist, Caps Filter

    while True:
        for event in obs.get_events():
            
            
            # print Messages in Terminal 
            # for Debugging reasons
            if event.type == 'TWITCHCHATMESSAGE':
                print(event.nickname,": ",event.message)

            # get modlist
            # gets a list of all mods of the channel
            # and saves them in modlist
            if event.type == 'TWITCHCHATNOTICE' and "The moderators of this channel are:" in event.message:
                modlist = event.message.split(":")
                modlist = modlist [1]


                    
# to Do get active list username + ID
            # create active viewerlist
            if event.type == 'TWITCHCHATUSERSTATE':
                activeViewer = {}
                name = str(event._params)
                name = name.split('#')
                name = name[1]
                client = TwitchClient(cfg.ClientID)
                try:
                    nameid = client.users.translate_usernames_to_ids(name)
                except:
                    continue

                nameid = str(nameid)
                nameid = nameid.split(",")
                nameid = nameid[1]
                nameid = nameid.split(":")
                nameid = nameid[1]
                nameid = nameid.split("'")
                nameid = nameid[1]

                activeViewer[name] = nameid
                activeViewer.setdefault(name,nameid)
            
            # delete user from list if they leave
            if event.type == 'TWITCHCHATLEAVE':
                name = str(event.nickname)
                try:
                    del activeViewer[name]
                except:
                    'do nothing'
            


       



                

########################################################################

####### Kuu commands 
            # Hype
            if event.type == 'TWITCHCHATMESSAGE'and event.message == "!hype" and  event.nickname == 'chris_lee_bear' :
                message = "sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd "
                obs.send_message(message, cfg.CHAN)
                botmsg(message)   

            # Bye
            if event.type == 'TWITCHCHATMESSAGE'and "say goodbye bot" in event.message and  event.nickname == 'chris_lee_bear' :
                message = "master said I have to say goodbye... see you soon everyone <3"
                obs.send_message(message, cfg.CHAN)
                botmsg(message)                

            #Sub notice
            if event.type == 'TWITCHCHATNOTICE' and "subscribed" in event.message:
                message1 = "Thanks for the Sub <3"
                message2 = "sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd sunbroLewd "
                obs.send_message(message1, cfg.CHAN)
                obs.send_message(message2, cfg.CHAN)
                botmsg(message1)   
                botmsg(message2)  

            # Voting


            if event.type == 'TWITCHCHATMESSAGE':
                if "!voting" in event.message and (event.nickname in modlist or event.nickname == 'chris_lee_bear' or event.nickname == cfg.CHAN):
                    try:
                        voteOptions = []
                        message = event.message.split(' ')
                        message = message[1]
                        message = int(message)+1
                        voteOptions = list(range(message))
                        del voteOptions[0]
                        print(voteOptions)

                        #obs.send_message('Voting will be open for 60 seconds. To voty simply type the number in chat you want to vote for. The options are '+ str(voteOptions), cfg.CHAN)
                        #time.sleep(1)

                        t = threading.Thread(target=get_votes)
                        t.daemon = True
                        t.start()
                        
                    except:
                        print('do nothing')

            if event.type == 'TWITCHCHATMESSAGE' and event.message == '!voteinfo':
                message = ('If voting is enabled, to vote simply type the number in chat you want to vote for and remember you can change your vote but only the last vote will be counted')
                botmsg(message)
                obs.send_message(message,cfg.CHAN)
                    

            

                            


                            
                            
                
                            
                            





                

                        

                           
                
                            



############# Custom Commands

            # Kappa Command also known as test command
            if event.type == 'TWITCHCHATMESSAGE' and event.message == "!Kappa":
                user = str(event.nickname)
                message = "@" + user + " Kappa"
                obs.send_message(message, cfg.CHAN)
                botmsg(message)
                
            # Shoutout 
            if event.type == 'TWITCHCHATMESSAGE' and "!so" in event.message and (event.nickname in modlist or event.nickname == cfg.CHAN) :
                try:
                    b = event.message.split(" ")
                    b = b[1]
                    b = str(b)
                    message = "please check out this awesome person @" + b + " at: https://www.twitch.tv/" + b
                    obs.send_message(message, cfg.CHAN)
                    botmsg(message)
                except:
                    continue 

            # mod list test
            if event.type == 'TWITCHCHATMESSAGE' and event.message == "!mod" :
                message = "the awesome people that help me doing my thing :" + modlist
                obs.send_message(message, cfg.CHAN)
                botmsg(message)

            # User ID test    
            if event.type == 'TWITCHCHATMESSAGE' and event.message == "!user":
                
                client = TwitchClient(cfg.ClientID)

                message = client.users.translate_usernames_to_ids(event.nickname)
                message = str(message)
                message = message.split(",")
                message = message[1]
                message = message.split(":")
                message = message[1]
                message = message.split("'")
                message = message[1]
                obs.send_message(message, cfg.CHAN)
                botmsg(message)


            if event.type == 'TWITCHCHATMESSAGE' and event.message == "!list":
                message = str(activeViewer[name])
                obs.send_message(message, cfg.CHAN)
                botmsg(message)



#### sql part
    #fill_viewer_list
            if event.type == 'TWITCHCHATMESSAGE' :
                client = TwitchClient(cfg.ClientID)
                try:
                    conn = db.connect(dbname=cfg.DBname,user=cfg.DBuser,password=cfg.DBpassword,host=cfg.DBhost,port=cfg.DBport)
                    conn.autocommit = True

                    viewer   = str(event.nickname)

                    viewerID = client.users.translate_usernames_to_ids(event.nickname)
                    viewerID = str(viewerID)
                    viewerID = viewerID.split(",")
                    viewerID = viewerID[1]
                    viewerID = viewerID.split(":")
                    viewerID = viewerID[1]
                    viewerID = viewerID.split("'")
                    viewerID = int(viewerID[1])     

                    joindate = str(time.strftime("%Y.%m.%d"))

                    points   = int(0)

                    # insert data in table
                    cursor = conn.cursor()

                    query = """INSERT INTO {0}.viewerlist 
                                            (
                                            viewer, 
                                            viewerID,
                                            joindate, 
                                            points
                                            ) 
                        Values(  
                            %(viewer)s,
                            %(viewerID)s,
                            %(joindate)s,
                            %(points)s
                            )
                            on CONFLICT (viewerID) DO NOTHING
                            """.format(cfg.CHAN)                      
                            
                    cursor.execute(query,{'viewer':viewer, 'viewerID':viewerID,'joindate':joindate,'points':points})
                    cursor.close()
                    conn.close
                except:
                    print("fill list error")


### add points
    sql.addPoints(cfg.CHAN,activeViewer[name])





    
                
            
                
    
########################################################################

sleep(1)

if __name__ == "__main__":
    main()

            
            
