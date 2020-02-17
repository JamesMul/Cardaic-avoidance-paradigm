#Avoidance cardiac paradigm task script
#James Mulcahy

#All imports

import os
import sys
import psychopy.gui
from psychopy import visual, event
import psychopy.core
import random
import psychtoolbox as ptb
from psychopy import sound
import numpy as np
import pandas as pd
from psychopy.hardware import keyboard
from psychopy import core
import time

# 1.Importing Modules for cardiac timing

from psychopy import gui, event, visual, core, logging, prefs, sound
import glob, os, random
from intart_functions import escape_keypress, shutdown #import customized functions
from pyglet.window import key
import numpy as np
import time
from ctypes import windll

# 2. Set up parallel port

# 2.1 Enable parallel port
ppPresent = 1 #If no parallel port connection set up, change to 0

# 2.2 Set up address
if ppPresent:
    pport_address_out=888 #0x378
    pport_address_in = 889
    pport=windll.inpoutx64 #create the connection via specific dll 
    pport.Out32(pport_address_out,0) #set all the parallel port pins to zero at the beginning of the experiment

# 2.3 Import intart_functions for communicating with port
if ppPresent:
    from intart_functions import sendParallelTrigger, readParallelTrigger
    
    
    
#Functions

def get_keyboard(timer, respkeylist, keyans):
    '''
    Get key board response
    '''
    Resp = None
    KeyResp = None
    KeyPressTime = np.nan
    keylist = ['escape'] + respkeylist

    for key, time in event.getKeys(keyList=keylist, timeStamped=timer):
        if key in ['escape']:
            quitEXP(True)
        else:
            KeyResp, KeyPressTime = key, time
    # get what the key press means
    if KeyResp:
        Resp = keyans[respkeylist.index(KeyResp)]
    return KeyResp, Resp, KeyPressTime

#entering participant information#

gui = psychopy.gui.Dlg() #Opens GUI to enter subject ID and Condition

gui.addField("Subject ID:")
gui.addField("Condition:")
gui.addField("Gender:")
gui.addField("Height(cm):")
gui.addField("Weight(kg):")


gui.show()

subj_id = gui.data[0] #saves subject ID
cond_num = gui.data[1] #Saves condition number (Only 2 conditions - counterbalanced) condition 1: image 1 is CS+, condition 2: image 2 is cs+
gender = gui.data[2] #saves participants gender
height = gui.data[3] #saves participants height
weight = gui.data[4] #saves participants weight


data_path = subj_id + "_rep_" + cond_num + ".tsv" #need to ammend or remove based on save output below####


if os.path.exists(data_path): # Stops progress if file already present - needs to be adapted
    sys.exit("Data path " + data_path + " already exists!")
    
 
exp_data = [] #All experimental data saved in this list

#Saves demographic as seperate file
demographic_data = {'Subject_ID':subj_id, 'Condition_number':cond_num, 'Gender':gender, 'Height':height, 'Weight':weight}
df1 = pd.DataFrame.from_dict(demographic_data, orient='index')
df1.transpose().to_csv(subj_id + '_demographics.csv') 


#create window#

win = psychopy.visual.Window(
    size=[1100,1100],
    units="pix",
    fullscr=False #If need fullscreen change to True
)


#Creating the stimulus#

image1 = psychopy.visual.Circle(
    win=win,
    units="pix",
    radius=150,
    fillColor=[-1,-1,-1],
    lineColor=[-1,-1,-1],
    edges=128
)

image1_forratings = psychopy.visual.Circle(
    win=win,
    units="pix",
    radius=150,
    fillColor=[-1,-1,-1],
    lineColor=[-1,-1,-1],
    edges=128,
    pos=(0,250)
)

image2 = psychopy.visual.Rect(
    win=win,
    units="pix",
    width=300,
    height=300,
    ori=45,
    fillColor=[-1,-1,-1],
    lineColor=[-1,-1,-1],
)

image2_forratings = psychopy.visual.Rect(
    win=win,
    units="pix",
    width=300,
    height=300,
    ori=45,
    fillColor=[-1,-1,-1],
    lineColor=[-1,-1,-1],
    pos=(0,280)
)

fixation = visual.ShapeStim(win, 
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor="white",
    size=50
)

startle = sound.Sound('startle.wav')


#counterbalancing

#condition1 = image1 as CS+, image2 as CS-
#condition2 = Image1 as CS-, image2 as CS+



########Part one - Instructions ########

message = visual.TextStim(win, text='Welcome to the experiment.\n\nPress the spacebar to continue.')
message.draw()
win.flip()

psychopy.event.waitKeys()


instructions = visual.TextStim(win, text = 'In the following task you will see pictures appear quickly on the screen.\n\nThese pictures may or may not be followed by a loud noise.\n\nFor the first part of the experiment you should just watch the screen and answer any questions when prompted.\n\nPress the spacebar to continue.')

instructions.draw()

win.flip()

psychopy.event.waitKeys()

fixation.draw()

win.flip()

fixation.draw()
win.flip()

psychopy.core.wait(6)#wait 6 seconds

########What happens on a given trial?########

pre_duration_s = 2 #pre trial time duration
stim_duration_s = 0.1 #stimuli presentation duration
post_duration_s = 4 #post trial duration (interval over whic aversive noise is played (1 seconds of safe time))
min_iti_s = 6 #inter-trial interval
aversive_noise_time_window = 4 # Time window in which averstive noise will be played (first second is safe so noise occurs randomly between seconds 1-4)


########Part two - novel stimulus ratings#########

#Variables saved
nsrating_list_image1 = [] 
nsrating_decisiontime_list_image1 = [] 
nsrating_list_image2 = []
nsrating_decisiontime_list_image2 = []

#Presents rating scale image 1
ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
item = visual.TextStim(win, "How likely is it that this picture will be followed by a loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm.")
while ratingscale.noResponse:
    image1_forratings.draw()
    item.draw()
    ratingscale.draw()
    win.flip()
#Varaibles that are saved from the rating scale
nsrating_image1 = ratingscale.getRating()
nsrating_decisiontime_image1 = ratingscale.getRT()
nsrating_list_image1.append(nsrating_image1)
nsrating_decisiontime_list_image1.append(nsrating_decisiontime_image1)

    
#presents rating scale image 2
ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
item2 = visual.TextStim(win, "How likely is it that this picture will be followed by a loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
while ratingscale2.noResponse:
    image2_forratings.draw()
    item2.draw()
    ratingscale2.draw()
    win.flip()
    #variables saved for image 2
nsrating_image2 = ratingscale2.getRating()
nsrating_decisiontime_image2 = ratingscale2.getRT()
nsrating_list_image2.append(nsrating_image2)
nsrating_decisiontime_list_image2.append(nsrating_decisiontime_image2)


#Save data fro initial ratings in seperate file
ns_data = {'Image_1_rating':nsrating_list_image1, 'Image_1_rating_reactiontime':nsrating_decisiontime_list_image1, 'Image_2_rating':nsrating_list_image2, 'Image_2_rating_reactiontime':nsrating_decisiontime_list_image2}
df2 = pd.DataFrame.from_dict(ns_data, orient='index')
df2.transpose().to_csv(subj_id + '_neutral_stimuli_ratings.csv')



########Part three - Fear conditioning########

fixation.draw()
win.flip()

psychopy.core.wait(6)#wait 6 seconds

#creates random order of stimuli presentation

trials_per_stimuli_fc = 4#4 trials per stimuli (8 total), then contingency ratings displayed. This happens twice (16 trials) and if a certain threshold (i.e. contingencies have been learnt) then progresses
                          # to the next stage. If not meet threshold, this repeats (another 16 trials) until contingencies have been learnt. 


num = [1,2] #This is used to create random order of dtimuli presentation (coded this way so the numbers can be used in if statements to call the aversive noise)
trial_order = num*trials_per_stimuli_fc #Creates the trial list of 8 trials
random.shuffle(trial_order) #randomises trial order
print(trial_order) #for testing
trial_stimuli = [] #list that will contain the stimuli

for x in trial_order: #This loop appends the stiimuli in the order of the trials (same as trial_order) above
    if x == 1:
        trial_stimuli.append(image1)
    elif x ==2:
        trial_stimuli.append(image2)


clocker = psychopy.core.Clock() #starts the clock

#These are all the variables that will be saved during Fear conditioning

fcrating_list_image1 = [] 
fcrating_decisiontime_list_image1 = [] 
fcrating_list_image2 = []
fcrating_decisiontime_list_image2 = []
fc_trial_number = []
fc_delay_before_noise_play = []
contingency_rating_cs_plus = 0
contingency_rating_cs_minus = 0
contingency_learnt = 0
num_contingency_ratings = 0
trials_completed = 1

while contingency_learnt < 1: #Will not progress until contingencies are learnt
    
    for trial, number in zip(trial_stimuli, trial_order): #Loops through trial_stimuli (to display the stimuli) and trial_order (to deleiver aversive noise) in parallel
        clocker.reset() #resets the clock
        flag_sent = False # set to false so maker placed in spike only once (changed to True later once marker placed)
        while clocker.getTime() < pre_duration_s: #pre stimulus duration (i.e. nothing is displayed until this time point is reached)
            win.flip()
        while clocker.getTime() < pre_duration_s + stim_duration_s: #pre stimulus duration plus stimulus duration (waits for pre stim duration and then presents the stimuli for 100ms)
            trial.draw()
            while flag_sent == False:
                sendParallelTrigger(pport_address_out,255) # sends triggers for all trials (not cardiac timed here - useful for GSR analysis)
                flag_sent = True
            win.flip()
        
        
        win.flip()

        if number==1 and cond_num =='1':
            t_1 = clocker.getTime()
            psychopy.core.wait(1) #waits 1 seconds (safe period)
            rand_interval = round(random.randint(200,400)/100) #generates random time interval between 2 and 4 seconds (2nd,3rd or 4th second) - creates 2 second no noise period - still need key pressed in first second
            print(rand_interval) #for testing
            now = clocker.getTime()
            startle.play(when=now+rand_interval) #plays startle after 1 safe second but randomly between 1-4 seconds
            post_aversion_wait = 4 - (clocker.getTime()-t_1) #time remaining of the 3 second itnerval when the aversive noise is played
            psychopy.core.wait(post_aversion_wait) # waits this remaining time so whole thing takes 4 seconds
            fc_trial_number.append(trials_completed)
            fc_delay_before_noise_play.append(rand_interval)
            #get the time now
            now = clocker.getTime() #for testing
            print(now-t_1) #for testing
        elif number==2 and cond_num=='2':
            t_1 = clocker.getTime()
            psychopy.core.wait(1) #waits 1 seconds (safe period)
            rand_interval = round(random.randint(200,400)/100) #generates random time interval between 2 and 4 seconds 
            print(rand_interval) #for testing
            now = clocker.getTime()
            startle.play(when=now+rand_interval) #plays startle after 1 safe second but randomly between 1-4 seconds
            post_aversion_wait = 4 - (clocker.getTime()-t_1) #time remaining of the 3 second itnerval when the aversive noise is played
            psychopy.core.wait(post_aversion_wait) # waits this remaining time so whole thing takes 4 seconds
            fc_trial_number.append(trials_completed)
            fc_delay_before_noise_play.append(rand_interval)
            #get the time now
            now = clocker.getTime() #for testing
        else:
            psychopy.core.wait(4) #if no aveersive noise played, still need the post trial time interval (4 seconds)
        
        fixation.draw()
        win.flip()
        other_time = clocker.getTime()
        print(other_time)
        psychopy.core.wait(6) # Wait 6 seconds (inter-trial-interval)
        timer = clocker.getTime()
        print(timer)
        
        print(number)#for testing
        print(cond_num)#for testing
                
        
        trials_completed += 1
        
        psychopy.core.wait(6)#wait 6 seconds 
        
        
        
#Presents rating scale image 1
    ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
    item = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale.noResponse:
        image1_forratings.draw()
        item.draw()
        ratingscale.draw()
        win.flip()
    #Varaibles that are saved from the rating scale
    fcrating_image1 = ratingscale.getRating()
    fcrating_decisiontime_image1 = ratingscale.getRT()
    fcrating_list_image1.append(fcrating_image1)
    fcrating_decisiontime_list_image1.append(fcrating_decisiontime_image1)
    
    
    
#presents rating scale image 2
    ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
    item2 = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale2.noResponse:
        image2_forratings.draw()
        item2.draw()
        ratingscale2.draw()
        win.flip()
    #variables saved for image 2
    fcrating_image2 = ratingscale2.getRating()
    fcrating_decisiontime_image2 = ratingscale2.getRT()
    fcrating_list_image2.append(fcrating_image2)
    fcrating_decisiontime_list_image2.append(fcrating_decisiontime_image2)
    
    #cs+ and cs- contigencies saved (used to check if extra round of 8 trials is needed)
    if cond_num == '1':
        contingency_rating_cs_plus = int(fcrating_image1)
        contingency_rating_cs_minus = int(fcrating_image2)
    elif cond_num == '2':
        contingency_rating_cs_plus = int(fcrating_image2)
        contingency_rating_cs_minus = int(fcrating_image1)
    print(contingency_rating_cs_plus)
    print(contingency_rating_cs_minus)

    num_contingency_ratings += 1 #number of ratings completed - adds one each time
    #continues if only one round completed (as 2 needed minimum)
    if num_contingency_ratings <= 2:
        contingency_rating_cs_plus = 0 # reset here so can check contigency IF extra set of 8 trials is used (i.e. when contigencies not learnt)
        contingency_rating_cs_minus = 0
        #re-randomise trial order
        num = [1,2] 
        trial_order = num*trials_per_stimuli_fc 
        random.shuffle(trial_order) 
        print(trial_order) #for testing
        trial_stimuli = [] 
        for x in trial_order: #This loop appends the stiimuli in the order of the trials (same as trial_order) above
            if x == 1:
                trial_stimuli.append(image1)
            elif x ==2:
                trial_stimuli.append(image2)
                continue
    #contingecy learnt if true, progresses after 3 trials
    elif num_contingency_ratings == 3 and contingency_rating_cs_plus >= 7 and contingency_rating_cs_minus <= 3:
        contingency_learnt += 1
    #If above not true, does one more round of 8 trials then will progress
    elif num_contingency_ratings == 4:
        contingency_learnt += 1
    else:        
        #re randomise trial order
        num = [1,2] #This is used to create random order of stimuli presentation (coded this way so the numbers can be used in if statements to call the aversive noise)
        trial_order = num*trials_per_stimuli_fc #Creates the trial list of 8 trials
        random.shuffle(trial_order) #randomises trial order
        print(trial_order) #for testing
        trial_stimuli = [] #list that will contain the stimuli
        for x in trial_order: #This loop appends the stiimuli in the order of the trials (same as trial_order) above
            if x == 1:
                trial_stimuli.append(image1)
            elif x ==2:
                trial_stimuli.append(image2)
                continue
    
        
        

#Save data fro FC in seperate file
fc_data = {'Image_1_rating':fcrating_list_image1, 'Image_1_rating_reactiontime':fcrating_decisiontime_list_image1, 'Image_2_rating':fcrating_list_image2, 'Image_2_rating_reactiontime':fcrating_decisiontime_list_image2, 'Trial_number':fc_trial_number, 'delay_before_noise_play':fc_delay_before_noise_play}
df2 = pd.DataFrame.from_dict(fc_data, orient='index')
df2.transpose().to_csv(subj_id + '_fear_conditioning.csv') 

#fc_trial_data = [fcrating, fcrating_decisiontime] needs to be sorted

#exp_data.append(fc_trial_data)

########Part four - Avoidance learning########

#Avoidance instructions

instructions = visual.TextStim(win, text = 'During the next phase the spacebar will be available to press.\n\nPressing the spacebar may or may not cancel an upcoming loud noise.\n\nYou should REPEATEDLY press the spaebar to cancel the noise and you should press thre space bar in response to BOTH pictures.\n\nPress the spacebar to continue.')

instructions.draw()

win.flip()

psychopy.event.waitKeys() #press key to continue

#6 second pre trial fixation
fixation.draw()
win.flip()
psychopy.core.wait(6)#wait 6 seconds

#Avoidance learning

trials_per_stimuli_al = 4 #4 trials per stimuli (8 total), then contingency ratings displayed. This happens four times (32 trials) 
al_half_trials = 2 #as 2 stimuli so need cardiac cycle list for each i.e. half the length of the total stimuli                       


num = [1,2] #This is used to create random order of dtimuli presentation (coded this way so the numbers can be used in if statements to call the aversive noise)
trial_order_al = num*trials_per_stimuli_al #Creates the trial list of 8 trials
random.shuffle(trial_order_al) #randomises trial order

cardiac_cycle_image1 = num*al_half_trials
cardiac_cycle_image2 = num*al_half_trials #1 = systole, 2 = diastole
random.shuffle(cardiac_cycle_image1)
random.shuffle(cardiac_cycle_image2)

print(cardiac_cycle_image1)#for testing
print(cardiac_cycle_image2)

trial_stimuli_al = [] #list that will contain the stimuli

for x in trial_order_al: #This loop appends the stiimuli in the order of the trials (same as trial_order) above
    if x == 1:
        trial_stimuli_al.append(image1)
    elif x ==2:
        trial_stimuli_al.append(image2)


clocker.reset() #starts the clock

#These are all the variables that will be saved during avoidance learning
#Image ratings
alrating_list_image1 = []
alrating_decisiontime_list_image1 = []
alrating_list_image2 = []
alrating_decisiontime_list_image2 = []
#Avoidance behaviour  
al_avoidance_response_RT_systole_image1_shocktrial = []
al_systole_image1_shock_trial_num = []
testing = []
al_avoidance_response_RT_diastole_image1_shocktrial = []
al_diastole_image1_shock_trial_num = []
al_avoidance_response_RT_systole_image2_shocktrial = []
al_systole_image2_shock_trial_num = []
al_avoidance_response_RT_diastole_image2_shocktrial = []
al_diastole_image2_shock_trial_num = []
al_avoidance_response_RT_systole_image1_noshocktrial = []
al_systole_image1_noshock_trial_num = []
al_avoidance_response_RT_diastole_image1_noshocktrial = []
al_diastole_image1_noshock_trial_num = []
al_avoidance_response_RT_systole_image2_noshocktrial = []
al_systole_image2_noshock_trial_num = []
al_avoidance_response_RT_diastole_image2_noshocktrial = []
al_diastole_image2_noshock_trial_num = []
startle_trial_number = []
noise_played = []
al_when_noise_played_after_stim = [] #know how long after trial noise was played. Only saved on shock trials
al_noise_played_at_trial_number = []

trial_number = 0
#number of trials completed
cc_index_image1 = 0
cc_index_image2 = 0

#Cardiac timing variables
ppPresent = 1
HB_delay = 0.1
stim_counter   = 0
beats_recorded = 0
beat_1st = False
beat_max = 10
flag_sent = False

while trial_number < 16: #Can change this to alter total number of trials

    for trial, number in zip(trial_stimuli_al, trial_order_al): #Loops through trial_stimuli (to display the stimuli) and trial_order (to deleiver aversive noise) in parallel. Both lists are the same
            avoidance_key_pressed = None
            clocker.reset() #resets the clock
            while clocker.getTime() < pre_duration_s: #pre stimulus duration (i.e. nothing is displayed until this time point is reached)
                win.flip()
            
            if number == 1 and cardiac_cycle_image1[cc_index_image1] == 1: #image 1 systole trial
                #Systole trial (stim on R plus 250ms)
                while True:
                    signal_in = readParallelTrigger(pport_address_in)
                    y = time.time()
                    if signal_in > 63:
                         x = time.time()
                        #sendParallelTrigger(pport_address_out,255)
                         while time.time() < x + 0.350: #This would be 0.1 on a diastole trial (100ms presentation on the R-peak). Because we want systole (250ms after R) we add 250ms (=0.350) and the core.wait(0.25) for the stim/systole delay
                            if flag_sent == False:
                                core.wait(0.25)
                                sendParallelTrigger(pport_address_out,255)
                                flag_sent = True
                            trial.draw()
                            win.flip()
                         if time.time() > x + 0.350:
                            break
            
            if number == 1 and cardiac_cycle_image1[cc_index_image1] == 2: #image 1 diastole trial
                #Diastole trial (Stim on R wave)
                while True:
                   signal_in = readParallelTrigger(pport_address_in)
                   if signal_in > 63:
                       x = time.time()
                       #sendParallelTrigger(pport_address_out,255)
                       while time.time() < x + 0.1:
                           if flag_sent == False:
                               sendParallelTrigger(pport_address_out,255)
                               flag_sent = True
                           trial.draw()
                           win.flip()
                       if time.time() > x + 0.1:
                           break
            
            if number == 2 and cardiac_cycle_image2[cc_index_image2] == 1: #image 2 systole trial
                #Systole trial (stim on R plus 250ms)
                while True:
                    signal_in = readParallelTrigger(pport_address_in)
                    y = time.time()
                    if signal_in > 63:
                         x = time.time()
                        #sendParallelTrigger(pport_address_out,255)
                         while time.time() < x + 0.350: #This would be 0.1 on a diastole trial (100ms presentation on the R-peak). Because we want systole (250ms after R) we add 250ms (=0.350) and the core.wait(0.25) for the stim/systole delay
                            if flag_sent == False:
                                core.wait(0.25)
                                sendParallelTrigger(pport_address_out,255)
                                flag_sent = True
                            trial.draw()
                            win.flip()
                         if time.time() > x + 0.350:
                            break
            
            if number == 2 and cardiac_cycle_image2[cc_index_image2] == 2: #image 2 disatole trial
                #Diastole trial (Stim on R wave)
                while True:
                   signal_in = readParallelTrigger(pport_address_in)
                   if signal_in > 63:
                       x = time.time()
                       #sendParallelTrigger(pport_address_out,255)
                       while time.time() < x + 0.1:
                           if flag_sent == False:
                               sendParallelTrigger(pport_address_out,255)
                               flag_sent = True
                           trial.draw()
                           win.flip()
                       if time.time() > x + 0.1:
                           break

            counter = 0 # reset here - used to make sure only one -0 is appended to data sheet if no response made (rather than infinate)
            trial_number += 1
            mayshock = random.randint(1,2) #this is the 50% noise contingency. i.e. if the avoidance key pressed and this number == 2 then still shock (only way I could think to do it randomly)
            win.flip()

            
            if number==1 and cond_num =='1' and cardiac_cycle_image1[cc_index_image1] == 1:#systole trial for image1 with noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                al_when_noise_played_after_stim.append(rand_interval)
                al_noise_played_at_trial_number.append(trial_number)
                trial_list = [] #Trial list is used so the trial always starts with an empty list
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_systole_image1_shocktrial.append(KeyPressTime)
                        al_systole_image1_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_systole_image1_shock_trial_num.append(trial_number)
                        al_avoidance_response_RT_systole_image1_shocktrial.append(0)
                        counter+=1
                    prev_t = cur_t
                cc_index_image1 += 1 # This is so we can loop through the cardiac cycle using indexing as it doesn't work wit ha for loop (we need equal number of cardiac trials for each condition)
            elif number==1 and cond_num=='1' and cardiac_cycle_image1[cc_index_image1] == 2: #diastole trial image 1 with noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                al_when_noise_played_after_stim.append(rand_interval)
                al_noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_diastole_image1_shocktrial.append(KeyPressTime)
                        al_diastole_image1_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_diastole_image1_shock_trial_num.append(trial_number)
                        al_avoidance_response_RT_diastole_image1_shocktrial.append(0)
                        counter+=1
                    prev_t = cur_t
                cc_index_image1 += 1
            elif number == 1 and cond_num == '2' and cardiac_cycle_image1[cc_index_image1] == 1: #Systole trial image 1 with no noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_systole_image1_noshocktrial.append(KeyPressTime)
                        al_systole_image1_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_systole_image1_noshock_trial_num.append(trial_number)
                        al_avoidance_response_RT_systole_image1_noshocktrial.append(0)
                        counter+=1
                cc_index_image1 += 1
            elif number == 1 and cond_num == '2' and cardiac_cycle_image1[cc_index_image1] == 2: #diastole trial image 1 with no noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_diastole_image1_noshocktrial.append(KeyPressTime)
                        al_diastole_image1_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_diastole_image1_noshock_trial_num.append(trial_number)
                        al_avoidance_response_RT_diastole_image1_noshocktrial.append(0)
                        counter+=1
                cc_index_image1 += 1
            elif number == 2 and cond_num == '1' and cardiac_cycle_image2[cc_index_image2] == 1: #systole trial image 2  with no noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_systole_image2_noshocktrial.append(KeyPressTime)
                        al_systole_image2_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_systole_image2_noshock_trial_num.append(trial_number)
                        al_avoidance_response_RT_systole_image2_noshocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '1' and cardiac_cycle_image2[cc_index_image2] == 2: #diastole trial image 2 with no noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_diastole_image2_noshocktrial.append(KeyPressTime)
                        al_diastole_image2_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_diastole_image2_noshock_trial_num.append(trial_number)
                        al_avoidance_response_RT_diastole_image2_noshocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '2' and cardiac_cycle_image2[cc_index_image2] == 1: #systole trial image 2 with noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                al_when_noise_played_after_stim.append(rand_interval)
                al_noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_systole_image2_shocktrial.append(KeyPressTime)
                        al_systole_image2_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_systole_image2_shock_trial_num.append(trial_number)
                        al_avoidance_response_RT_systole_image2_shocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '2' and cardiac_cycle_image2[cc_index_image2] == 2: #diastole trial image 2 with noise
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                al_when_noise_played_after_stim.append(rand_interval)
                al_noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        al_avoidance_response_RT_diastole_image2_shocktrial.append(KeyPressTime)
                        al_diastole_image2_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        al_diastole_image2_shock_trial_num.append(trial_number)
                        al_avoidance_response_RT_diastole_image2_shocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            avoidance_key_pressed = None #has to be reset here to work in loop
            
            flag_sent = False #reset for cardiac timing here (so flag sent on each trial)
            trial_list = [] # reset the trial list for each trial
            fixation.draw()
            win.flip()
            other_time = clocker.getTime()
            print(other_time)
            psychopy.core.wait(6) # Wait 6 seconds (inter-trial-interval)
            timer = clocker.getTime()
            print(timer)
            
        
            #psychopy.core.wait(6)#wait 6 seconds 

        
       
        #Presents rating scale image 1 #Should have the same number of ratings per participant so dont need to track trial number
    ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
    item = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale.noResponse:
        image1_forratings.draw()
        item.draw()
        ratingscale.draw()
        win.flip()
    #Varaibles that are saved from the rating scale
    alrating_image1 = ratingscale.getRating()
    alrating_list_image1.append(alrating_image1)
    alrating_decisiontime_image1 = ratingscale.getRT()
    alrating_decisiontime_list_image1.append(alrating_decisiontime_image1)

    
    #presents rating scale image 2
    ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
    item2 = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale2.noResponse:
        image2_forratings.draw()
        item2.draw()
        ratingscale2.draw()
        win.flip()
    #variables saved for image 2
    alrating_image2 = ratingscale2.getRating()
    alrating_decisiontime_image2 = ratingscale2.getRT()
    alrating_list_image2.append(alrating_image2)
    alrating_decisiontime_list_image2.append(alrating_decisiontime_image2)
    
    cc_index_image1 = 0 #resets the indexing after end of first round of trials_completed
    cc_index_image2 = 0




al_data = {'Noise_played_trial_number':al_noise_played_at_trial_number, 'Noise_played_after_stim_duration':al_when_noise_played_after_stim,'Image_1_rating':alrating_list_image1, 'Image_1_rating_reactiontime':alrating_decisiontime_list_image1, 'Image_2_rating':alrating_list_image2, 'Image_2_rating_reactiontime':alrating_decisiontime_list_image2, 'Systole_image1_shock_trialnum':al_systole_image1_shock_trial_num, 'AL_RT_systole_image1_shock_trial':al_avoidance_response_RT_systole_image1_shocktrial, 'Diastole_image1_shock_trialnum':al_diastole_image1_shock_trial_num, 'AL_RT_Diastole_image1_shock_trial': al_avoidance_response_RT_diastole_image1_shocktrial,
           'Systole_image2_shock_trialnum':al_systole_image2_shock_trial_num, 'AL_RT_systole_image2_shock_trial':al_avoidance_response_RT_systole_image2_shocktrial,'Diastole_image2_shock_trialnum':al_diastole_image2_shock_trial_num, 'AL_RT_diastole_image2_shock_trial':al_avoidance_response_RT_diastole_image2_shocktrial, 'Systole_image1_NOshock_trialnum':al_systole_image1_noshock_trial_num, 'AL_RT_systole_image1_NOshock_trial':al_avoidance_response_RT_systole_image1_noshocktrial, 'Diastole_image1_NOshock_trialnum':al_diastole_image1_noshock_trial_num, 'AL_RT_Diastole_image1_NOshock_trial': al_avoidance_response_RT_diastole_image1_noshocktrial,
           'Systole_image2_NOshock_trialnum':al_systole_image2_noshock_trial_num, 'AL_RT_systole_image2_NOshock_trial':al_avoidance_response_RT_systole_image2_noshocktrial,
           'Diastole_Image2_NOshock_trial_num':al_diastole_image2_noshock_trial_num, 'AL_RT_diastole_image2_NOshock_trial':al_avoidance_response_RT_diastole_image2_noshocktrial, 'Trial_number_startle_played(despite_avoidance_key_pressed)':startle_trial_number, 'Startle_played?':noise_played}
df3 = pd.DataFrame.from_dict(al_data, orient='index')
df3.transpose().to_csv(subj_id + '_avoidance_learning.csv')


########Part five - Test phase ########

#Test instructions

instructions = visual.TextStim(win, text = 'The next phase is the same as the previous.\n\nREPEATEDLY pressing the spaebar may or may not cancel the noise and you should press the space bar in response to BOTH pictures.\n\nPress the spacebar to continue.')

instructions.draw()

win.flip()

psychopy.event.waitKeys() #press key to continue

#6 second pre trial fixation
fixation.draw()
win.flip()
psychopy.core.wait(6)#wait 6 seconds

#Test phase

trials_per_stimuli_t = 4 #4 trials per stimuli (8 total), then contingency ratings displayed. This happens four times (32 trials) 
t_half_trials = 2 #as 2 stimuli so need cardiac cycle list for each i.e. half the length of the total stimuli                       


num = [1,2] #This is used to create random order of dtimuli presentation (coded this way so the numbers can be used in if statements to call the aversive noise)
trial_order_t = num*trials_per_stimuli_t #Creates the trial list of 8 trials
random.shuffle(trial_order_t) #randomises trial order

cardiac_cycle_image1 = num*t_half_trials
cardiac_cycle_image2 = num*t_half_trials #1 = systole, 2 = diastole
random.shuffle(cardiac_cycle_image1)
random.shuffle(cardiac_cycle_image2)

print(cardiac_cycle_image1)#for testing
print(cardiac_cycle_image2)

trial_stimuli_t = [] #list that will contain the stimuli

for x in trial_order_t: #This loop appends the stiimuli in the order of the trials (same as trial_order) above
    if x == 1:
        trial_stimuli_t.append(image1)
    elif x ==2:
        trial_stimuli_t.append(image2)


clocker.reset() #starts the clock

#These are all the variables that will be saved during avoidance learning
#Image ratings
trating_list_image1 = []
trating_decisiontime_list_image1 = []
trating_list_image2 = []
trating_decisiontime_list_image2 = []
#Avoidance behaviour  
t_avoidance_response_RT_systole_image1_shocktrial = []
t_systole_image1_shock_trial_num = []
t_avoidance_response_RT_diastole_image1_shocktrial = []
t_diastole_image1_shock_trial_num = []
t_avoidance_response_RT_systole_image2_shocktrial = []
t_systole_image2_shock_trial_num = []
t_avoidance_response_RT_diastole_image2_shocktrial = []
t_diastole_image2_shock_trial_num = []
t_avoidance_response_RT_systole_image1_noshocktrial = []
t_systole_image1_noshock_trial_num = []
t_avoidance_response_RT_diastole_image1_noshocktrial = []
t_diastole_image1_noshock_trial_num = []
t_avoidance_response_RT_systole_image2_noshocktrial = []
t_systole_image2_noshock_trial_num = []
t_avoidance_response_RT_diastole_image2_noshocktrial = []
t_diastole_image2_noshock_trial_num = []
startle_trial_number = []
noise_played = []
when_noise_played_after_stim = [] #know how long after trial noise was played. Only saved on shock trials
noise_played_at_trial_number = []
trial_number = 0
#number of trials completed
trials_completed_t = 0
cc_index_image1 = 0
cc_index_image2 = 0

#Cardiac timing variables
ppPresent = 1
HB_delay = 0.1
stim_counter   = 0
beats_recorded = 0
beat_1st = False
beat_max = 10
flag_sent = False

while trial_number < 64: #Can change this to alter total number of trials

    for trial, number in zip(trial_stimuli_t, trial_order_t): #Loops through trial_stimuli (to display the stimuli) and trial_order (to deleiver aversive noise) in parallel. Both lists are the same
            avoidance_key_pressed = None
            clocker.reset() #resets the clock
            while clocker.getTime() < pre_duration_s: #pre stimulus duration (i.e. nothing is displayed until this time point is reached)
                win.flip()
            
            if number == 1 and cardiac_cycle_image1[cc_index_image1] == 1: #image 1 systole trial
                #Systole trial (stim on R plus 250ms)
                while True:
                    signal_in = readParallelTrigger(pport_address_in)
                    y = time.time()
                    if signal_in > 63:
                         x = time.time()
                        #sendParallelTrigger(pport_address_out,255)
                         while time.time() < x + 0.350: #This would be 0.1 on a diastole trial (100ms presentation on the R-peak). Because we want systole (250ms after R) we add 250ms (=0.350) and the core.wait(0.25) for the stim/systole delay
                            if flag_sent == False:
                                core.wait(0.25)
                                sendParallelTrigger(pport_address_out,255)
                                flag_sent = True
                            trial.draw()
                            win.flip()
                         if time.time() > x + 0.350:
                            break
            
            if number == 1 and cardiac_cycle_image1[cc_index_image1] == 2: #image 1 diastole trial
                #Diastole trial (Stim on R wave)
                while True:
                   signal_in = readParallelTrigger(pport_address_in)
                   if signal_in > 63:
                       x = time.time()
                       #sendParallelTrigger(pport_address_out,255)
                       while time.time() < x + 0.1:
                           if flag_sent == False:
                               sendParallelTrigger(pport_address_out,255)
                               flag_sent = True
                           trial.draw()
                           win.flip()
                       if time.time() > x + 0.1:
                           break
            
            if number == 2 and cardiac_cycle_image2[cc_index_image2] == 1: #image 2 systole trial
                #Systole trial (stim on R plus 250ms)
                while True:
                    signal_in = readParallelTrigger(pport_address_in)
                    y = time.time()
                    if signal_in > 63:
                         x = time.time()
                        #sendParallelTrigger(pport_address_out,255)
                         while time.time() < x + 0.350: #This would be 0.1 on a diastole trial (100ms presentation on the R-peak). Because we want systole (250ms after R) we add 250ms (=0.350) and the core.wait(0.25) for the stim/systole delay
                            if flag_sent == False:
                                core.wait(0.25)
                                sendParallelTrigger(pport_address_out,255)
                                flag_sent = True
                            trial.draw()
                            win.flip()
                         if time.time() > x + 0.350:
                            break
            
            if number == 2 and cardiac_cycle_image2[cc_index_image2] == 2: #image 2 disatole trial
                #Diastole trial (Stim on R wave)
                while True:
                   signal_in = readParallelTrigger(pport_address_in)
                   if signal_in > 63:
                       x = time.time()
                       #sendParallelTrigger(pport_address_out,255)
                       while time.time() < x + 0.1:
                           if flag_sent == False:
                               sendParallelTrigger(pport_address_out,255)
                               flag_sent = True
                           trial.draw()
                           win.flip()
                       if time.time() > x + 0.1:
                           break

            counter = 0 # reset here - used to make sure only one -0 is appended to data sheet if no response made (rather than infinate)
            trial_number += 1
            mayshock = random.randint(1,2) #this is the 50% shock contingency. i.e. if the avoidance key pressed and this number == 2 then still shock (only way I could think to do it randomly)
            win.flip()
            
            if number==1 and cond_num =='1' and cardiac_cycle_image1[cc_index_image1] == 1:#systole trial for image1 with shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                when_noise_played_after_stim.append(rand_interval)
                noise_played_at_trial_number.append(trial_number)
                trial_list = [] #Trial list is used so the trial always starts with an empty list
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_systole_image1_shocktrial.append(KeyPressTime)
                        t_systole_image1_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_systole_image1_shock_trial_num.append(trial_number)
                        t_avoidance_response_RT_systole_image1_shocktrial.append(0)
                        counter+=1
                    prev_t = cur_t
                cc_index_image1 += 1 # This is so we can loop tthrough the cardiac cycle using indexing as it doesn't work wit ha for loop (we need equal number of cardiac trials for each condition)
            elif number==1 and cond_num=='1' and cardiac_cycle_image1[cc_index_image1] == 2: #diastole trial image 1 with shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                when_noise_played_after_stim.append(rand_interval)
                noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_diastole_image1_shocktrial.append(KeyPressTime)
                        t_diastole_image1_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_diastole_image1_shock_trial_num.append(trial_number)
                        t_avoidance_response_RT_diastole_image1_shocktrial.append(0)
                        counter+=1
                    prev_t = cur_t
                cc_index_image1 += 1
            elif number == 1 and cond_num == '2' and cardiac_cycle_image1[cc_index_image1] == 1: #Systole trial image 1 with no shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_systole_image1_noshocktrial.append(KeyPressTime)
                        t_systole_image1_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_systole_image1_noshock_trial_num.append(trial_number)
                        t_avoidance_response_RT_systole_image1_noshocktrial.append(0)
                        counter+=1
                cc_index_image1 += 1
            elif number == 1 and cond_num == '2' and cardiac_cycle_image1[cc_index_image1] == 2: #diastole trial image 1 with no shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_diastole_image1_noshocktrial.append(KeyPressTime)
                        t_diastole_image1_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_diastole_image1_noshock_trial_num.append(trial_number)
                        t_avoidance_response_RT_diastole_image1_noshocktrial.append(0)
                        counter+=1
                cc_index_image1 += 1
            elif number == 2 and cond_num == '1' and cardiac_cycle_image2[cc_index_image2] == 1: #systole trial image 2  with no shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_systole_image2_noshocktrial.append(KeyPressTime)
                        t_systole_image2_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_systole_image2_noshock_trial_num.append(trial_number)
                        t_avoidance_response_RT_systole_image2_noshocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '1' and cardiac_cycle_image2[cc_index_image2] == 2: #diastole trial image 2 with no shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 : #may need to change this if duration changes (This just does nothing for 4 seconds - still records key presses)
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_diastole_image2_noshocktrial.append(KeyPressTime)
                        t_diastole_image2_noshock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_diastole_image2_noshock_trial_num.append(trial_number)
                        t_avoidance_response_RT_diastole_image2_noshocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '2' and cardiac_cycle_image2[cc_index_image2] == 1: #systole trial image 2 with shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                when_noise_played_after_stim.append(rand_interval)
                noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_systole_image2_shocktrial.append(KeyPressTime)
                        t_systole_image2_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_systole_image2_shock_trial_num.append(trial_number)
                        t_avoidance_response_RT_systole_image2_shocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            elif number == 2 and cond_num == '2' and cardiac_cycle_image2[cc_index_image2] == 2: #diastole trial image 2 with shock
                clock = psychopy.core.Clock() #starts the clock
                start_trial = clock.getTime()
                trial_clock = core.Clock()
                KeyResp = None
                prev_t = 0
                rand_interval = round(random.randint(200,400)/100)
                when_noise_played_after_stim.append(rand_interval)
                noise_played_at_trial_number.append(trial_number)
                trial_list = []
                #print(mayshock)
                while  trial_clock.getTime() <= 5 :
                    # get key press and then disappear
                    win.flip()
                    KeyResp, Resp, KeyPressTime = get_keyboard(
                                    clock, ['space'], ['space'])
                    if KeyResp == 'space':                
                        print(KeyResp)
                        print(KeyPressTime)
                        t_avoidance_response_RT_diastole_image2_shocktrial.append(KeyPressTime)
                        t_diastole_image2_shock_trial_num.append(trial_number)
                        trial_list.append(KeyPressTime)
                    
                    cur_t = trial_clock.getTime()
                    if int(cur_t) == rand_interval and int(cur_t) - int(prev_t)== 1:  # condition for avoidance behaviour
                        #print('4 sec', cur_t)
                        if  len(trial_list)== 0 or trial_list[0] >1:
                            startle.play() # replace with sound playing function
                        elif len(trial_list) > 0 and trial_list[0] < 1 and mayshock == 2: #if avoidance key pressed in right place at right time, still shock on 50% of trials (i.e. when mayshock == 2)
                            startle.play()
                            startle_trial_number.append(trial_number)
                            noise_played.append('Noise_played')
                        else:
                            pass
                    if len(trial_list) < 1 and counter == 0: # if no response made append the trial number and a 0
                        t_diastole_image2_shock_trial_num.append(trial_number)
                        t_avoidance_response_RT_diastole_image2_shocktrial.append(0)
                        counter+=1
                cc_index_image2 += 1
            avoidance_key_pressed = None #has to be reset here to work in loop
            
            flag_sent = False #reset for cardiac timing here (so flag sent on each trial)
            trial_list = [] # reset the trial list for each trial
            fixation.draw()
            win.flip()
            other_time = clocker.getTime()
            print(other_time)
            psychopy.core.wait(6) # Wait 6 seconds (inter-trial-interval)
            timer = clocker.getTime()
            print(timer)
            
        
            #psychopy.core.wait(6)#wait 6 seconds 

        
       
    #Presents rating scale image 1 #Should have the same number of ratings per participant so dont need to track trial number
    ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
    item = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale.noResponse:
        image1_forratings.draw()
        item.draw()
        ratingscale.draw()
        win.flip()
    #Varaibles that are saved from the rating scale
    trating_image1 = ratingscale.getRating()
    trating_list_image1.append(trating_image1)
    trating_decisiontime_image1 = ratingscale.getRT()
    trating_decisiontime_list_image1.append(trating_decisiontime_image1)

    
    #presents rating scale image 2
    ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
    item2 = visual.TextStim(win, "How likely was the loud noise?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
    while ratingscale2.noResponse:
        image2_forratings.draw()
        item2.draw()
        ratingscale2.draw()
        win.flip()
    #variables saved for image 2
    trating_image2 = ratingscale2.getRating()
    trating_decisiontime_image2 = ratingscale2.getRT()
    trating_list_image2.append(trating_image2)
    trating_decisiontime_list_image2.append(trating_decisiontime_image2)
    
    cc_index_image1 = 0 #resets the indexing after end of first round of trials_completed
    cc_index_image2 = 0




test_data = {'Noise_played_trial_number':noise_played_at_trial_number, 'Noise_played_after_stim_duration':when_noise_played_after_stim, 'Image_1_rating':trating_list_image1, 'Image_1_rating_reactiontime':trating_decisiontime_list_image1, 'Image_2_rating':trating_list_image2, 'Image_2_rating_reactiontime':trating_decisiontime_list_image2, 'Systole_image1_shock_trialnum':t_systole_image1_shock_trial_num, 't_RT_systole_image1_shock_trial':t_avoidance_response_RT_systole_image1_shocktrial, 'Diastole_image1_shock_trialnum':t_diastole_image1_shock_trial_num, 't_RT_Diastole_image1_shock_trial': t_avoidance_response_RT_diastole_image1_shocktrial,
           'Systole_image2_shock_trialnum':t_systole_image2_shock_trial_num, 't_RT_systole_image2_shock_trial':t_avoidance_response_RT_systole_image2_shocktrial,'Diastole_image2_shock_trialnum':t_diastole_image2_shock_trial_num, 't_RT_diastole_image2_shock_trial':t_avoidance_response_RT_diastole_image2_shocktrial, 'Systole_image1_NOshock_trialnum':t_systole_image1_noshock_trial_num, 't_RT_systole_image1_NOshock_trial':t_avoidance_response_RT_systole_image1_noshocktrial, 'Diastole_image1_NOshock_trialnum':t_diastole_image1_noshock_trial_num, 't_RT_Diastole_image1_NOshock_trial': t_avoidance_response_RT_diastole_image1_noshocktrial,
           'Systole_image2_NOshock_trialnum':t_systole_image2_noshock_trial_num, 't_RT_systole_image2_NOshock_trial':t_avoidance_response_RT_systole_image2_noshocktrial,
           'Diastole_Image2_NOshock_trial_num':t_diastole_image2_noshock_trial_num, 't_RT_diastole_image2_NOshock_trial':t_avoidance_response_RT_diastole_image2_noshocktrial, 'Trial_number_startle_played(despite_avoidance_key_pressed)':startle_trial_number, 'Startle_played?':noise_played}
df3 = pd.DataFrame.from_dict(test_data, orient='index')
df3.transpose().to_csv(subj_id + '_test_phase.csv')


#####Part 6 - post trial stiumulus ratings#####
#Only need to do the anxiety questions as the last part of the test phase does the how likely is the loud noise questions

#Variables saved
erating_list_image1_pleasant = []
erating_decisiontime_list_image1_pleasant = []
erating_list_image2_pleasant = []
erating_decisiontime_list_image2_pleasant = []
erating_list_image1_anxiety = []
erating_decisiontime_list_image1_anxiety = []
erating_list_image2_anxiety = []
erating_decisiontime_list_image2_anxiety = []

#Pleasant questions
ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
item = visual.TextStim(win, "How pleasant do you find this picture?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
while ratingscale.noResponse:
    image1_forratings.draw()
    item.draw()
    ratingscale.draw()
    win.flip()
#Varaibles that are saved from the rating scale
erating_image1 = ratingscale.getRating()
erating_list_image1_pleasant.append(erating_image1)
erating_decisiontime_image1 = ratingscale.getRT()
erating_decisiontime_list_image1_pleasant.append(erating_decisiontime_image1)

    
    #presents rating scale image 2
ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
item2 = visual.TextStim(win, "How pleasant do you find this picture?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
while ratingscale2.noResponse:
    image2_forratings.draw()
    item2.draw()
    ratingscale2.draw()
    win.flip()
#variables saved for image 2
erating_image2 = ratingscale2.getRating()
erating_decisiontime_image2 = ratingscale2.getRT()
erating_list_image2_pleasant.append(erating_image2)
erating_decisiontime_list_image2_pleasant.append(erating_decisiontime_image2)

#Anxiety questions
ratingscale = visual.RatingScale(win, low = 1, high = 10, stretch = 2) 
item = visual.TextStim(win, "How anxious does this picture make you feel?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
while ratingscale.noResponse:
    image1_forratings.draw()
    item.draw()
    ratingscale.draw()
    win.flip()
#Varaibles that are saved from the rating scale
erating_image1 = ratingscale.getRating()
erating_list_image1_anxiety.append(erating_image1)
erating_decisiontime_image1 = ratingscale.getRT()
erating_decisiontime_list_image1_anxiety.append(erating_decisiontime_image1)

    
#presents rating scale image 2
ratingscale2 = visual.RatingScale(win, low = 1, high = 10, stretch = 2)
item2 = visual.TextStim(win, "How anxious does this picture make you feel?\n\nLeft click with the mouse on the scale and then click the button at the bottom of the screen to confirm")
while ratingscale2.noResponse:
    image2_forratings.draw()
    item2.draw()
    ratingscale2.draw()
    win.flip()
#variables saved for image 2
erating_image2 = ratingscale2.getRating()
erating_decisiontime_image2 = ratingscale2.getRT()
erating_list_image2_anxiety.append(erating_image2)
erating_decisiontime_list_image2_anxiety.append(erating_decisiontime_image2)


#Save variables from this phase
evaluative_data = {'Image1_pleasantness':erating_list_image1_pleasant, 'Image1_pleasantness_RT':erating_decisiontime_list_image1_pleasant, 'Image2_plesantness':erating_list_image2_pleasant, 'Image2_plesantness_RT':erating_decisiontime_list_image2_pleasant,
                    'Image1_anxiety':erating_list_image1_anxiety, 'Image1_anxiety_RT':erating_decisiontime_list_image1_anxiety, 'Image2_anxiety':erating_list_image2_anxiety, 'Image2_anxiety_RT':erating_decisiontime_list_image2_anxiety}
df3 = pd.DataFrame.from_dict(evaluative_data, orient='index')
df3.transpose().to_csv(subj_id + '_stimuli_evaluation.csv')



instructions = visual.TextStim(win, text = 'End of experiment.\n\nPlease contact the researcher.\n\nThank you for taking part.')

instructions.draw()

win.flip()

psychopy.event.waitKeys() #press key to continue




win.close()






####unused could be useful code####

#for empty trial WILL NEED
#if keys != None:
 #   if 'up' in keys:
  #      line.length += 0.5
   # if 'down' in keys:
    #    line.length -= 0.5
#else:
#    pass  # you can do something explicitly on missing response here.

#scale rating scale#

    #rating scale
#    minload = 0
#    maxload = 100
#    loanrange = range(minload, maxload+1, 1)
#    labelpoints = [0, 0.5, 1]
#    labels = [str(int(maxload*point)) for point in labelpoints]
#    ticks = [len(loanrange)*point for point in labelpoints]
#    ratingscale = visual.RatingScale(win, choices = loanrange, labels = labels, tickMarks = ticks, stretch = 2)
#    item = visual.TextStim(win, "Test")
#    while ratingscale.noResponse:
#        item.draw()
#        ratingscale.draw()
#        win.flip()
#        rating = ratingscale.getRating()
#        decisiontime = ratingscale.getRT()
#        
#    win.flip()


#import images#

#image1 = psychopy.visual.ImageStim(
#    win=win,
#    image="image1.png",
#    units="pix"
#)
#
#image2 = psychopy.visual.ImageStim(
#    win=win,
#    image="image2.png",
#    units="pix"
#)
#
#image3 = psychopy.visual.ImageStim(
#    win=win,
#    image="image3.png",
#    units="pix"
#)
