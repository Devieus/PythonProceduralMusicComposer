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
T="Overturn" # Song title
# Key
keys=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
K=r.choice(keys) # Random key, they're all the same mostly
# and will only be used at the end for transposition.
# scales=['Penta','Major','Minor','Dev']
scales=['Major','Minor','Dev','Pentatonic']
# Dev is my personal scale that drops the septet altogether, because I dislike the B sound in C
scalesDic={
    'Major':[1,3,4,6,8,9,11,13,15,16,18,20,21,23],
    'Minor':[1,3,4,6,7,9,11,13,15,16,18,19,21,23],
    'Dev':[1,4,6,8,9,11,13,16,18,20,21,23],
    'Pentatonic':[1,4,6,8,11,13,16,18,20,23]
}
scale=r.choice(scales)
# Meter, 4/4 for now
M=int(r.gauss(mu=4,sigma=1)) # Beats per bar, might change since bar and arps will fit anyway.
M2=4 # note that is said beat (inverted), will stay 4 for a while

# Choose a tempo between 2b/s and 4b/s.
Q=r.randint(120,240)
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
notes=['_A,','A,' ,'_B,','B,','C',
       '_D','D' ,'_E' ,'E' ,'F',
       '_G','G' ,'_A' ,'A' ,'_B',
       'B' ,'c','_d' ,'d' ,'_e',
       'e' ,'f' ,'_g' ,'g']

# Let's hit some things.
drum=['hatopen','hatclose','base1','base2','snare1','snare2','clave']
drumDic={'hatopen':'_G,,','hatclose':'_B,,','base1':'_C,,','base2':'=C,,',
        'snare1':'=D,,','snare2':'=E,,','clave':'_e'}
# First choose which snare drum and base drum to use, since there's two of each.
snare=r.choice(['snare1','snare2'])
# No use in using both just yet, the difference is too minimal.
basedrum=r.choice(['base1','base2'])

# One possible way to start the music is by having the bass do chord progressions.
# It's a simple set of progressions for now.
# Though it looks pretty complex and there's some redundant names, they're all different states.
# Any new progression can enhance existing states, which would increase variety without increasing complexity.
# Make a finite state machine.
state='0'
# A list of all states, 9 for now.
states=['0','1','2','3','4','5','6','7','8']
# A dictionary of all the states
statesDic={'0':{'name':'I','notes':[4,8,11],'next':['1','2','3']}, #CEG
           '1':{'name':'iii','notes':[3,8,11],'next':['7']}, #EGB
           '2':{'name':'IV','notes':[1,4,9],'next':['8']}, #FAC
           '3':{'name':'vi','notes':[1,4,8],'next':['5']}, #ACE
           '4':{'name':'ii','notes':[1,6,9],'next':['7','8']}, #DFA
           '5':{'name':'IV','notes':[1,4,9],'next':['7','8']},
           '6':{'name':'ii','notes':[1,6,9],'next':['0']},
           '7':{'name':'IV','notes':[1,4,9],'next':['0']},
           '8':{'name':'V','notes':[3,6,11],'next':['0']}} #GBD

# Make a bass bar based on the progressions.
def bassBar(state):
    # The result list where everything is added to.
    result=[]
    # A counter that counts the notes in a bar.
    x=(M/M2)/(L/L2)
    while x>0:
        # Pick a random note from the available selection.
        note=notes[r.choice(statesDic[state]['notes'])]
        # Pick a length for the note.
        fitting=False
        # It has to fit.
        while not fitting:
            # A random note length that favors eighths.
            noteLength=int(abs(r.gauss(0,1.5))+1)
            if noteLength<=x:
                fitting=True
                x-=noteLength
        if noteLength>1:
            # If the note is longer than L's default value, add the number
            result.append(note+str(noteLength))
        else:
            result.append(note)
    # At the end of the bar, the state has to change;
    # this can be done anywhere, so it won't be done here.
    return result

# Make the whole bass.
def bassify(state):
    result=[]
    for i in range(bars):
        result.append(bassBar(state))
        state=r.choice(statesDic[state]['next'])
    return result

# Make a lead bar, the first note is based on the bass.
def leadBar(state,bassBar):
    # The result list.
    result=[]
    # The note counter.
    x=(M/M2)/(L/L2)
    # Check to see if the first note has an incident.
    if bassBar[0][0]=='_':
        # If it does, take it into account.
        note=bassBar[0][0]+bassBar[0][1]
    else:
        # If it doesn't, take just the note.
        note=bassBar[0][0]
    # Store the note in a backup.   
    backupNote=note
    while x>0:
        fitting=False
        while not fitting:
            noteLength=int(abs(r.gauss(0,1.5))+1)
            if noteLength<=x:
                fitting=True
                x-=noteLength
        if noteLength>1:
            # If the note is longer than L's default value, add the number
            result.append(note+str(noteLength))
        else:
            result.append(note)
        # Retrieve the backup to calculate the next note.
        note=backupNote
        # Check to see if the next note should be a rest.
        if r.randint(1,10)<4:
            note='z'
        else:
            # Some notes in the progression chord aren't in the scale.
            if scalesDic[scale].count(notes.index(note))>0:
                # Choose a random note from the scale to be the next note up to 5 notes away.
                y=abs(scalesDic[scale].index(notes.index(note))+r.randint(-5,+5))
                # It has to still be on the scale list.
                if y>len(scalesDic[scale])-1:
                    # Bounce down the excess
                    y=y-(y-len(scalesDic[scale]))-1
                note=notes[scalesDic[scale][y]]
            # E is not in the minor scale for example, so just make the note 'C', or tonic, which is always in there.
            else:
                note='C'
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
    # There's 8 hits in a bar.
    x=(M/M2)/(L/L2)
    # There's 1 chance in 4 there's a rest.
    while x>0:
        if r.choice([True,False,False,False]):
            result+='z'
        else:
            # Otherwise, there's going to be a hit, which will always be one beat long.
            result+=drumDic[r.choice(drum)]
        x-=1
    return result
'''
Here be main
'''
# All the bass notes.
bassNotes=bassify(state)
# Make the whole lead section from the bass notes.
leadNotes=leadify(state,bassNotes)

# First voice (lead)
output+='V:1\n'
# Don't use the first and last three bars for an intro/outro.
output+='|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|'
for i in range(3,bars-3):
    for j in leadNotes[i]:
        output+=j
    output+='|'
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|]\n\n'

# Second voice (bass).
output+='V:2\n'
for i in range(bars):
    for j in bassNotes[i]:
        output+=j
    output+='|'
output+=']\n\n'

# Third voice (drums).
output+='V:3\n'
output+='|z'+str(M*2)
# Since it's going over bars, there needs a flag to see if a new roll has to be made.
roll=drumroll()
# Go through the whole song, starting at bar 2, ending one bar before the end.
for i in range(1,bars-1):
    # Add the current roll to the song.
    output+=roll+'|'
    # The makings of a new roll can perfectly fall in line with i.
    if i%4==0:
        roll=drumroll()
# voice end, add a last roll for good measure.
output+='|z'+str(M*2)+'|]\n\n'

# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.abc','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
# Flush the output, free up space, plus the parser can't handle a string that long.
output=''
# Meta information
print(scale+' in '+K+' at '+str(Q)+'BPM\nSong length is '+str(songLength)[0]+':'+str(int((songLength%1+.01)*60)))
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
# The bass goes down an octave, to make it a bass.
song.parts[1].transpose(transpose[K]-12,True)
# Drums don't get transposed.
#song.parts[3].transpose(transpose[K]*-1,True)
# Open the song in Musescore for final touches.
song.show()
# Now everything works.
