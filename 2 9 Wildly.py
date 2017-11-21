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
T="Wildly" # Song title
# Key
keys=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
K=r.choice(keys) # Random key, they're all the same mostly
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
for x in range(len(scale)):
    # Store the value in another variable.
    deltaScale.append(deltaScale[x]+scale[x])

# Meter, 4/4 for now
M=int(r.gauss(mu=4,sigma=1)) # Beats per bar, might change since bar and arps will fit anyway.
M2=4 # note that is said beat (inverted), will stay 4 for a while

# Choose a tempo between 1.5b/s and 4b/s.
Q=r.randint(90,240)
# Choose a song length between 2:00 and 6:00.
songLength=r.randint(120,360)
# Turn that into minutes.
songLength=float(songLength/60)
# Calculate the number of beats that is in a song.
beats=songLength*Q
# A bar has M beats. Round up to match the length as close as possible.
bars=ceil(beats/M)

# Default note length
L=1 # eighths
L2=8
# Voice
V=4 # Number of voices, the main, the second main, the base, and the drum
# These are important in some way. The variables are what makes ABC
# But there are also a few non-standard variables that'll help
instrument='80' # Square wave
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
# A dictionary of all the states
statesDic={'0':{'name':'I','notes':[0,4,7],'next':['1']}, # State 1 will always be the tonic.
           '1':{'name':'II','notes':[2,6,9],'next':['2','3']}, # State 2 will only have majors.
           '2':{'name':'II','notes':[2,6,9],'next':['2','3','4']}, # State 3 will feature minors.
           '3':{'name':'ii','notes':[2,5,9],'next':['2','3','4']},# It might also have others later on.
           '4':{'name':'I','notes':[0,4,7],'next':['0']}} # State 4 will bring it back to the tonic.
# If progressions will be generated progressively eventually, it should be making sensible circles.

# A place for all the songs.
songDic={
    "lead":[],
    "lead2":[], # This will be implemented later.
    "lead3":[], # More variety is better.
    "bass":[],
    "arp":[], # Steady reimplmentation.
    "drum1":[], # A series of booleans to denote the circle is complete.
    "drum2":[], # The drums won't be added just yet.
    "drum3":[], # Not until an advantage has been found.
    "voice":[], # It'll get there eventually.
    "bar":[], # Bar numbers.
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "fail":[True,True,True] # A list of chaos induced failures.
}

# The voice track is for lyrics, these lyrics don't have to make sense, they're procedurally generated words.
# This makes a word of x syllables, x being the number of actual notes, i.e. not rests, in a bar.
# The list of consonants to be used at the beginning of a syllable.
cons=['b','c','d','f','g','h','j','k','l','m','n','p','qu','r','s','t','v','w','x','y','z','ch','sh','th']
# The list of consonants to be used at the end of a syllable.
cons2=['b','c','d','f','g','h','k','l','m','n','p','r','s','t','w','x','y','z','ch','sh','rk','th','ts','ng','nk']
# Every syllable has 1 vowel and is the definition of a syllable in a basic sense.
vow=['a','e','i','o','u']
# Make a syllable.
def syl():
    # The result string.
    result=''
    #Does it start with a consonant?
    if c([True,False]):
        result+=r.choice(cons)
    #Then add a vowel
    result+=r.choice(vow)
    #Does it end with a consonant?
    if c([True,False]):
        result+=r.choice(cons)
    return result
# Make a word with x syllables.
def word(x):
    # The result string.
    result=''
    # Run syl() as many times as it's been given.
    for y in range(x):
        result+=syl()
    return result


# Fill the bar track with all the numbers.
for x in range(bars):
    songDic["bar"]=x
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
            noteLength=int(abs(r.gauss(0,1.5))+1)
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
    # The result list.
    result=[]
    # Go through the entire song.
    for i in range(bars):
        # If the current state is I (tonic):
        if statesDic[state]['name']=='I':
            # Create a bass bar and add it to the bass track.
            result.append(bassBar(statesDic[state]['notes']))
        else:
            # Make sure the increment is between 0 and 6 (7 would be I one octave higher).
            incrementalValue=r.randint(0,6)
            # Choose a note on the scale to be the chord.
            baseChord=statesDic[state]['notes']
            for x in baseChord:
                # Elevate all notes of the chord to match with the notes.
                x+=incrementalValue
            # Make the bass bar and add it to the bass track.
            result.append(bassBar(baseChord))
        # Add True or False to the drum1 track depending on whether it's state 0.
        songDic["drum1"].append(True) if state=='4' else songDic["drum1"].append(False)
        # Add the state to the state track.
        songDic["state"].append(state)
        # Add the name of the chord played to the right track.
        songDic['chord'].append(notes[statesDic[state]['notes'][0]])
        # Change the state.
        state=r.choice(statesDic[state]['next'])
    return result

# Make a lead bar, the first note is based on the bass.
def leadBar(state,bassBar):
    # The result list.
    result=[]
    # The note counter.
    x=(M/M2)/(L/L2)
    # Find a note that exists.
    y=0
    while True:
        # Check to see if the first note has an incident.
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
    for i in bassNotes:
        # This then gets added.
        result.append(leadBar(state,i))
    return result

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
'''
Here be main
'''
# All the bass notes.
songDic["bass"]=bassify(state)
# Make the whole lead section from the bass notes.
songDic["lead"]=leadify(state,songDic["bass"])

# First voice (lead)
output+='V:1\n'
# Don't use the first and last three bars for an intro/outro.
output+='|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|'
for i in range(3,bars-3):
        # Write down the bar with 1/3 chance of failure.
    if r.choice([True,True,False]):
        for j in songDic["lead"][i]:
            output+=j
        songDic["fail"].append(False)
    else:
        output+='z'+str(M*2)
        songDic["fail"].append(True)
    output+='|'
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|]\n\n'

# Second voice (bass).
output+='V:2\n'
for i in range(bars):
    for j in songDic["bass"][i]:
        output+=j
    output+='|'
output+=']\n\n'

# Third voice (drums).
output+='V:3\n'
output+='z'+str(M*2)
# Make the initial drum roll.
roll=drumroll()
# Go through the whole song, starting at bar 2, ending one bar before the end.
for i in range(1,bars-1):
    # Add the current roll to the song.
    output+=roll+'|'
    # Upon the end of a cycle, make a new roll.
    if songDic['drum1'][i]:
        roll=drumroll()
# voice end, let it die.
output+='|z'+str(M*2)+'|]\n\n'

# Fourth voice, the basic drums.
output+='V:4\n'
# Intro of rests.
output+='z'+str(M*2)+'|'
# Make the initial drum roll.
roll=drumBase()
for i in range(1,bars-1):
    output+=roll+'|'
    if songDic['drum1'][i]:
        roll=drumBase()
output+='|z'+str(M*2)+'|]\n\n'

# Fifth voice, eventually the drums are just going to be deconstructed into their own tracks, but for now this adds accents where they're needed.
output+='V:5\n'
# This voice's only task is to put a crash (or an open hi-hat as analog) at the end of each progression cycle.
for i in range(bars):
    # It'll do this throughout the song, disregarding intros and outros.
    output+='z'+str(M*2-1)+drumDic['hatopen']+'|' if songDic['drum1'][i] else 'z'+str(M*2)+'|'
output+=']\n\n'

# Sixth voice, time for a bit of chaos.
output+='V:6\n'
# Don't use the first and last three bars for an intro/outro.
output+='|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|'
for i in range(3,bars-3):
    # Write down the bar if V1 failed.
    if songDic["fail"][i]:
        for j in songDic["lead"][i]:
            output+=j
    else:
        # Otherwise, write down the bar with 1/3 chance of success.
        if r.choice([True,True,False]):
            output+='z'+str(M*2)
        else:
            for j in songDic["lead"][i]:
                output+=j
    output+='|'
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|]\n\n'

# Seventh voice, whatever.
output+='V:7\n'
# Make a fresh start.
songDic["lead2"]=leadify(state,songDic["bass"])
# Don't use the first and last three bars for an intro/outro.
output+='|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|'
for i in range(3,bars-3):
    # Write down the bar with 1/2 chance of success.
    if r.choice([True,False]):
        output+='z'+str(M*2)
    else:
        for j in songDic["lead2"][i]:
            output+=j
    output+='|'
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|]\n\n'

# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.abc','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
# Flush the output, free up space, plus the parser can't handle a string that long.
output=''
# Meta information
print(str(oldScale)+' in '+K+' at '+str(Q)+'BPM\nSong length is '+str(songLength)[0]+':'+str(int((songLength%1+.01)*60)))
'''todo: actual chord progression
the reason it's not here is because this version bases itself on the notes, not the chords
i.e. it makes the notes first, then the chords from that.
Other ways of making a song proc-gen is starting with drums, a base note (i.e. not chords), or just a function for the pitch (e.g. sine)'''
# Time to parse the ABC with
import music21 as mu
# package for further processing
song=mu.converter.parse(T+'.abc')
# one such process is transposing according to the key.
transpose={'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':-5,'G#':-4,'A':-3,'A#':-2,'B':-1}
# This is where the key is being actually used.
song.parts[0].transpose(transpose[K],True)
song.parts[5].transpose(transpose[K],True)
song.parts[6].transpose(transpose[K],True)
# The bass goes down an octave, to make it a bass.
song.parts[1].transpose(transpose[K]-12,True)
# Drums don't get transposed.
#song.parts[3].transpose(transpose[K]*-1,True)
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
