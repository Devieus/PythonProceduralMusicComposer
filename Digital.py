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
T="Digital" # Song title
# Key
keys=['C','C# ','D','D# ','E','F','F# ','G','G# ','A','A# ','B']
K=r.choice(keys) # Random key, they're all the same mostly
# and will only be used at the end for transposition.
scales=['Penta','Major','Minor','Dev']
# Dev is my personal scale that drops the septet altogether, because I dislike the B sound in C
scalesDic={
    'Penta':[1,4,6,8,11,13,16,18,20,23,-1],
    'Major':[1,3,4,6,8,9,11,13,15,16,18,20,21,23,-1],
    'Minor':[1,3,4,6,7,9,11,13,15,16,18,19,21,23,-1],
    'Dev':[1,4,6,8,9,11,13,16,18,20,21,23,-1]
}
# 'BC'D'EF'G'A'BC
scale=r.choice(scales)
# Meter, 4/4 for now
M=4 # Beats per bar, might change since bar and arps will fit anyway.
M2=4 # note that is said beat (inverted), will stay 4 for a while
# Choose a tempo between 1/s and 4/s.
Q=r.randint(60,240)
# Choose a song length between 1:30 and 6:00.
songLength=r.randint(90,360)
# Turn that into minutes.
songLength=float(songLength/60)
# Calculate the number of beats that is in a song.
beats=songLength*Q
# A line has 5 bars, a bar has M beats.
# Round up to match the length as close as possible.
lines=ceil(beats/(5*M))
# Default note length
L=1 # eighths
L2=8
# Voice
V=3 # Number of voices, the main, the base, and the arp (not used)
# These are important in some way. The variables are what makes ABC
# But there are also a few non-standard variables that'll help
instrument='80' # Square wave
sequence=1 # track 1
# Make the basic output
output='X:'+X+'\nT:'+T+'\nK:'+K+'\nM:'+str(M)+'/'+str(M2)+'\nQ:'+str(Q)+'\nL:'+str(L)+'/'+str(L2)+'\n%%MIDI instrument%%:'+instrument+'\nV:1\n'
# All these variables are set differently in the ABC, but that'll sort itself out.

# Introducing the brand new, all improved, 2.0 version of chord progressions
# Featuring your all time favorites such as majors, minors, 7ths and power chords
# palette=['C','D_','D','E_','E','F','G_','G','A_','A','B_','B']
flavor=['','m','7','M7','m7','','-5','sus4','sus2'] # blank is in there twice, making it twice as likely to be chosen.
flavorDic={'':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'M7':[0,4,7,11],'m7':[0,3,7,10],'aug':[0,4,8],'-5':[0,7],'sus4':[0,6,7],'sus2':[0,3,7]}
    
# The concept here is to randomly generate a sequence of
#  - Notes, represented by a-g,A-G
#  - Note lengths, represented by numbers after the note
#  - Chords in the second track
# Then end it all with the end token, which looks like |]


# all the valid notes in a neat 5x5 grid
notes=['_A,','A,' ,'_B,','B,','C',
       '_D','D' ,'_E' ,'E' ,'F',
       '_G','G' ,'_A' ,'A' ,'_B',
       'B' ,'c,','_d' ,'d' ,'_e',
       'e' ,'f' ,'_g' ,'g' ,'z']
# A routine that generates a bar
def bar():
    # The result list where everything is added to
    result=[]
    # A counter that counts the number of notes in a bar
    # It comes from M/L; in standard time with eighths that's (4/4)/(1/8)=8
    x=(M/M2)/(L/L2)
    while(x>0):
        # Pick a random note from the chosen scale
        note=notes[r.choice(scalesDic[scale])]
        # This is to make sure the note fits the bar
        fitting=False
        # Pick notes until something fits.
        while(not fitting):
            # Random note length, because only eighths is boring as all fuck.
            notelength=int(abs(r.gauss(0,1.5))+1)
            # Check to see if the note fits the bar.
            if(notelength<=x):
                # It does.
                fitting=True
        # If the bar isn't full yet, add the note.
        if(notelength>1):
            # If the note is actually longer than an eighth, it needs a number.
            result.append(note+str(notelength))
        else:
            result.append(note)
        # Another bit of the bar filled.
        x-=notelength
    # The bar is complete.
    return result

# A routine that makes a song
def songify():
    result=[]
    # x bars per song
    for k in range(lines*5):
        result.append(bar())
    return result

# The bass consists of the first actual note of the bar and is made fun of.
# If no such note exists, because the whole bar is rests, send a C (might change this later on).
def bass(note):
    # Output string of the routine
    result=''
    # These are the note lengths, 8=whole, 1=eights, you do the math.
    lengths=[8,4,2,1]
    # Choose a length
    length=r.choice(lengths)
    # This next bit is pretty blatantly proc-gen, literally random stuff built upon the previous random step.
    if length!=8:
        # Random boolean in Python is fun
        alternating=r.choice([True,False]) # Generate a random number, turn int into boolean
        # Make a new note that's one octave higher or lower
        altNotes=[note+'\'',note+',']
        altNote=r.choice(altNotes)
        # Fill up the bar
        flag=True
        for x in range(int(8/length)):
            if flag:
                # Add the input node to the output string, which is one bar's worth of bass note
                result+=note+str(length)
                # This routine is called every bar, so it's possible one bar has a whole note, then 8 alternating, then 4 non-alternating
                if alternating:
                # toggle the flag
                    flag=False
            else:
                # Add the alternated note instead.
                result+=altNote+str(length)
                flag=True
    else:
        result+=note+'8'
    return result

# The bass writing routine.
def bassify(songNotes):
    result=[]
    # Which is the first note of the bar.
    for x in songNotes:
        # Unless it's a rest.
        for y in x:
            # This is for edge cases where there is no note on the bar, it'll default to C.
            note2='C'
                # A note is a name, a pitch modifier and a length (the latter is optional), if the name is 'z' it's a rest.
            if not y[0]=='z':
                # Check for accidentals.
                if y[0]=='_':
                    # Bass notes will be one octave lower no matter what.
                    note2=bass(y[0]+y[1].upper()+',')
                else:
                    note2=bass(y[0].upper()+',')
                # A note is found, break the loop
                break
        # Whether we broke out the loop or found no note, add the note2 to the staff.
        result.append(note2)
    return result

# Every bar has a chord, which will be used for the arp and is based on the bass note. Eventually it can be replaced with an actual chord
def progression(note,length):
    # Uppercase the note name, so it won't ever go out of bounds.
    note=note.upper()
    # The result string
    result=''
    # Choose a flavor
    chordflavor=''
    # The synergy of a dictionary and its index list is not to be understated
    chord=flavorDic[chordflavor]
    # Now it needs to be resolved to the 2 to 4 notes.
    # For playback purposes of course, but also for the arp.
    up=r.choice([True,False])
    # Separate activity based on the chord length
    # Length 2 should flip between the two notes, possibly with extra octave support later.
    for x in range(length*2):
        if len(chord)==2:
            # Length 1 means the whole arp takes 1/1 note, write / for half time
            # Length 4 means the whole arp takes 1/4 note, write /4 for eighth time
            for y in chord:
                result+=notes[y+notes.index(note)]+'/'+str(length)+' '
            for y in chord:
                result+=notes[y+notes.index(note)]+'/'+str(length)+' '
        # Length 3 should oscillate between the notes.
        if len(chord)==3:
            # Oscillation goes one longer than the actual chord, doing the 2nd note again at the end.
            for y in range(len(chord)+1):
                if y>2:
                    result+=notes[chord[1]+notes.index(note)]+'/'+str(length)+' '
                else:
                    result+=notes[chord[y]+notes.index(note)]+'/'+str(length)+' '
        # Length 4 should go up or down the notes.
        if len(chord)==4:
                if up:
                    for y in chord:
                        result+=notes[y+notes.index(note)]+'/'+str(length)+' '
                else:
                    for y in range(len(chord)):
                        result+=notes[chord[len(chord)-y-1]+notes.index(note)]+'/'+str(length)+' '
    return result

# The arp writing routine
def progressify(bassNotes):
    result=[]
    # Choose a length, which is actually going to be really small and should be constant
    length=r.choice([1,2])
    # Take a bar from the bass notes                              
    for i in bassNotes:
        # Put each first note of it through the wrangler
        # Since it's already sorted, bass notes is easier than sorting out the actual notes again.
        if i[0]=='_':
            result.append(progression((i[0]+i[1]),length))
        else:
            result.append(progression(i[0],length))
    return result

'''Here be actual main'''
# Generate a song
# The notes
songNotes=songify()
# This is for outputting the song notes
for i in range(lines):
    for j in range(5):
        for k in songNotes[j+i*5]:
        # Add each bar of the note list to the output
            output+=k
        # And put a | delimiter at the end of it.
        output+='|'
    # End of the line'
    if i*j<(lines-1)*4:
        output+='\n'
# voice end
output+=']\n\n'

# For my next trick, I'll do the bass notes, which is the second voice
output+='V:2\n'
bassNotes=bassify(songNotes)
# This is for outputting the bass notes
output+='z8|z8|'+bassNotes[2]+'|'+bassNotes[3]+'|'+bassNotes[4]+'|\n'
# After a 2 bar intro, add the bass.
for i in range(lines-1):
    for j in range(5):
        for k in bassNotes[j+i*5]:
        # Add each bar of the note list to the output
            output+=k
        # And put a | delimiter at the end of it.
        output+='|'
    # End of the line, unless end of song
    if i*j<(lines-1)*4:
        output+='\n'
# voice end
output+=']\n\n'

# For my last trick, I'll do an arp
# After a 4 bar intro, add the arps.
output+='V:3\n'
progNotes=progressify(bassNotes)
output+='z8|z8|z8|z8|'+progNotes[4]+'|\n'
for i in range(lines-1):
    for j in range(5):
        for k in progNotes[j+i*5]:
        # Add each bar of the note list to the output
            output+=k # This can be changed so instead it outputs alternating octaved notes in half, quarter, or eighths, which should be a def
        # And put a | delimiter at the end of it.
        output+='|'
    # End of the line, unless end of song
    if i*j<(lines-1)*4:
        output+='\n'
# voice end
output+=']\n\n'

# output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.abc','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
# Flush the output, free up space, plus the parser can't handle a string that long.
output=''
'''todo: actual chord progression
the reason it's not here is because this version bases itself on the notes, not the chords
i.e. it makes the notes first, then the chords from that.
Other ways of making a song proc-gen is starting with drums, a base note (i.e. not chords), or just a function for the pitch (e.g. sine)'''
# Time to parse the ABC with
import music21 as mu
# package for further processing
song=mu.converter.parse(T+'.abc')
# one such process is transposing according to the key.
transpose={'C':0,'C# ':1,'D':2,'D# ':3,'E':4,'F':5,'F# ':6,'G':-5,'G# ':-4,'A':-3,'A# ':-2,'B':-1}
# This is where the key is being actually used.
song.transpose(transpose[K])
# Open the song in Musescore for final touches.
song.show()
# Now everything works.
