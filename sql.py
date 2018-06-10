import cfg
import sqlalchemy as sql
import psycopg2 as db
from twitchobserver import Observer
from twitch import TwitchClient
import time 
import threading


obs = Observer(cfg.NICK, cfg.PASS)

obs.start()
obs.join_channel(cfg.CHAN)



# create a schema and table for the users and their streampoints
def create_viewer_list(schema):
    conn = db.connect(dbname=cfg.DBname,user=cfg.DBuser,password=cfg.DBpassword,host=cfg.DBhost,port=cfg.DBport)
    conn.autocommit = True
    
    # create schema and table viewer list
    cursor = conn.cursor()
    cursor.execute('CREATE SCHEMA IF NOT EXISTS {0}'.format(schema))
    cursor.execute("""CREATE TABLE IF NOT EXISTS {0}.viewerlist
                    (
                        id              SERIAL,
                        viewer          VARCHAR(80) ,
                        viewerID        NUMERIC PRIMARY KEY,
                        joindate        VARCHAR(80) ,
                        followdate      VARCHAR(80) ,   
                        points          NUMERIC
                    )""".format(schema))

    cursor.close()
    conn.close()



# fill table with users       
def fill_viewer_list(schema):
    client = TwitchClient(cfg.ClientID)
    while True:
        for event in obs.get_events():
            if event.type == 'TWITCHCHATMESSAGE' :
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
                            """.format(schema)                      
                            
                    cursor.execute(query,{'viewer':viewer, 'viewerID':viewerID,'joindate':joindate,'points':points})
                    cursor.close()
                    conn.close
                except:
                    print("error")

#To do add points to users in userlist
def addPoints(schema,activeViewer):
    # add points every n seconds
    conn = db.connect(dbname=cfg.DBname,user=cfg.DBuser,password=cfg.DBpassword,host=cfg.DBhost,port=cfg.DBport)
    conn.autocommit = True
    cursor = conn.cursor()

    query = """ update {0}.viewerlist
                    points
                set
                    points = (points + 5)
                where viewerID in ('{1}')
            """.format(schema,activeViewer)
    cursor.execute(query)        
    cursor.close()
    conn.close
    threading.Timer(5,addPoints).start()



           
    



#create_viewer_list(cfg.CHAN)
#fill_viewer_list(cfg.CHAN)

