#All imports
import pandas as pd
import numpy as np
import math
import os
import glob

#Functions
def Average(lst): 
    return sum(lst) / len(lst)

#Create participant lsit
px_list = [i.split('/')[-1] for i in glob.glob('//Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/D1*')]

for ID in px_list:
    #####Neutral_stim_ratings####
    ns = pd.read_csv("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}/{}_neutral_stimuli_ratings.csv".format(ID,ID))
    #Image 1
    ns_image1_rating = [ns.iloc[0]['Image_1_rating']]
    ns_image1_rt = [ns.iloc[0]['Image_1_rating_reactiontime']]
    #Image 2
    ns_image2_rating = [ns.iloc[0]["Image_2_rating"]]
    ns_image2_rt = [ns.iloc[0]["Image_2_rating_reactiontime"]]

    ####Fear_conditioning####
    fc = pd.read_csv("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}/{}_fear_conditioning.csv".format(ID,ID))
    #Variables to save
    number_of_ratings_per_stim = [len(fc['Image_1_rating'])]
    #Image1
    fc_mean_image1_rating = [fc['Image_1_rating'].mean(skipna = True)]
    fc_mean_image1_rating_RT = [fc['Image_1_rating_reactiontime'].mean(skipna = True)]
    #Image2
    fc_mean_image2_rating = [fc['Image_2_rating'].mean(skipna = True)]
    fc_mean_image2_rating_RT = [fc['Image_2_rating_reactiontime'].mean(skipna = True)]
    group = [1]

    ####Avoidance_Learning####
    df = pd.read_csv("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}/{}_avoidance_learning.csv".format(ID,ID))
    #Image rating extractions and variables to save
    #Image 1
    al_mean_image1_rating = [df['Image_1_rating'].mean(skipna = True)]
    al_mean_image1_rating_RT = [df['Image_1_rating_reactiontime'].mean(skipna = True)]
    #Image2
    al_mean_image2_rating = [df['Image_2_rating'].mean(skipna = True)]
    al_mean_image2_rating_RT = [df['Image_2_rating_reactiontime'].mean(skipna = True)]

    #calculate average time interval between avoidance response and noise play for this participant Test phase
    trials_with_noise_play = df['Noise_played_trial_number'].tolist() #creates list
    cleanedList_trials = [x for x in trials_with_noise_play if str(x) != 'nan'] #removes nan values
    delay_with_noise_play = df['Noise_played_after_stim_duration'].tolist()
    cleanedList_noise = [x for x in delay_with_noise_play if str(x) != 'nan']
    trialnum_list1 = df['Systole_image1_shock_trialnum'].tolist()#converts column to list
    trialnum_list2 = df['Diastole_image1_shock_trialnum'].tolist()#converts column to list
    delays_systole_image1_shock = []
    delays_diastole_image1_shock = []
    for a in cleanedList_trials: #Checks for occurance of trial number in trial list, if yes, appends the delay 
        if a in trialnum_list1:
            a_index = trials_with_noise_play.index(a)
            delays_systole_image1_shock.append(cleanedList_noise[a_index])
        elif a in trialnum_list2:
            a_index = trials_with_noise_play.index(a)
            delays_diastole_image1_shock.append(cleanedList_noise[a_index])
    #saving variables
    mean_delay_systole_shock = Average(delays_systole_image1_shock)
    mean_delay_diastole_shock = Average(delays_diastole_image1_shock)
    #Calculate amount of times avoidance key pressed but noise still played (should be roughly 50%)
    avoidance_pressed_right_and_still_startle = df['Trial_number_startle_played(despite_avoidance_key_pressed)'].tolist()
    cleaned_aprass = [x for x in avoidance_pressed_right_and_still_startle if str(x) != 'nan']
    count_systole_still_shock_despite_avoidance = 0
    count_diastole_still_shock_despite_avoidance = 0
    for a in cleaned_aprass:
        if a in trialnum_list1:
            count_systole_still_shock_despite_avoidance += 1
        elif a in trialnum_list2:
            count_diastole_still_shock_despite_avoidance += 1
    #variables to save
    al_mean_delay_systole_shock = [mean_delay_systole_shock]
    al_mean_delay_diastole_shock = [mean_delay_diastole_shock]
    al_count_systole_still_shock_despite_avoidance = [count_systole_still_shock_despite_avoidance]
    al_count_diastole_still_shock_despite_avoidance = [count_diastole_still_shock_despite_avoidance]

    #Systole image 1 shock
    list_of_trial_numbers = []
    trial_numbers_systole_shock = df['Systole_image1_shock_trialnum'].tolist() #creates list
    cleanedList_trials_systole_s = [x for x in trial_numbers_systole_shock if str(x) != 'nan'] #removes nan values
    rt_systole_shock = df['AL_RT_systole_image1_shock_trial'].tolist()
    cleanedList_rt_systole_s = [x for x in rt_systole_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_s) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_systole_s[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_systole_s[x] != cleanedList_trials_systole_s[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_s) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_systole_s = [i for j, i in enumerate(cleanedList_rt_systole_s) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_systole_s[x] = 0
    cleanedList_trials_systole_s = [value for value in cleanedList_trials_systole_s if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    systole_image1_shock_count = []
    systole_image1_shock_rt = []
    #calculates number of trials in which response was made so below 4 loop can work (otherwise indexing is wrong)
    if total_no_response_trials > 0:
        rangenum = 3 - total_no_response_trials
    else:
        rangenum = 3
    #trial 1
    num = cleanedList_trials_systole_s[0] #assigns first value (trial number) to num
    systole_image1_shock_count.append(cleanedList_trials_systole_s.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    systole_image1_shock_rt.append(cleanedList_rt_systole_s[num_for_rt])
    for x in range(rangenum):#change number to number of remaining trials
        num = cleanedList_trials_systole_s[sum(systole_image1_shock_count)] #sum list (for index as this is reccursive) 
        num_for_rt = int(sum(systole_image1_shock_count)) #need index to be total count of trials so far
        systole_image1_shock_count.append(cleanedList_trials_systole_s.count(num))
        systole_image1_shock_rt.append(cleanedList_rt_systole_s[num_for_rt])
    #Varaibles to save
    al_mean_num_responses_systole_csplus = [Average(systole_image1_shock_count)]
    al_mean_rt_systole_csplus = [Average(systole_image1_shock_rt)]
    al_total_response_trials_systoloe_csplus = [16 - total_no_response_trials]
    al_total_no_response_trials_systole_csplus = [total_no_response_trials]

    #Diastole image 1 shock
    list_of_trial_numbers = []
    trial_numbers_diastole_shock = df['Diastole_image1_shock_trialnum'].tolist() #creates list
    cleanedList_trials_diastole_s = [x for x in trial_numbers_diastole_shock if str(x) != 'nan'] #removes nan values
    rt_diastole_shock = df['AL_RT_Diastole_image1_shock_trial'].tolist()
    cleanedList_rt_diastole_s = [x for x in rt_diastole_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_s) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_diastole_s[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_diastole_s[x] != cleanedList_trials_diastole_s[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_s) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_diastole_s = [i for j, i in enumerate(cleanedList_rt_diastole_s) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_diastole_s[x] = 0  
    cleanedList_trials_diastole_s = [value for value in cleanedList_trials_diastole_s if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    diastole_image1_shock_count = []
    diastole_image1_shock_rt = []
    #trial 1
    num = cleanedList_trials_diastole_s[0] #assigns first value (trial number) to num
    diastole_image1_shock_count.append(cleanedList_trials_diastole_s.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    diastole_image1_shock_rt.append(cleanedList_rt_diastole_s[num_for_rt])
    print(diastole_image1_shock_count)
    print(cleanedList_trials_diastole_s)
    #calculates number of trials in which response was made so below 4 loop can work (otherwise indexing is wrong)
    if total_no_response_trials > 0:
        rangenum = 3 - total_no_response_trials
    else:
        rangenum = 3
    for x in range(rangenum):
        num = cleanedList_trials_diastole_s[sum(diastole_image1_shock_count)] 
        print(num)
        num_for_rt = int(sum(diastole_image1_shock_count)) 
        diastole_image1_shock_count.append(cleanedList_trials_diastole_s.count(num))
        diastole_image1_shock_rt.append(cleanedList_rt_diastole_s[num_for_rt])
    #Varaibles to save
    al_mean_num_responses_diastole_csplus = [Average(diastole_image1_shock_count)]
    al_mean_rt_diastole_csplus = [Average(diastole_image1_shock_rt)]
    al_total_response_trials_diastole_csplus = [16 - total_no_response_trials] 
    al_total_no_response_trials_diastole_csplus = [total_no_response_trials]

    #Systole image 2 no shock
    list_of_trial_numbers = []
    trial_numbers_systole_no_shock = df['Systole_image2_NOshock_trialnum'].tolist() #creates list
    cleanedList_trials_systole_ns = [x for x in trial_numbers_systole_no_shock if str(x) != 'nan'] #removes nan values
    rt_systole_no_shock = df['AL_RT_systole_image2_NOshock_trial'].tolist()
    cleanedList_rt_systole_ns = [x for x in rt_systole_no_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_ns) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_systole_ns[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_systole_ns[x] != cleanedList_trials_systole_ns[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_ns) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_systole_ns = [i for j, i in enumerate(cleanedList_rt_systole_ns) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_systole_ns[x] = 0 
    cleanedList_trials_systole_ns = [value for value in cleanedList_trials_systole_ns if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    systole_image2_noshock_count = []
    systole_image2_noshock_rt = []
    if total_no_response_trials > 0:
        rangenum = 3 - total_no_response_trials
    else:
        rangenum = 3 
    #trial 1
    num = cleanedList_trials_systole_ns[0] #assigns first value (trial number) to num
    systole_image2_noshock_count.append(cleanedList_trials_systole_ns.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    systole_image2_noshock_rt.append(cleanedList_rt_systole_ns[num_for_rt])
    for x in range(rangenum):
        num = cleanedList_trials_systole_ns[sum(systole_image2_noshock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(systole_image2_noshock_count)) #need index to be total count of trials so far
        systole_image2_noshock_count.append(cleanedList_trials_systole_ns.count(num))
        systole_image2_noshock_rt.append(cleanedList_rt_systole_ns[num_for_rt])
    #Varaibles to save
    al_mean_num_responses_systole_csminus = [Average(systole_image2_noshock_count)]
    al_mean_rt_systole_csminus = [Average(systole_image2_noshock_rt)]
    al_total_response_trials_systole_csminus= [16 - total_no_response_trials] 
    al_total_no_response_trials_systole_csminus = [total_no_response_trials]

    #Diastole image 2 no shock
    list_of_trial_numbers = []
    trial_numbers_diastole_no_shock = df['Diastole_Image2_NOshock_trial_num'].tolist() #creates list
    cleanedList_trials_diastole_ns = [x for x in trial_numbers_diastole_no_shock if str(x) != 'nan'] #removes nan values
    rt_diastole_no_shock = df['AL_RT_diastole_image2_NOshock_trial'].tolist()
    cleanedList_rt_diastole_ns = [x for x in rt_diastole_no_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_ns) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_diastole_ns[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_diastole_ns[x] != cleanedList_trials_diastole_ns[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_ns) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_diastole_ns = [i for j, i in enumerate(cleanedList_rt_diastole_ns) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_diastole_ns[x] = 0 
    cleanedList_trials_diastole_ns = [value for value in cleanedList_trials_diastole_ns if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    diastole_image2_no_shock_count = []
    diastole_image2_no_shock_rt = []
    if total_no_response_trials > 0:
        rangenum = 3 - total_no_response_trials
    else:
        rangenum = 3
    #trial 1
    num = cleanedList_trials_diastole_ns[0] #assigns first value (trial number) to num
    diastole_image2_no_shock_count.append(cleanedList_trials_diastole_ns.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    diastole_image2_no_shock_rt.append(cleanedList_rt_diastole_ns[num_for_rt])
    for x in range(rangenum):
        num = cleanedList_trials_diastole_ns[sum(diastole_image2_no_shock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(diastole_image2_no_shock_count)) #need index to be total count of trials so far
        diastole_image2_no_shock_count.append(cleanedList_trials_diastole_ns.count(num))
        diastole_image2_no_shock_rt.append(cleanedList_rt_diastole_ns[num_for_rt])
    #Varaibles to save
    al_mean_num_responses_diastole_csminus = [Average(diastole_image2_no_shock_count)]
    al_mean_rt_disatole_csminus = [Average(diastole_image2_no_shock_rt)]
    al_total_response_trials_diastole_csminus = [16 - total_no_response_trials]
    al_total_no_response_trials_diastole_csminus = [total_no_response_trials]

    ####TEST####
    df1 = pd.read_csv("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}/{}_test_phase.csv".format(ID,ID))
    
    #Image rating extractions and variables to save
    #Image 1
    t_mean_image1_rating = [df1['Image_1_rating'].mean(skipna = True)]
    t_image1_rating_RT = [df1['Image_1_rating_reactiontime'].mean(skipna = True)]
    #Image2
    t_mean_image2_rating = [df['Image_2_rating'].mean(skipna = True)]
    t_image2_rating_RT = [df['Image_2_rating_reactiontime'].mean(skipna = True)]

    #calculate average time interval between avoidance response and noise play for this participant Test phase
    trials_with_noise_play = df1['Noise_played_trial_number'].tolist() #creates list
    cleanedList_trials = [x for x in trials_with_noise_play if str(x) != 'nan'] #removes nan values
    delay_with_noise_play = df1['Noise_played_after_stim_duration'].tolist()
    cleanedList_noise = [x for x in delay_with_noise_play if str(x) != 'nan']
    trialnum_list1 = df1['Systole_image1_shock_trialnum'].tolist()#converts column to list
    trialnum_list2 = df1['Diastole_image1_shock_trialnum'].tolist()#converts column to list
    delays_systole_image1_shock = []
    delays_diastole_image1_shock = []
    for a in cleanedList_trials: #Checks for occurance of trial number in trial list, if yes, appends the delay 
        if a in trialnum_list1:
            a_index = trials_with_noise_play.index(a)
            delays_systole_image1_shock.append(cleanedList_noise[a_index])
        elif a in trialnum_list2:
            a_index = trials_with_noise_play.index(a)
            delays_diastole_image1_shock.append(cleanedList_noise[a_index])
    #saving variables
    mean_delay_systole_shock = Average(delays_systole_image1_shock)
    mean_delay_diastole_shock = Average(delays_diastole_image1_shock)
    #Calculate amount of times avoidance key pressed but noise still played (should be roughly 50%)
    avoidance_pressed_right_and_still_startle = df1['Trial_number_startle_played(despite_avoidance_key_pressed)'].tolist()
    cleaned_aprass = [x for x in avoidance_pressed_right_and_still_startle if str(x) != 'nan']
    count_systole_still_shock_despite_avoidance = 0
    count_diastole_still_shock_despite_avoidance = 0
    for a in cleaned_aprass:
        if a in trialnum_list1:
            count_systole_still_shock_despite_avoidance += 1
        elif a in trialnum_list2:
            count_diastole_still_shock_despite_avoidance += 1
    #variables to save
    t_mean_delay_systole_shock = [mean_delay_systole_shock]
    t_mean_delay_diastole_shock = [mean_delay_diastole_shock]
    t_count_systole_still_shock_despite_avoidance = [count_systole_still_shock_despite_avoidance]
    t_count_diastole_still_shock_despite_avoidance = [count_diastole_still_shock_despite_avoidance]

    #Systole image 1 shock
    list_of_trial_numbers = []
    trial_numbers_systole_shock = df1['Systole_image1_shock_trialnum'].tolist() #creates list
    cleanedList_trials_systole_s = [x for x in trial_numbers_systole_shock if str(x) != 'nan'] #removes nan values
    rt_systole_shock = df1['t_RT_systole_image1_shock_trial'].tolist()
    cleanedList_rt_systole_s = [x for x in rt_systole_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_s) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_systole_s[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_systole_s[x] != cleanedList_trials_systole_s[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_s) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_systole_s = [i for j, i in enumerate(cleanedList_rt_systole_s) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_systole_s[x] = 0  
    cleanedList_trials_systole_s = [value for value in cleanedList_trials_systole_s if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    systole_image1_shock_count = []
    systole_image1_shock_rt = []
    if total_no_response_trials > 0:
        rangenum = 15 - total_no_response_trials
    else:
        rangenum = 15
    #trial 1
    num = cleanedList_trials_systole_s[0] #assigns first value (trial number) to num
    systole_image1_shock_count.append(cleanedList_trials_systole_s.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    systole_image1_shock_rt.append(cleanedList_rt_systole_s[num_for_rt])
    for x in range(rangenum):
        num = cleanedList_trials_systole_s[sum(systole_image1_shock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(systole_image1_shock_count)) #need index to be total count of trials so far
        systole_image1_shock_count.append(cleanedList_trials_systole_s.count(num))
        systole_image1_shock_rt.append(cleanedList_rt_systole_s[num_for_rt])
    #Varaibles to save
    t_mean_num_responses_systole_csplus = [Average(systole_image1_shock_count)]
    t_mean_rt_systole_s_csplus = [Average(systole_image1_shock_rt)]
    t_total_response_trials_systole_csplus = [16 - total_no_response_trials] 
    t_total_no_response_trials_systole_csplus = [total_no_response_trials]

    #Diastole image 1 shock
    list_of_trial_numbers = []
    trial_numbers_diastole_shock = df1['Diastole_image1_shock_trialnum'].tolist() #creates list
    cleanedList_trials_diastole_s = [x for x in trial_numbers_diastole_shock if str(x) != 'nan'] #removes nan values
    rt_diastole_shock = df1['t_RT_Diastole_image1_shock_trial'].tolist()
    cleanedList_rt_diastole_s = [x for x in rt_diastole_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_s) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_diastole_s[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_diastole_s[x] != cleanedList_trials_diastole_s[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_s) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_diastole_s = [i for j, i in enumerate(cleanedList_rt_diastole_s) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_diastole_s[x] = 0  
    cleanedList_trials_diastole_s = [value for value in cleanedList_trials_diastole_s if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    diastole_image1_shock_count = []
    diastole_image1_shock_rt = []
    #testing
    if total_no_response_trials > 0:
        rangenum = 15 - total_no_response_trials
    else:
        rangenum = 15  
    #trial 1
    num = cleanedList_trials_diastole_s[0] #assigns first value (trial number) to num
    diastole_image1_shock_count.append(cleanedList_trials_diastole_s.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    diastole_image1_shock_rt.append(cleanedList_rt_diastole_s[num_for_rt])   
    for x in range(rangenum):
        num = cleanedList_trials_diastole_s[sum(diastole_image1_shock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(diastole_image1_shock_count)) #need index to be total count of trials so far
        diastole_image1_shock_count.append(cleanedList_trials_diastole_s.count(num))
        diastole_image1_shock_rt.append(cleanedList_rt_diastole_s[num_for_rt])
    #Varaibles to save
    t_mean_num_responses_diastole_csplus = [Average(diastole_image1_shock_count)]
    t_mean_rt_diastole_csplus = [Average(diastole_image1_shock_rt)]
    t_total_response_trials_diastole_csplus = [16 - total_no_response_trials] 
    t_total_no_response_trials_diastole_csplus = [total_no_response_trials]

    # Systole image 2 no shock
    list_of_trial_numbers = []
    trial_numbers_systole_no_shock = df1['Systole_image2_NOshock_trialnum'].tolist() #creates list
    cleanedList_trials_systole_ns = [x for x in trial_numbers_systole_no_shock if str(x) != 'nan'] #removes nan values
    rt_systole_no_shock = df1['t_RT_systole_image2_NOshock_trial'].tolist()
    cleanedList_rt_systole_ns = [x for x in rt_systole_no_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_ns) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_systole_ns[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_systole_ns[x] != cleanedList_trials_systole_ns[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_systole_ns) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_systole_ns = [i for j, i in enumerate(cleanedList_rt_systole_ns) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_systole_ns[x] = 0 
    cleanedList_trials_systole_ns = [value for value in cleanedList_trials_systole_ns if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    systole_image2_noshock_count = []
    systole_image2_noshock_rt = []
    if total_no_response_trials > 0:
        rangenum = 15 - total_no_response_trials
    else:
        rangenum = 15
    #trial 1
    num = cleanedList_trials_systole_ns[0] #assigns first value (trial number) to num
    systole_image2_noshock_count.append(cleanedList_trials_systole_ns.count(num))#counts occurances of num and appends to empty list (-1 because of 0 trials)
    num_for_rt = 0 #needs to be int
    systole_image2_noshock_rt.append(cleanedList_rt_systole_ns[num_for_rt])
    for x in range(rangenum):
        num = cleanedList_trials_systole_ns[sum(systole_image2_noshock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(systole_image2_noshock_count)) #need index to be total count of trials so far
        systole_image2_noshock_count.append(cleanedList_trials_systole_ns.count(num))
        systole_image2_noshock_rt.append(cleanedList_rt_systole_ns[num_for_rt])
    #Varaibles to save
    t_mean_num_responses_systole_csminus = [Average(systole_image2_noshock_count)]
    t_mean_rt_systole_csminus = [Average(systole_image2_noshock_rt)]
    t_total_response_trials_systole_csminus = [16 - total_no_response_trials] 
    t_total_no_response_trials_systole_csminus = [total_no_response_trials]

    #Diastole image 2 no shock
    list_of_trial_numbers = []
    trial_numbers_diastole_no_shock = df1['Diastole_Image2_NOshock_trial_num'].tolist() #creates list
    cleanedList_trials_diastole_ns = [x for x in trial_numbers_diastole_no_shock if str(x) != 'nan'] #removes nan values
    rt_diastole_no_shock = df1['t_RT_diastole_image2_NOshock_trial'].tolist()
    cleanedList_rt_diastole_ns = [x for x in rt_diastole_no_shock if str(x) != 'nan']
    #works out if non-response or just first 0 recording (has to happen before 0s removed from list)
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_ns) if x == 0] #finds all 0 values
    total_no_response_trials = 0
    if cleanedList_rt_diastole_ns[-1] == 0: #removes last item of 0 index if its a 0 (and adds 1 to no response trial) so the next statement is in range
        total_no_response_trials += 1
        del(index_of_0[-1])
    for x in index_of_0: #calculates other occurances of one 0
        if cleanedList_trials_diastole_ns[x] != cleanedList_trials_diastole_ns[x+1]:
            total_no_response_trials += 1 #total number of trials with no response
    index_of_0 = [i for i, x in enumerate(cleanedList_rt_diastole_ns) if x == 0] #resets the list incase last value deleted above
    #caluclating RT and number of spacebar presses
    cleanedList_rt_diastole_ns = [i for j, i in enumerate(cleanedList_rt_diastole_ns) if j not in index_of_0] #creates new list with 0 values removed
    for x in index_of_0: #messy hack, turns indexs of 0's (on the trial number side to 0) so all 0's can be removed from list
        cleanedList_trials_diastole_ns[x] = 0
    cleanedList_trials_diastole_ns = [value for value in cleanedList_trials_diastole_ns if value != 0] #removes all 0s i.e. the trials wit no response/first recording
    diastole_image2_no_shock_count = []
    diastole_image2_no_shock_rt = []
    if total_no_response_trials > 0:
        rangenum = 15 - total_no_response_trials
    else:
        rangenum = 15
    #trial 1
    num = cleanedList_trials_diastole_ns[0] #assigns first value (trial number) to num
    diastole_image2_no_shock_count.append(cleanedList_trials_diastole_ns.count(num))#counts occurances of num and appends to empty list 
    num_for_rt = 0 #needs to be int
    diastole_image2_no_shock_rt.append(cleanedList_rt_diastole_ns[num_for_rt])
    for x in range(rangenum):
        num = cleanedList_trials_diastole_ns[sum(diastole_image2_no_shock_count)] #sum list (for index as this is reccursive), adds 2 becasue of previous subtraction and to get to the next trial number
        num_for_rt = int(sum(diastole_image2_no_shock_count)) #need index to be total count of trials so far
        diastole_image2_no_shock_count.append(cleanedList_trials_diastole_ns.count(num))
        diastole_image2_no_shock_rt.append(cleanedList_rt_diastole_ns[num_for_rt])
    #Varaibles to save
    t_mean_num_responses_diastole_csminus = [Average(diastole_image2_no_shock_count)]
    t_mean_rt_disatole_csminus = [Average(diastole_image2_no_shock_rt)]
    t_total_response_trials_diastole_csminus = [16 - total_no_response_trials]
    t_total_no_response_trials_diastole_csminus = [total_no_response_trials]

    ####POST_EXPERIMENT_RATINGS####
    pt = pd.read_csv("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}/{}_stimuli_evaluation.csv".format(ID,ID))
    #Variables to save
    #Image 1
    ns_image1_pleasantness = [pt.iloc[0]['Image1_pleasantness']]
    ns_image1_pleasantness_rt = [pt.iloc[0]['Image1_pleasantness_RT']]
    ns_image1_anxiety = [pt.iloc[0]['Image1_anxiety']]
    ns_image1_anxiety_rt = [pt.iloc[0]['Image1_anxiety_RT']]
    #Image 2
    ns_image2_pleasantness = [pt.iloc[0]['Image2_plesantness']]
    ns_image2_pleasantness_rt = [pt.iloc[0]['Image2_plesantness_RT']]
    ns_image2_anxiety = [pt.iloc[0]['Image2_anxiety']]
    ns_image2_anxiety_rt = [pt.iloc[0]['Image2_anxiety_RT']]
    
      ####FINAL_OUTPUT####
      
    os.chdir("/Users/JamesMulcahy/Desktop/PhD_Year_2/Avoidance_project/pilot_data/{}".format(ID)) #Directory of where data saved
    
    output = {'Group':group,'NS_image1_rating': ns_image1_rating, 'NS_image1_rt':ns_image1_rt, 'NS_image2_rating':ns_image2_rating,
            'NS_image2_rt':ns_image2_rt,'FC_number_of_ratings':number_of_ratings_per_stim, 'FC_mean_image1_rating':fc_mean_image1_rating,
            'FC_mean_image1_rt':fc_mean_image1_rating_RT, 'FC_mean_image2_rating':fc_mean_image2_rating,
            'FC_mean_image2_rt':fc_mean_image2_rating_RT, 'AL_mean_image1_rating': al_mean_image1_rating,
            'AL_mean_image1_rt':al_mean_image1_rating_RT, 'AL_mean_image2_rating':al_mean_image2_rating,
            'AL_mean_image2_rt':al_mean_image2_rating_RT, 'AL_mean_delay_systole_shock':al_mean_delay_systole_shock,
            'AL_mean_delay_diastole_shock':al_mean_delay_diastole_shock, 'AL_systole_still_shock_with_avoidance_count':al_count_systole_still_shock_despite_avoidance,
            'AL_diastole_still_shock_with_avoidance_count':al_count_diastole_still_shock_despite_avoidance,
            'AL_systole_csplus_mean_num_responses':al_mean_num_responses_systole_csplus, 'AL_systole_csplus_mean_rt':al_mean_rt_systole_csplus,
            'AL_systole_csplus_total_num_responses':al_total_response_trials_systoloe_csplus, 'AL_systole_csplus_total_no_responses':al_total_no_response_trials_systole_csplus,
            'AL_diastole_csplus_mean_num_responses':al_mean_num_responses_diastole_csplus, 'AL_diastole_csplus_mean_rt':al_mean_rt_diastole_csplus,
            'AL_diastole_csplus_total_num_responses':al_total_response_trials_diastole_csplus,'AL_diastole_csplus_total_no_responses':al_total_no_response_trials_diastole_csplus,
            'AL_systole_csminus_mean_num_responses':al_mean_num_responses_systole_csminus, 'AL_systole_csminus_mean_rt':al_mean_rt_systole_csminus,
            'AL_systole_csminus_total_num_responses':al_total_response_trials_systole_csminus, 'AL_systole_csminus_total_no_responses':al_total_no_response_trials_systole_csminus,
            'AL_diastole_csminus_mean_num_responses':al_mean_num_responses_diastole_csminus,'AL_diastole_csminus_mean_rt':al_mean_rt_disatole_csminus,
            'AL_diastole_csminus_total_num_responses':al_total_response_trials_diastole_csminus, 'AL_diastole_csminus_total_no_responses':al_total_no_response_trials_diastole_csminus,
            'T_mean_image1_rating':t_mean_image1_rating, 'T_mean_image1_rt':t_image1_rating_RT, 'T_mean_image2_rating':t_mean_image2_rating,
            'T_mean_image2_rt':t_image2_rating_RT, 'T_mean_delay_systole_shock':t_mean_delay_systole_shock, 'T_mean_delay_diastole_shock':t_mean_delay_diastole_shock,
            'T_systole_still_shock_with_avoidance_count':t_count_systole_still_shock_despite_avoidance, 'T_diastole_still_shock_with_avoidance_count':t_count_diastole_still_shock_despite_avoidance,
            'T_systole_csplus_mean_num_responses':t_mean_num_responses_systole_csplus,'T_systole_csplus_mean_rt':t_mean_rt_systole_s_csplus,
            'T_systole_csplus_total_num_responses':t_total_response_trials_systole_csplus, 'T_systole_csplus_total_no_responses':t_total_no_response_trials_systole_csplus,
            'T_diastole_csplus_mean_num_responses':t_mean_num_responses_diastole_csplus,'T_diastole_csplus_mean_rt':t_mean_rt_diastole_csplus,
            'T_diastole_csplus_total_num_responses':t_total_response_trials_diastole_csplus,'T_diastole_csplus_total_no_responses':t_total_no_response_trials_diastole_csplus,
            'T_systole_csminus_mean_num_responses':t_mean_num_responses_systole_csminus, 'T_systole_csminus_mean_rt':t_mean_rt_systole_csminus,
            'T_systole_csminus_total_num_responses':t_total_response_trials_systole_csminus, 'T_systole_csminus_total_no_responses': t_total_no_response_trials_systole_csminus,
            'T_diastole_csminus_mean_num_responses':t_mean_num_responses_diastole_csminus, 'T_diastole_csminus_mean_rt':t_mean_rt_disatole_csminus,
            'T_diastole_csminus_total_num_responses':t_total_response_trials_diastole_csminus, 'T_diastole_csminus_total_no_responses':t_total_no_response_trials_diastole_csminus,
            'F_image1_pleasantness':ns_image1_pleasantness, 'F_image1_pleasantness_rt':ns_image1_pleasantness_rt,
            'F_image1_anxiety':ns_image1_anxiety, 'F_image1_anxiety_rt':ns_image1_anxiety_rt,
            'F_image2_pleasantness':ns_image2_pleasantness, 'F_image2_pleasantness_rt':ns_image2_pleasantness_rt,
            'F_image2_anxiety':ns_image2_anxiety, 'F_image2_anxiety_rt':ns_image2_anxiety_rt}
    df = pd.DataFrame.from_dict(output, orient='index')
    df.transpose().to_csv('{}_sorted_results.csv'.format(ID))