import pygame
import serial
import math
import random
import time
import os.path
from openal import * 
import serial.tools.list_ports
from pygame.locals import Color, KEYUP, K_ESCAPE, K_RETURN
# import PyOpenAL (will require an OpenAL shared library)
from openal import * 

# import the time module, for sleeping during playback
import time

pygame.init()
black = Color('black')
white = Color('white')
yellow = Color('yellow')
darkgreen = (50,100,50)
myfont = pygame.font.SysFont(None,25)#,False,False)
bigfont= pygame.font.SysFont(None,50)#,False,False)
menufont = pygame.font.SysFont(None,100)#,False,False)
Sndfile_path = os.path.join("SND","reload.wav")
reload = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","gun_shot.wav")
source = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","L.wav")
sL = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","R.wav")
sR = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","intro1.wav")
intro1 = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","connect.wav")
connect = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","disconnect.wav")
disconnect = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","mainmenu.wav")
mainmenu = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","question.wav")
Q_sentence = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","ans")
Sndfile_path = os.path.join(Sndfile_path,"1.wav")
cow = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","ans")
Sndfile_path = os.path.join(Sndfile_path,"ans2.wav")
cat = oalOpen(Sndfile_path)
Sndfile_path = os.path.join("SND","introGame2.wav")
introGame2 = oalOpen(Sndfile_path)

bitrate = 57600
sight_time = 60
sound_sts = False
def num2snd(num):
    #snd_filename = str(num)+".wav" 
    snd_filename = os.path.join("SND",str(num)+ ".wav")
    s = oalOpen(snd_filename)
    s.set_looping(False)
    s.play()

def message2screen(msg, x, y, color):
    screen_text = myfont.render(msg, False,color)
    screen.blit(screen_text,(x,y))

def BigText2screen(msg, x, y, color):
    screen_text = bigfont.render(msg, False,color)
    screen.blit(screen_text,(x,y))

def MenuText2screen(msg, x, y, color):
    screen_text = menufont.render(msg, False,color)
    screen.blit(screen_text,(x,y))

def get_ports():
    ports = ()
    ports = serial.tools.list_ports.comports()
    #print (ports[0])
    return ports

def finePixy(portsFound):
    commPort = None
    numConnection = len(portsFound)
    
    if numConnection > 0:
        for i in range (0,numConnection):
            port = portsFound[i]
            strPort = str(port)
            spritPort = strPort.split(' ')
            commPort = spritPort[0]
            try :
                ser = serial.Serial(commPort, 57600)
                time.sleep(2)
                ser.write(b'Who are u\n')
                time.sleep(0.1)
                while ser.in_waiting:
                    ans = ser.readline().decode('utf-8')
                    if ans.rstrip() == 'Pixy':
                        ser.close()
                        return commPort
                    else:
                        ser.close()
                        return None
            except:
                print ("Can not open serial port.")
            
def target_draw(x,y):
    pygame.draw.circle(screen, red, [x, y],40,3)
    pygame.draw.line(screen, red, (x,y-45),(x,y-32),4)
    pygame.draw.line(screen, red, (x,y+45),(x,y+32),4)
    pygame.draw.line(screen, red, (x-45,y),(x-32,y),4)
    pygame.draw.line(screen, red, (x+45,y),(x+32,y),4)

def target_paper():
    pygame.draw.circle(screen, black, [159*3, 99*3],22,22)
    pygame.draw.circle(screen, black, [159*3, 99*3],50,3)
    pygame.draw.circle(screen, black, [159*3, 99*3],90,3)
    pygame.draw.circle(screen, black, [159*3, 99*3],140,3)
    pygame.draw.circle(screen, black, [159*3, 99*3],200,3)
    pygame.draw.circle(screen, black, [159*3, 99*3],280,3)
    message2screen("10",159*3-10,99*3-8,white)
    message2screen("9",159*3-36,99*3-8,black)
    message2screen("9",159*3+31,99*3-8,black)
    message2screen("8",159*3-70,99*3-8,black)
    message2screen("8",159*3+62,99*3-8,black)
    message2screen("7",159*3-117,99*3-8,black)
    message2screen("7",159*3+107,99*3-8,black)
    message2screen("6",159*3-171,99*3-8,black)
    message2screen("6",159*3+161,99*3-8,black)
    message2screen("5",159*3-242,99*3-8,black)
    message2screen("5",159*3+232,99*3-8,black)
    
def score_cal(x,y,cx,cy):
    dist = math.sqrt(((x-cx)*(x-cx)+(y-cy)*(y-cy))/3)
    if  dist < 11.5:
        return  10
    elif dist < 25.5+3:
        return 9
    elif dist < 45.5+6:
        return 8
    elif dist < 70.5+9:
        return 7
    elif dist < 100.5+12:
        return 6
    elif dist < 140.5+15:
        return 5
    elif dist >140.5+15  :
        return 4
    
def bullet_show(num):
    for i in range(5):
        if i < num  :
            screen.blit(bullet_gold, (250*3+i*35,170*3))
        else:
            screen.blit(bullet_empty, (250*3+i*35,170*3))
            
def menu_sound(menu):
    if menu > 0 and menu < 4 :
        snd_filename = os.path.join("SND","menu"+str(menu)+ ".wav")
        menuSND = oalOpen(snd_filename)
        menuSND.set_looping(False)
        menuSND.play()

def game2wall(sc):
    screen.fill(darkgreen)
    screen.blit(questionMark, (150,120))
    screen.blit(questionMark, (600,120))
    BigText2screen('SCORE '+ str(sc) , 30, 20, green)
    pygame.display.flip()

def game2key(sc,ansKey,x):
    screen.fill(darkgreen)
    screen.blit(questionMark, (150,120))
    screen.blit(questionMark, (600,120))
    BigText2screen('SCORE '+ str(sc) , 30, 20, green)
    key_filename = os.path.join("IMG","ans")
    key_filename = os.path.join(key_filename,str(ansKey)+ ".png")
    ansPic = pygame.image.load(key_filename).convert()
    #print (key_filename)
    #print (x)
    if x == -4 :
        screen.blit(ansPic, (150,120))
    else:
        screen.blit(ansPic, (600,120))
    pygame.display.flip()
        
def intro():
    file_path = os.path.join("IMG","License.png")
    License =  pygame.image.load(file_path).convert()
    License.set_colorkey(black)
    screen.blit(License, (120,20))
    pygame.display.flip()
    intro1.set_looping(False)
    intro1.play()
    time.sleep(11)


programMode = 0
menuSelect = 0
score = 0
level = 1
pygame.mixer.init()
green  = (  0,255,  0)
red    = (255,  0,  0)
blue   = (  0,  0,255) 

foundPorts = () 
foundPorts = get_ports()
size=(320*3+10,200*3+10)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Blind Shooting Game")
file_path = os.path.join("IMG","icon_bullet_empty_long.png")
bullet_empty =  pygame.image.load(file_path).convert()
bullet_empty.set_colorkey(black)
file_path = os.path.join("IMG","icon_bullet_gold_long.png")
bullet_gold =  pygame.image.load(file_path).convert()
bullet_gold.set_colorkey(black)
file_path = os.path.join("IMG","text_score_small.png")
TXTscore =  pygame.image.load(file_path).convert()
TXTscore.set_colorkey(black)
file_path = os.path.join("IMG","text_1.png")
TXTnum1 =  pygame.image.load(file_path).convert()
TXTnum1.set_colorkey(black)
file_path = os.path.join("IMG","text_2.png")
TXTnum2 =  pygame.image.load(file_path).convert()
TXTnum2.set_colorkey(black)
file_path = os.path.join("IMG","shot_yellow_small.png")
ShotHole =  pygame.image.load(file_path).convert()
ShotHole.set_colorkey(black)
file_path = os.path.join("IMG","wall.png")
menuwall =  pygame.image.load(file_path).convert()
file_path = os.path.join("IMG","BlueQuestionMark2.png")
questionMark =  pygame.image.load(file_path).convert()

intro()

#============================================================
#                   Pixy Scan
#============================================================
Pixy = finePixy(foundPorts)
#print (Pixy)
if Pixy is None :
    pixy_connect = False
    disconnect.set_looping(False)
    disconnect.play()
    time.sleep(3)
else:
    ser = serial.Serial(Pixy, bitrate, timeout = 1)
    pixy_connect = True
    connect.set_looping(False)
    connect.play()
    time.sleep(2.5)
mainmenu.set_looping(False)
mainmenu.play()
time.sleep(2)
programMode = 1    
SNDplay = 0
#frame_count =0
#F_count = False
#Loop game control
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
Bpoint = ""
bullet_in_mag = 5
Bullet_point = []
Sndfile_path = os.path.join("SND","pew.wav")
target_sound = oalOpen(Sndfile_path)
player_listener = Listener()

#============================================================
#                       Main Loop
#============================================================
target_pos = (250*3,150*3)
anspre_time = pre_time = pygame.time.get_ticks()
ask_speak = False
end_of_game2 = False
#askNum = 1
ask_file = ch_file = 0
QuestionNumber = 0
QuestionList = []
#ansX = 0
ch1X = 0
randomSound = False 
choice2 = 0
Rdm = [-4,4]
goToNextGame = False
mydelay = 0
timelimit = 0
introG2 = False
Game2start = False
while not done:
    
    #if F_count :
    #    frame_count += 1
        #print (frame_count)
    #if frame_count > 20 :
    #    frame_count = 0
    #    F_count = False
    while pixy_connect and ser.in_waiting:
        Bpoint = ser.readline()
        #print (Bpoint)
        if len(Bpoint) > 0 :
            Bpoint = Bpoint[:len(Bpoint)-1]
            Bpoint = Bpoint.decode('UTF-8')
            co1 = Bpoint.split(" ")
            print (co1)
            if co1[0]=='G':
                if co1[1] == '1' and co1[2] == '0\r' :
                    if programMode == 1 :
                        SNDplay = 1 
                        if menuSelect < 4 :
                            menuSelect+=1
                        if menuSelect == 4:
                            menuSelect = 1
                    elif programMode == 2:
                        # reload bullet
                        bullet_in_mag = 5
                        reload.set_looping(False)
                        reload.play()
                elif co1[1] == '1' and co1[2] == '1\r' :
                    programMode = 1 # Menu page
                elif co1[1] == '0' and co1[2] == '1\r' : 
                    
                    if programMode < 2:
                        if menuSelect == 3 :
                            done = True
                        programMode = 2
                    else :
                        if bullet_in_mag > 0 :
                            source.set_looping(False)
                            source.play()
                            time.sleep(0.2)
                            Bullet_point.append(target_pos)
                            bullet_in_mag -= 1
                            s = score_cal(target_pos[0],target_pos[1],159*3,99*3)
                            num2snd(s)
                            score = score + s
            elif co1[0] == '1': #red laser
                sight_time = 60
                sound_sts = True
                target_pos = ((319-int(co1[1]))*3,int(co1[2])*3)
                if target_pos[0] < 80 :
                    target_pos = (90,target_pos[1])
                    sL.set_looping(False)
                    sL.play()
                    #time.sleep(2)
                elif target_pos[0] > 320*3-80:
                    target_pos = (320*3-70,target_pos[1])
                    sR.set_looping(False)
                    sR.play()
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 :
                if menuSelect == 3:
                    done = True
                elif menuSelect == 2:
                    if Game2start == False:
                        Game2start = True
                        if introG2 == False:
                            introG2 = True
                        programMode = 2
                        SNDplay = 1
                elif menuSelect == 1:
                    programMode = 2
                    SNDplay = 1
            if event.button == 5:
                if menuSelect < 4 :
                    menuSelect+=1
                    SNDplay = 1
                else:
                    menuSelect = 1
                    SNDplay = 1
            elif event.button == 4:
                if menuSelect > 0 :
                    menuSelect-=1
                    SNDplay = 1
                else:
                    menuSelect = 3
                    SNDplay = 1
        
    #====================================================
    #                   Game Menu
    #====================================================             
    if programMode == 1:
        screen.blit(menuwall, (0,0))
        MenuText2screen('Blind Shooting Game' , 120, 50, yellow)
        MenuText2screen('Shooting' , 300, 200, green)
        MenuText2screen('Vocab Quiz' , 300, 350, green)
        MenuText2screen('EXIT' , 350, 500, green)      
        
        if menuSelect == 1 :
            MenuText2screen('Shooting' , 300, 200, red)
        if menuSelect == 2 :
            MenuText2screen('Vocab Quiz' , 300, 350, red)
        if menuSelect == 3 :
            MenuText2screen('EXIT' , 350, 500, red)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if menuSelect == 3:
                    done = True
                else:
                    programMode = 2
    if programMode == 2 and menuSelect == 1 :
        if not pixy_connect :
            if pygame.mouse.get_focused():
                #print ("mouse IN")
                sight_time = 60
                sound_sts = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    if  bullet_in_mag < 5:
                        bullet_in_mag = 5
                        reload.set_looping(False)
                        reload.play()
            if event.type == pygame.MOUSEMOTION :
                target_pos = pygame.mouse.get_pos()
                if target_pos[0] < 50 :
                    target_pos = (55,target_pos[1])
                    sL.set_looping(False)
                    sL.play()
                    pygame.mouse.set_pos(target_pos)
                elif target_pos[0] > 320*3-40:
                    target_pos = (320*3-45,target_pos[1])
                    sR.set_looping(False)
                    sR.play()
                    pygame.mouse.set_pos(target_pos)
                                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bullet_in_mag >0 :
                    bullet_in_mag -= 1
                    source.set_looping(False)
                    source.play()
                    time.sleep(0.2)
                    Bullet_point.append(target_pos)
                    s = score_cal(target_pos[0],target_pos[1],159*3,99*3)
                    num2snd(s)
                    score = score + s
                    target_pos = (random.randrange(60,900,3),random.randrange(60,450,3))
                    pygame.mouse.set_pos(target_pos[0],target_pos[1])
                  
        screen.fill(white)
        bullet_show(bullet_in_mag)
        BigText2screen('SCORE '+ str(score) , 30, 20, green)
        #screen.blit(TXTscore, (30,20))
        BigText2screen('LEVEL '+ str(level) , 250*3, 20, green)
        target_paper()
        target_draw(target_pos[0],target_pos[1])
                
        for temp in Bullet_point :
            #pygame.draw.circle(screen, green,[temp[0],temp[1]] ,10,10 )
            screen.blit(ShotHole, (temp[0]-10,temp[1]-10))
        
        if len(Bullet_point) == 5 and not goToNextGame :
            goToNextGame = True
            mydelay = 10
        if  goToNextGame and mydelay == 0:
            goToNextGame = False
            
            
        cur_time = pygame.time.get_ticks()
        if cur_time - pre_time >200 :
            pre_time = pygame.time.get_ticks()
            if timelimit > 0 :
                timelimit -= 1
                print (timelimit)
                if timelimit == 0 :# restart level 3
                    print ("game over")
            if mydelay > 0 :
                mydelay -= 1
                if mydelay == 0:
                    if level == 1 :
                       level = 2
                       score = 0
                    elif level == 2 :
                        if score >= 35 :
                            level = 3
                            #
                        else :
                            #Sndfile_path = os.path.join("SND","notpassL2.wav")
                            #notpassL2 = oalOpen(Sndfile_path)
                            #notpassL2.set_looping(False)
                            #notpassL2.play()
                            score = 0
                    elif level == 3 :
                        if score >= 40 :
                            timelimit = 600 # 30fps*20sec  
                            level = 4
                        else :
                            score = 0
                    elif level == 3 and score >= 35 and timelimit > 0:
                        level = 4
                    Bullet_point = []
            
            if  target_sound.get_state() != AL_PLAYING and mydelay == 0:
                player_listener.set_position([0,0,2])
                target_sound.set_position([(target_pos[0]-159*3)/4,(target_pos[1]-99*3)/4,0])
                target_sound.set_pitch(1)
                if sound_sts == True :
                    target_sound.play()
    #pygame.display.flip()    
#===============================================================================================                
    if programMode == 2 and menuSelect == 2 : # VOCAB. QUIZ
        
        game2wall(score)
        
        
        if introG2 == True :
            introG2 = False
            randomSound = True 
            score = 0
            introGame2.set_looping(False)
            introGame2.play()
            while True :
                    if introGame2.get_state() != AL_PLAYING :
                        break
        if randomSound == True :
            randomSound = False
            while True :
                x = random.randrange(1,11)
                if x not in QuestionList:
                    QuestionList.append(x)
                    if len(QuestionList) == 10:
                        print(QuestionList)
                        break
        
        if not pixy_connect :
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ask_speak == True :
                    answer_is =  int((target_pos[0]-159*3)/36)
                    print ( answer_is )
                    if (ch1X == -4 and answer_is <= -4) or (ch1X == 4 and answer_is >= 4):                          
                        Sndfile_path = os.path.join("SND","correct.wav")
                        correct = oalOpen(Sndfile_path)
                        correct.set_looping(False)
                        correct.play()
                        score += 1
                        
                    else :
                        Sndfile_path = os.path.join("SND","incorrect.wav")
                        incorrect = oalOpen(Sndfile_path)
                        incorrect.set_looping(False)
                        incorrect.play()
                      
                    game2key(score,QuestionList[QuestionNumber],ch1X)
                    time.sleep(2)
                    
                    if QuestionNumber < 9 :
                        QuestionNumber += 1
                        ask_speak = False
                    else:
                        end_of_game2 = True
            if event.type == pygame.MOUSEMOTION :
                target_pos = pygame.mouse.get_pos()
                if target_pos[0] < 50 :
                    target_pos = (55,target_pos[1])
                    sL.set_looping(False)
                    sL.play()
                    pygame.mouse.set_pos(target_pos)
                elif target_pos[0] > 320*3-40:
                    target_pos = (320*3-45,target_pos[1])
                    sR.set_looping(False)
                    sR.play()
                    pygame.mouse.set_pos(target_pos)
                                        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    source.set_looping(False)
                    source.play()
                    time.sleep(0.2)
                    
        anscur_time = pygame.time.get_ticks()
        if anscur_time - anspre_time > 5000 and ask_speak == True and end_of_game2 == False :
            anspre_time = pygame.time.get_ticks()
            ask_file = os.path.join("SND","ans")
            ask_file = os.path.join(ask_file, str(QuestionList[QuestionNumber])+".wav")
            ch1_sound =  oalOpen(ask_file)
            if  ch1_sound.get_state() != AL_PLAYING :
                player_listener.set_position([0,0,2])
                ch1_sound.set_position([ch1X,0,0])
                ch1_sound.play()
               
            if  ch2_sound.get_state() != AL_PLAYING :
                #player_listener.set_position([0,0,2])
                if ch1X == 4 :
                    choice2 = -4
                else:
                    choice2 = 4
                    
                ch2_sound.set_position([choice2,0,0])
                ch2_sound.play()
            time.sleep(2) 
        cur_time = pygame.time.get_ticks()
        if cur_time - pre_time >300 and ask_speak == True and end_of_game2 == False :
            pre_time = pygame.time.get_ticks()
            if  target_sound.get_state() != AL_PLAYING :
                player_listener.set_position([0,0,2])
                target_sound.set_position([(target_pos[0]-159*3)/20, 0, 2])
                target_sound.play()
    pygame.display.flip()
    if SNDplay == 1 :
        if programMode == 1:
            menu_sound(menuSelect)
            SNDplay = 0
    if programMode == 2 and menuSelect == 2:
        if ask_speak == False:
            ask_speak = True
            ch1X = random.choice(Rdm)
            while True:
                x = random.randrange(1,6)
                if x != QuestionList[QuestionNumber]:
                    break    
            ask_file = os.path.join("SND","ans")
            ask_file = os.path.join(ask_file, str(x)+".wav")
            ch2_sound =  oalOpen(ask_file)
            Q_sentence.set_looping(False)
            game2wall(score)
            Q_sentence.play()
            while True :
                if Q_sentence.get_state() != AL_PLAYING :
                    break
            ask_file = os.path.join("SND","ask")
            ask_file = os.path.join(ask_file, str(QuestionList[QuestionNumber])+".wav")
            ask_sound =  oalOpen(ask_file)
            ask_sound.set_looping(False)
            for i in range(2):
                ask_sound.play()
                time.sleep(2)
            
clock.tick(30)
snd_filename = os.path.join("SND","TheEnd"+ ".wav")
endSND = oalOpen(snd_filename)
endSND.set_looping(False)
endSND.play()
time.sleep(1.5)
if pixy_connect :
    ser.close()
oalQuit()
pygame.quit()
