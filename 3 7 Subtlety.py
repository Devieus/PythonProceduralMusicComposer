'''
* * *
Sheet music generator using ABC notation
* * *
'''

# The bread and butter of proc-gen
import random as r
from math import ceil
# Some basic values related to ABC:
# Song number
X='1' # First song, increase this to make an opus
# Title
T="Subtlety" # Song title
# Tempo
Q=r.randint(90,240) # Choose a tempo between 1.5b/s and 4b/s.
# Key
keys=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
K=keys[Q%12] # Based on tempo, they're all the same mostly, though this will favor the upper half very slightly.
# and will only be used at the end for transposition.

# Default scale is blank, but make sure there're two whole notes in there.
# The reason for this is because it favors a heptatonic scale, favoring hexatonic and octatonic scale second.
scale=[0,0,0,2,0,0,0,0,2,0,0,0]
# Add one to a random step in the scale eight times to make it 12 steps, or a whole octave.
for x in range(8):
    # Select a random index of the scale and add 1 to it.
    scale[r.randint(0,len(scale)-1)]+=1
# Prune all the zeroes from the scale
while scale.count(0)>0:
    scale.remove(0)
# For administrative purposes, store the scale in a different variable.
oldScale=[]
# Somehow oldScale=scale makes a soft copy.
for x in scale:
    # That's not administratively responsible.
    oldScale.append(x)
# Append the scale to itself so all chords can be played.
for x in range(len(scale)):
    scale.append(scale[x])
# A delta scale indicating the sum of all previous steps, so they correspond to the notes 1:1.
deltaScale=[0]
# deltaScale's next value is its previous value plus scale's previous value
for x in range(len(oldScale)):
    # Store the value in another variable.
    deltaScale.append(deltaScale[x]+oldScale[x])

# Meter, x/4 for now
M=int(r.gauss(mu=4,sigma=1)) # Beats per bar, might change since bar and arps will fit anyway.
M2=4 # note that is said beat (inverted), will stay 4 for a while

# Choose a song length between 3 and 5 progression cycles, taking tempo into account.
songLength=int(r.randint(3,5)*Q/180+0.5)

# Default note length
L=1 # eighths
L2=8
# Voice
V=4 # Number of voices, the main, the second main, the base, and the drum
# These are important in some way. The variables are what makes ABC
sequence=1 # track 1
# Make the basic output
output='X:'+X+'\nT:'+T+'\nK:'+K+'\nM:'+str(M)+'/'+str(M2)+'\nQ:'+str(Q)+'\nL:'+str(L)+'/'+str(L2)+'\n'
# All these variables are set differently in the ABC, but that'll sort itself out.
 
# The concept here is to randomly generate a sequence of
#  - Notes, represented by a-g,A-G
#  - Note lengths, represented by numbers after the note
#  - Chords in the second track
# Then end it all with the end token, which looks like |]
# 
# All the valid notes in a neat 5x5 grid
notes=['C','_D','D','_E','E',
       'F','_G','G','_A','A',
       '_B','B' ,'c','_d','d',
       '_e','e' ,'f','_g','g',
       '_a','a','_b','b','c\''
       ,'z']

# Let's hit some things.
drum=['hatclose','clave']
drumDic={'hatopen':'_B,,','hatclose':'_G,,','base1':'_C,,','base2':'=C,,',
        'snare1':'=D,,','snare2':'=E,,','clave':'_e'}
# First choose which snare drum and base drum to use, since there's two of each.
snare=r.choice(['snare1','snare2'])
# No use in using both just yet, the difference is too minimal.
bassdrum=r.choice(['base1','base2'])
options=['z2',drumDic[snare]+'2',drumDic[bassdrum]+'2','['+drumDic[snare]+'2'+drumDic[bassdrum]+'2'+']']

# One possible way to start the music is by having the bass do chord progressions.
# It's a simple set of progressions for now.
# Though it looks pretty complex and there's some redundant names, they're all different states.
# Any new progression can enhance existing states, which would increase variety without increasing complexity.
# Make a finite state machine.
state='0'
# A list of all states, 9 for now.
states=['0','1','2','3','4','5','6','7','8']
# A dictionary of all the states.
statesDic={'0':{'name':'M','notes':[0,0,0],'next':['1']}, # State 1 will always be the tonic.
           '1':{'name':'M','notes':[0,0,0],'next':['2','3']}, # State 2 will only have majors.
           '2':{'name':'M','notes':[0,0,0],'next':['4','5','6','7','8']}, # State 3 will feature majors,
           '3':{'name':'m','notes':[0,-1,0],'next':['4','5','6','7','8']},# as well as minors and can jump out.
           '4':{'name':'M','notes':[0,0,0],'next':['4','5','6','7','8']}, # State 4 will feature majors chords.
           '5':{'name':'m','notes':[0,-1,0],'next':['4','5','6','7','8']},# Minors chords.
           '6':{'name':'Aug','notes':[0,1,1],'next':['4','5','6','7','8']}, # Augmented chords.
           '7':{'name':'Dim','notes':[0,-1,-1],'next':['4','5','6','7','8']},# And diminished chords, and can jump out if it has to.
           '8':{'name':'M','notes':[0,0,0],'next':['0']}} # State 5 will bring it back to the tonic and will resolve the cadence.
# A basic chord
basic=[0,3,5]
# A place for all the songs.
songDic={
    "lead":[], # The other lead.
    "lead2":[], # The bass lead.
    "lead3":[], # More variety is better.
    "bass":[],
    "arp":[], # Steady reimplmentation.
    "drum1":[], # Basic drums.
    "drum2":[], # Extra drums.
    "drum3":[], # Not used.
    "voiceCount":[], # Syllables per bar.
    "voice":[], # Words
    "bars":[], # Bar numbers.
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "fail":[], # A list of chaos induced failures.
    "chordNotes":[] # A list of chord notes represented as notes from the notes list.
}
# The chorus part of the song, which will be appended into the songDic.
chorusDic={
    "lead":[],
    "bass":[],
    "arp":[], # Steady reimplmentation.
    "drum1":[], # Basic drums.
    "drum2":[], # Extra drums.
    "drum3":[], # Not used.
    "voiceCount":[], # Syllables per bar.
    "voice":[], # Words
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "chordNotes":[] # A list of chord notes represented as notes from the notes list.
}
# The other dictionary, which is the intros, refrains and outros.
otherDic={
    "lead":[],
    "bass":[],
    "arp":[], # Steady reimplmentation.
    "drum1":[], # Basic drums.
    "drum2":[], # Extra drums.
    "drum3":[], # Not used.
    "voiceCount":[], # Syllables per bar.
    "voice":[], # Words
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "chordNotes":[] # A list of chord notes represented as notes from the notes list.
}


"""
Bass
"""
# Make a bass bar based on the progressions.
def bassBar(chord):
    # The result list where everything is added to.
    result=[]
    # A counter that counts the notes in a bar.
    x=(M/M2)/(L/L2)
    while x>0:
        # Pick a random note from the available selection, or a rest with probablity equal to the signature.
        note=notes[r.choice(chord)] if r.randint(1,10)>M else 'z'
        # Pick a length for the note.
        fitting=False
        # It has to fit.
        while not fitting:
            # A random note length that favors eighths.
            noteLength=int(abs(r.gauss(0,M*2))+1)
            # Check if the note fits.
            if noteLength<=x:
                fitting=True
                # Subtract the note from x for future length checks.
                x-=noteLength
        # If the note is longer than an eigth, add the number to the note.
        result.append(note+str(noteLength)) if noteLength>1 else result.append(note)
    # At the end of the bar, the state has to change;
    # this can be done anywhere, so it won't be done here.
    return result

# Make the whole bass.
def bassify(state):
    # The result dictionary.
    result={"state":[],"chord":[],"bass":[],"chordNotes":[]}
    # Build bars for the duration of a progression.
    # Add the current state,
    result["state"].append(state)
    # The chord name,
    result["chord"].append(str(notes[statesDic[state]['notes'][0]]))
    # And the bass bar.
    result["bass"].append(bassBar(statesDic[state]['notes']))
    # Add the chord notes for future use.
    result["chordNotes"].append(statesDic[state]['notes'])
    # Elevate the state to the next one
    state=r.choice(statesDic[state]['next'])
    # Do that again until the state is back to the first.
    while state!="0" and state!="8":
        # Make sure the increment is between 1 and whatever's in the scale (except the last which would be I one octave higher and the first which is I).
        incrementalValue=deltaScale[r.randint(1,len(deltaScale)-2)]
        # Grab the notes belonging to that state.
        bassChord=[]
        for x in statesDic[state]['notes']:
            bassChord.append(x)
        for x in range(len(bassChord)):
            # Elevate all notes of the chord to match with the notes.
            bassChord[x]+=incrementalValue
        # Add this new list to the track.
        result["chordNotes"].append(bassChord)
        # Make the bass bar and add it to the bass track.
        result["bass"].append(bassBar(bassChord))
        # Add the state to the state track.
        result["state"].append(state)
        # Add the name of the chord played to the right track.
        if statesDic[state]['name']=='m':
            # This is, what passes for, a minor chord.
            result["chord"].append(str(notes[bassChord[0]])+'m')
        elif statesDic[state]['name']=='Dim':
            # This is, what passes for, a dim chord.
            result["chord"].append(str(notes[bassChord[0]])+'o')
        elif statesDic[state]['name']=='Aug':
            # This is, what passes for, an aug chord.
            result["chord"].append(str(notes[bassChord[0]])+'+')
        else:
            # This is, what passes for, a regular chord.
            result["chord"].append(notes[bassChord[0]])
        # Change the state.
        state=r.choice(statesDic[state]['next'])
        # Add the current state,
    # Right now, state=8, so do the same thing as before.
    result["state"].append(state)
    # The chord name,
    result["chord"].append(str(notes[statesDic[state]['notes'][0]]))
    # And the bass bar.
    result["bass"].append(bassBar(statesDic[state]['notes']))
    # Add the chord notes for future use.
    result["chordNotes"].append(statesDic[state]['notes'])
    # Reset the state to 0
    state="0"
    return result

"""
Lead
"""

# Make a lead bar, the first note is based on the bass.
def leadBar(state,bassBar):
    # The result list.
    result=[]
    # The note counter.
    x=(M/M2)/(L/L2)
    # Find a note that exists.
    y=0
    while True:
        # Check to see if the first note has an accidental.
        note=bassBar[y][0]+bassBar[y][1] if bassBar[y][0]=='_' else bassBar[y][0]
        # If it exists, break out.
        if deltaScale.count(notes.index(note))>0:
            break
        # Otherwise, search the next note.
        else:
            y+=1
        # If no note could be found, e.g. in a minor bar and only non-existing notes are written,
        if y==len(bassBar):
            # Make the note C,
            note='C'
            # and break out.
            break
    # Resolve cadence is the progression has ended.
    if state=='8':
        return note+str(x)
    # Store the note in a backup, that way if a rest is implemented, the note isn't lost.
    backupNote=note
    while x>0:
        fitting=False
        while not fitting:
            noteLength=int(abs(r.gauss(0,1.5))+1)
            if noteLength<=x:
                fitting=True
                x-=noteLength
        # If the note is longer than L's default value, add the number
        result.append(note+str(noteLength)) if noteLength>1 else result.append(note)
        # Retrieve the backup to calculate the next note.
        note=backupNote
        # Check to see if the next note should be a rest.
        if r.randint(1,10)<4:
            note='z'
        else:
            # Choose a random note from the scale to be the next note up to 5 notes away with some variance.
            y=abs(deltaScale.index(notes.index(note))+int(r.gauss(0,2.5))) # abs() bounces negatives up.
            # It has to still be on the scale list.
            if y>len(deltaScale)-1:
                # Bounce down the excess
                y=y-(y-len(deltaScale))-1
            note=notes[deltaScale[y]]
            backupNote=note
    return result

# Make the whole lead.
def leadify(state,bassNotes):
    # The result list.
    result=[]
    # A bar has to be made for every bass bar
    for i in range(len(bassNotes)):
        # This then gets added.
        result.append(leadBar(state[i],bassNotes[i]))
    return result


"""
Drums
"""

# Create a drum bar.
def drumroll():
    # Result string
    result=''
    # There's 8 hits in a 4/4 bar.
    x=(M/M2)/(L/L2)
    # There's 1 chance in 4 there's a rest.
    while x>0:
        # Either add a rest or a note, both'll be one eighth in length.
        result+='z' if r.randint(1,10)<4 else drumDic[r.choice(drum)]
        x-=1
    return result

# This makes the basic drum track with snare and bass drums.
def drumBase():
    # Result string:
    result=''
    # 4 hits in a 4/4 bar.
    x=((M/M2)/(L/L2))/2
    # A beat is either a rest, a base drum, a snare drum, or both.
    while x>0:
        result+=options[r.randint(0,3)]
        x-=1
    return result

"""
Arps
"""

# Every bar has a chord of 3 notes in length, which will be used for the arp. These chords are major, minor, aug and dim.
def arpeggio(chord,method,reps):
    # The result string.
    result=''
    # One edge case.
    if M==2 and reps==2:
        result+=notes[chord[0]+basic[0]]+"["+notes[chord[1]+basic[1]]+notes[chord[2]+basic[2]]+"]"
        result+=notes[chord[0]+basic[0]]+"["+notes[chord[1]+basic[1]]+notes[chord[2]+basic[2]]+"]"
        return result
    # Asign a length that the notes will be getting depending on the number of reps.
    length="2" if reps==1 else ""
    for x in range(reps):
        # Separate activity basicd on the method.
        if method==0:
            # Go up, then down.
            for x in range(M):
                # When the last note is reached, go back down by negating x and level it.
                result+=notes[chord[x]+basic[x]]+length if x<3 else notes[chord[M-(x+M%4)]+basic[M-(x+M%4)]]+length
        if method==1:
            # Go down, then up.
            for x in range(M):
                # This method is much the same, but in reverse order.
                result+=notes[chord[M-(x+M-2)]+basic[M-(x+M-2)]]+length if x<3 else notes[chord[x-2]+basic[x-2]]+length
        if method==2:
            # Go up, stay up. This one places the first few notes, then lets the last linger.
            result+=notes[chord[0]+basic[0]]+length+notes[chord[1]+basic[1]]+length+notes[chord[2]+basic[2]]+str((len(length)+1)*(M-2)) if M>2 else notes[chord[0]+basic[0]]+length+notes[chord[1]+basic[1]]+length
        if method==3:
            # Go down, stay down.
            # This method is much the same as the second, but staying up.
            # result+=notes[chord[M-(x+M-2)]]+length if x<3 else notes[chord[2]]+length
            # This method is much the same as the previous.
            result+=notes[chord[0]+basic[0]]+length+notes[chord[1]+basic[1]]+length+notes[chord[2]+basic[2]]+str((len(length)+1)*(M-2)) if M>2 else notes[chord[0]+basic[0]]+length+notes[chord[1]+basic[1]]+length
        if method==4:
            # Play the first note, then the other two; repeat.
            for x in range(M):
                # This is similar to the edge case.
                result+=notes[chord[0]+basic[0]]+length if x%2==1 else "["+notes[chord[1]+basic[1]]+length+notes[chord[2]+basic[2]]+length+"]"
        if method==5:
            # Play the first note, then the other two over and over.
            for x in range(M):
                result+=notes[chord[0]+basic[0]]+length if x==0 else "["+notes[chord[1]+basic[1]]+length+notes[chord[2]+basic[2]]+length+"]"
        if method==6:
            # Play the first note, then the other two, holding them.
            result+=notes[chord[0]+basic[0]]+length+"["+notes[chord[1]+basic[1]]+str((len(length)+1)*(M-1))+notes[chord[2]+basic[2]]+str((len(length)+1)*(M-1))+"]"
    return result

# The arp writing routine
def arpeggify(chords):
    # Choose the method.
    method=r.choice(range(8))
    # The result list.
    result=[]
    # Choose a length, which is actually going to be really small and should be constant
    reps=r.choice([1,2])
    # A bar has to be made for every bass bar
    for i in chords:
        # This then gets added.
        result.append(arpeggio(i,method,reps))
    return result

"""
Vocals
"""
# The voice track is for lyrics, these lyrics don't have to make sense, they're procedurally generated words.
# This makes a word of x syllables, x being the number of actual notes, i.e. not rests, in a bar.
# The list of consonants to be used at the beginning of a syllable.
cons=['b','c','d','f','g','h','j','k','l','m','n','p','qu','r','s','t','v','w','y','z','ch','sh','th']
# The list of consonants to be used at the end of a syllable.
cons2=['b','c','d','f','g','h','k','l','m','n','p','r','s','t','w','y','z','ch','sh','rk','th','ts','ng','nk']
# Every syllable has 1 vowel and is the definition of a syllable in a basic sense.
vow=['a','e','i','o','u','oi','ea']
# Make a syllable.
def syl():
    # The result string.
    result=''
    #Does it start with a consonant?
    if r.choice([True,False]):
        result+=r.choice(cons)
    #Then add a vowel
    result+=r.choice(vow)
    #Does it end with a consonant?
    if r.choice([True,False]):
        result+=r.choice(cons)
    return result

# Make a word with x syllables.
def word(x):
    # The result string.
    result=''
    if x<=0:
        return result
    # Run syl() as many times as it's been given.
    for y in range(x):
        result+=syl()
    return result

def vocals(track):
    result=[]
    # Bar is exactly the same as the range of any songDic that's filled out. This just ensures it syncs right.
    for x in range(len(track)):
        # Start with a 0.
        result.append([0])
        # The voice is synced to the bar, but numbers are required, plus notes are combined.
        for y in track[x]:
            index=0
            # If the next note is an accidental.
            if y[0]=='_':
                index+=1
            # If it's a rest, subtract the length of it from the latest number.
            if y[0]=='z':
                # Check to see if the current number is 0 (because it's the first) or negative.
                if result[x][len(result[x])-1]>0:
                    # If it isn't, add a new number to work on.
                    result[x].append(0)
                # If y doesn't have a number, i.e. it's length 1,
                if len(y)==1:
                    # Subtract that 1 from the count.
                    result[x][len(result[x])-1]-=1
                else:
                    # Subtract the rest length from the number.
                    result[x][len(result[x])-1]-=int(y[1])
            # The next thing is a note.
            else:
                # Check to see if the current number is 0 (because it's the first) or positive or 4 syllables long.
                if result[x][len(result[x])-1]<0 or result[x][len(result[x])-1]>=4:
                    # If it isn't, add a new number to work on.
                    result[x].append(0)
                # If y doesn't have a number, i.e. it's length 1,
                if len(y)==1+index:
                    # Add that 1 from the count.
                    result[x][len(result[x])-1]+=1
                else:
                    # Add the note length from the number.
                    result[x][len(result[x])-1]+=int(y[-1])
    return result
                
def lyrics(otherLength,voiceCount):
    result=[]
    for x in range(otherLength):
        result.append([])
        for y in voiceCount[x]:
            result[x].append(word(y))
    return result
'''
Building the song
'''
# First make the chorus
# All the bass notes.
chorus=bassify(state)
chorusDic["bass"]=chorus["bass"]*2
chorusDic["state"]=chorus["state"]*2
chorusDic["chord"]=chorus["chord"]*2
chorusDic["chordNotes"]=chorus["chordNotes"]*2
# Make the whole lead section from the bass notes.
chorusDic["lead"]=leadify(chorusDic["state"],chorusDic["bass"])
chorusDic["drum1"]=drumroll()
chorusDic["drum2"]=drumBase()
chorusDic["arp"]=arpeggify(chorusDic["chordNotes"])
# The length of the chorus in bars.
chorusLength=len(chorusDic["bass"])
# The vocals.
chorusDic["voiceCount"]=vocals(r.choice([chorusDic["bass"],chorusDic["lead"]]))
for x in range(chorusLength):    
    for y in chorusDic['voiceCount'][x]:
        chorusDic['voice'].append(word(y))

# Do it again for the other.
other=bassify(state)
otherDic["bass"]=other["bass"]*2
otherDic["state"]=other["state"]*2
otherDic["chord"]=other["chord"]*2
otherDic["chordNotes"]=other["chordNotes"]*2
otherDic["lead"]=leadify(otherDic["state"],otherDic["bass"])
otherDic["drum1"]=drumroll()
otherDic["drum2"]=drumBase()
otherDic["arp"]=arpeggify(otherDic["chordNotes"])
# The length of the other in bars.
otherLength=len(otherDic["bass"])
# The vocals
otherDic["voiceCount"]=vocals(r.choice([otherDic["bass"],otherDic["lead"]]))
otherDic["voice"]=lyrics(otherLength,otherDic["voiceCount"])

'''
Making the song
'''
# Add the intro.
for x in range(otherLength):
# Fill in the songDic with the gathered information
    songDic["bass"].append(otherDic["bass"][x])
    # Starting with an intro of just the basic other tracks
    songDic["lead"].append(otherDic["lead"][x])
#    songDic["drum1"].append(otherDic["drum1"])
#    songDic["drum2"].append(otherDic["drum2"])
    songDic["drum1"].append("z"+str(int((M/M2)/(L/L2)))) if x<otherLength*2/3 else songDic["drum1"].append(otherDic["drum1"])
    songDic["drum2"].append("z"+str(int((M/M2)/(L/L2)))) if x<otherLength*2/3 else songDic["drum2"].append(otherDic["drum2"])
    songDic["state"].append(otherDic["state"][x])
    songDic["lead2"].append(["z"+str(int((M/M2)/(L/L2)))])
    songDic["chord"].append(otherDic["chord"][x])
    songDic["chordNotes"].append(otherDic["chordNotes"][x])
    songDic["arp"].append(["z"+str(int((M/M2)/(L/L2)))]) if x<otherLength/3 else songDic["arp"].append(otherDic["arp"][x])
    songDic["voiceCount"].append(otherDic["voiceCount"][x])
    songDic["voice"].append(otherDic["voice"][x])
# The total length of the song.
totalLength=otherLength
# The song length is measured in progression cycles.
for x in range(songLength):
    # A cycle the song consists of is the chorus followed by an other
    for y in range(chorusLength):
        songDic["bass"].append(chorusDic["bass"][y])
        songDic["lead2"].append(chorusDic["lead"][y])
        songDic["drum1"].append(chorusDic["drum1"])
        songDic["drum2"].append(chorusDic["drum2"])
        songDic["state"].append(chorusDic["state"][y])
        songDic["lead"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["chord"].append(chorusDic["chord"][y])
        songDic["chordNotes"].append(chorusDic["chordNotes"][y])
        songDic["arp"].append(chorusDic["arp"][y])
        songDic["voiceCount"].append(chorusDic["voiceCount"][y])
        songDic["voice"].append(chorusDic["voice"][y])
    totalLength+=chorusLength
    # It's possible at this point to regenerate the otherDic.
    # For instance, new lyrics.
    otherDic["voice"]=lyrics(otherLength,otherDic["voiceCount"])
    # And a new lead.
    otherDic["lead"]=leadify(otherDic["state"],otherDic["bass"])
    for y in range(otherLength):
        songDic["bass"].append(otherDic["bass"][y])
        songDic["lead"].append(otherDic["lead"][y])
        songDic["drum1"].append(otherDic["drum1"])
        songDic["drum2"].append(otherDic["drum2"])
        songDic["state"].append(otherDic["state"][y])
        songDic["lead2"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["chord"].append(otherDic["chord"][y]) 
        songDic["chordNotes"].append(otherDic["chordNotes"][y]) 
        songDic["arp"].append(otherDic["arp"][y]) if x%2==0 else songDic["arp"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["voiceCount"].append(otherDic["voiceCount"][y])
        songDic["voice"].append(otherDic["voice"][y])               
    totalLength+=otherLength
    
# Add the outro, starting with new lyrics.
otherDic["voice"]=lyrics(otherLength,otherDic["voiceCount"])
# Then do the same as the intro.
for x in range(otherLength):
# Fill in the songDic with the gathered information
    songDic["bass"].append(otherDic["bass"][x])
    # Starting with an intro of just the basic other tracks
    songDic["lead"].append(otherDic["lead"][x])
#    songDic["drum1"].append(otherDic["drum1"])
#    songDic["drum2"].append(otherDic["drum2"])
    songDic["drum1"].append("z"+str(int((M/M2)/(L/L2))))
    songDic["drum2"].append("z"+str(int((M/M2)/(L/L2))))
    songDic["state"].append(otherDic["state"][x])
    songDic["lead2"].append(["z"+str(int((M/M2)/(L/L2)))])
    songDic["chord"].append(otherDic["chord"][x])
    songDic["chordNotes"].append(otherDic["chordNotes"][x])
    # Don't always add the arp, for sanity's sake.
    songDic["arp"].append(otherDic["arp"][x])
    songDic["voiceCount"].append(otherDic["voiceCount"][x])
    songDic["voice"].append(otherDic["voice"][x])
totalLength+=otherLength

# Getting the bar numbers.
for x in range(totalLength):
    songDic["bars"].append(x)

"""
Writing down
"""
# First voice (lead)
output+='V:1\n'
# The full song should be in the songDic.
for i in songDic["bars"]:
    # Write down the bar.
    for j in songDic["lead"][i]:
            output+=j
    output+='|'
output+=']\n\n'

# Second voice, the chorus lead.
output+='V:2\n'
# The full song should be in the songDic.
for i in songDic["bars"]:
    # Write down the bar.
    for j in songDic["lead2"][i]:
            output+=j
    output+='|'
output+=']\n\n'

# Third voice, whatever.
output+='V:3\n'
# Make a fresh start.
songDic["lead3"]=leadify(songDic['state']*2,songDic["bass"])*2
for i in songDic["bars"]:
    # Write down the bar with 1/2 chance of success.
    if r.choice([True,False]):
        output+='z'+str(int((M/M2)/(L/L2)))
    else:
        for j in songDic["lead3"][i]:
            output+=j
    # Make a new lead 2 when the old one ran its course.
    if i%len(songDic["lead3"])==0:
        songDic["lead3"]=leadify(songDic['state']*2,songDic["bass"])*2
    output+='|'
output+=']\n\n'

# Fourth voice (bass).
output+='V:4\n'
# The protocol is much the same as the leads.
for i in songDic["bars"]:
    for j in songDic["bass"][i]:
        output+=j
    output+='|'
output+=']\n\n'

# Fifth voice (arp).
output+='V:5\n'
# The protocol is much the same as the leads.
for i in songDic["bars"]:
    for j in songDic["arp"][i]:
        output+=j
    output+='|'
output+=']\n\n'

# Third voice (drums).
output+='V:6\n'
for i in songDic['bars']:
    # Unlike the other tracks, the drums are stored in a list of strings, rather than a list of lists of strings.
    output+=songDic['drum1'][i]+'|'
# Closing statements
output+=']\n\n'

# Fourth voice, the basic drums.
output+='V:7\n'
# Go through the whole song.
for i in songDic['bars']:
    # Unlike the other tracks, the drums are stored in a list of strings, rather than a list of lists of strings.
    output+=songDic['drum2'][i]+'|'
# Closing statements
output+=']\n\n'

# Fifth voice, eventually the drums are just going to be deconstructed into their own tracks, but for now this adds accents where they're needed.
output+='V:8\n'
# This voice's only task is to put a crash (or an open hi-hat as analog) at the end of each progression cycle.
for i in songDic["bars"]:
    # It'll do this throughout the song, disregarding intros and outros.
    output+='z'+str(int((M/M2)/(L/L2))-1)+drumDic['hatopen']+'|' if songDic['state'][i]=='8' and i>1 else 'z'+str(int((M/M2)/(L/L2)))+'|'
output+=']\n\n'

# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.abc','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
output=str(songDic["voice"])
# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.txt','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
# Flush the output, free up space, plus the parser can't handle a string that long.
output=''
# Calculate the song length in minutes. The number of bars times the number of notes in a bar=number of beats, divided by tempo (or beats per minute).
t=(songDic['bars'][-1]*M)/Q
# Meta information
print(str(oldScale)+' in '+K+' at '+str(Q)+'BPM\nSong length is '+str(int(t))+':'+str(int(t%1*60)))
      #str(int(((songLength*songDic['bars'][-1]*M2)/(Q*60)%1+.01)*60)))

# Time to parse the ABC with
import music21 as mu
# package for further processing
song=mu.converter.parse(T+'.abc')
# one such process is transposing according to the key.
transpose={'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':-5,'G#':-4,'A':-3,'A#':-2,'B':-1}
# This is where the key is being actually used. First the first lead,
song.parts[0].transpose(transpose[K],True)
# Then the second lead,
song.parts[1].transpose(transpose[K],True)
# And finally the third lead.
song.parts[2].transpose(transpose[K],True)
# The bass goes down an octave as well, to make it a bass.
song.parts[3].transpose(transpose[K]-12,True)
# As does the arpeggio
song.parts[4].transpose(transpose[K]-12,True)
# Drums don't get transposed.
# Open the song in Musescore for final touches.
song.show()
# Now everything works.

##An alternate way of putting a shorthand if statement is
##note=[bassBar[0][0],bassBar[0][0]+bassBar[0][1]][bassBar[0][0]=='_']
##Which is witchcraft of lists by making a list of 2 elements,
##then choosing one with the knowledge boolean operators are either 0 or 1
##e.g. [0,1][True] will return 1, because True=1 and [0,1][1]=1
##
##Doing it the way it is now is more explicitly ternary and slightly more grammatically logical.
##Plus, operations such as append cannot be in lists.
"""
# A dictionary of all the states.
statesDic={'0':{'name':'M','notes':[0,4,7],'next':['1']}, # State 1 will always be the tonic.
           '1':{'name':'M','notes':[0,4,7],'next':['2','3']}, # State 2 will only have majors.
           '2':{'name':'M','notes':[0,4,7],'next':['4','5','6','7','8']}, # State 3 will feature majors,
           '3':{'name':'m','notes':[0,3,7],'next':['4','5','6','7','8']},# as well as minors and can jump out.
           '4':{'name':'M','notes':[0,4,7],'next':['4','5','6','7','8']}, # State 4 will feature majors chords.
           '5':{'name':'m','notes':[0,3,7],'next':['4','5','6','7','8']},# Minors chords.
           '6':{'name':'Aug','notes':[0,4,8],'next':['4','5','6','7','8']}, # Augmented chords.
           '7':{'name':'Dim','notes':[0,3,6],'next':['4','5','6','7','8']},# And diminished chords, and can jump out if it has to.
           '8':{'name':'M','notes':[0,4,7],'next':['0']}} # State 5 will bring it back to the tonic and will resolve the cadence.
           """
