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
T="song" # Song title
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
M=4 # Beats per bar, might change since bar and arps will fit anyway.
M2=4 # note that is said beat (inverted), will stay 4 for a while
# Choose a tempo between 1b/s and 4b/s.
Q=r.randint(60,240)
# Choose a song length between 1:30 and 6:00.
songLength=r.randint(90,360)
# Turn that into minutes.
songLength=float(songLength/60)
# Calculate the number of beats that is in a song.
beats=songLength*Q
# A line has 5 bars, a bar has M beats. Round up to match the length as close as possible.
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
drumDic={'hatopen':'_G,,','hatclose':'_B,,','base1':'_C,,','base2':'C,,',
        'snare1':'D,,','snare2':'E,,','clave':'_e'}
# First choose which snare drum and base drum to use, since there's two of each.
snare=r.choice(['snare1','snare2'])
# No use in using both just yet, the difference is too minimal.
basedrum=r.choice(['base1','base2'])

# A routine that generates a bar
def bar():
    # The result list where everything is added to
    result=[]
    # A counter that counts the number of notes in a bar
    # It comes from M/L; in standard time with eighths that's (4/4)/(1/8)=8
    x=(M/M2)/(L/L2)
    # Pick a random note from the chosen scale
    note=notes[r.choice(scalesDic[scale])]
    while note=='z':
        note=notes[r.choice(scalesDic[scale])]
    # If the next note is a rest, use the previous note that was a note.
    note2=note
    while(x>0):
        # Check to see if the note is a rest, with 3/10th chance.
        if r.randint(1,10)<4:
            # The rest is the 'z' character, there's also 'x', but it won't show on the bar.
            note='z'
        else:
            # If it's a note, the next note is one at most 5 away from the current note, bounce up anything below 0. 
            y=abs(scalesDic[scale].index(notes.index(note))+r.randint(-5,+5))
            # It has to still be on the scale list.
            if y>len(scalesDic[scale])-1:
                # Bounce down the excess
                y=y-(y-len(scalesDic[scale]))-1
            note=notes[scalesDic[scale][y]]
            # A backup of the note is stored, because it's not a rest.
            note2=note
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
        # Restore the backup note, even if it wasn't a rest.
        note=note2
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
    lengths=[M*2,M]
    # Choose a length
    length=r.choice(lengths)
    # This next bit is pretty blatantly proc-gen, literally random stuff built upon the previous random step.
    if length!=M*2:
        # Random boolean in Python is fun
        alternating=r.choice([True,False]) # Generate a random number, turn int into boolean
        # Make a new note that's one octave higher or lower
        altNotes=[note+'\'',note+',']
        altNote=r.choice(altNotes)
        # Fill up the bar
        flag=True
        for x in range(int(M*2/length)):
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
        result+=note+str(M*2)
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
                    note2=y[0]+y[1].upper()+','
                else:
                    note2=y[0].upper()+','
                # A note is found, break the loop
                break
        # Whether we broke out the loop or found no note, add the note2 to the staff.
        result.append(bass(note2))
    return result


# Every bar has a chord, which will be used for the arp and is based on the bass note. Eventually it can be replaced with an actual chord
def arpeggio(note,length):
    # The result string.
    result=''
    # The synergy of a dictionary and its index list is not to be understated.
    chord=flavorDic[r.choice(flavor)]
    # If the chord length is 4 notes, choose whether it goes up or down.
    up=r.choice([True,False])
    # Separate activity based on the chord length.
    for x in range(length*2):
        # Length 2 should flip between the two notes.
        if len(chord)==2:
            #y+notes.index(note)
            # Length 1 means a note is 1/1 beat, write / for half time
            # Length 4 means a note is 1/4 beat, write /4 for eighth time
            for y in chord:
                # For greek chords, the chords are from the scale itself.
                result+=notes[scalesDic[scale][y+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
            for y in chord:
                result+=notes[scalesDic[scale][y+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
        # Length 3 should oscillate between the notes.
        if len(chord)==3:
            # Oscillation goes one longer than the actual chord, doing the 2nd note again at the end.
            for y in chord:
                result+=notes[scalesDic[scale][y+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
            result+=notes[scalesDic[scale][chord[1]+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
        # Length 4 should go up or down the notes.
        if len(chord)==4:
                if up:
                    for y in chord:
                        result+=notes[scalesDic[scale][y+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
                else:
                    for y in range(len(chord)):
                        result+=notes[scalesDic[scale][chord[len(chord)-y-1]+scalesDic[scale].index(notes.index(note))]]+'/'+str(length)+' '
    return result

# The arp writing routine
def apreggify(bassNotes):
    result=[]
    # Choose a length, which is actually going to be really small and should be constant
    length=r.choice([1,2])
    # Take a bar from the bass notes                              
    for i in bassNotes:
        # Put each first note of it through the wrangler
        # Since it's already sorted, bass notes is easier than sorting out the actual notes again.
        if i[0]=='_':
            result.append(arpeggio((i[0]+i[1]),length))
        else:
            result.append(arpeggio(i[0],length))
    return result

# Create a string, filling one bar, containing just drums.
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
output+='\nz8|z8|]\n\n'

# For my next trick, I'll do the bass notes, which is the second voice
output+='V:2\n'
bassNotes=bassify(songNotes)
# This is for outputting the bass notes
output+='z'+str(M*2)+'|z'+str(M*2)+'|'+bassNotes[2]+'|'+bassNotes[3]+'|'+bassNotes[4]+'|\n'
# After a 2 bar intro, add the bass.
for i in range(lines-1):
    for j in range(5):
        for k in bassNotes[j+(i+1)*5]:
        # Add each bar of the note list to the output
            output+=k
        # And put a | delimiter at the end of it.
        output+='|'
    # End of the line, unless end of song
    if i*j<(lines-1)*4:
        output+='\n'
# Add two more notes as an outro, nothing spectecular, but it's much more graceful.
note=notes[r.choice(scalesDic[scale])].upper()
output+=bass(note)+'|'
note=notes[r.choice(scalesDic[scale])].upper()
output+=bass(note)
# voice end
output+='|]\n\n'

# For my last trick, I'll do an arp
# After a 4 bar intro, add the arps.
output+='V:3\n'
'''
# Introducing the brand new, all improved, 2.0 version of chord progressions
# Featuring your all time favorites such as majors, minors, 7ths and power chords
# palette=['C','D_','D','E_','E','F','G_','G','A_','A','B_','B']
flavor=['','m','7','M7','m7','','-3','sus4','sus2'] # blank is in there twice, making it twice as likely to be chosen.
flavorDic={'':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'M7':[0,4,7,11],'m7':[0,3,7,10],'aug':[0,4,8],'-3':[0,7],'sus4':[0,6,7],'sus2':[0,3,7]}

flavor=['triad','seventh','power','sus4','sus2']
flavorDic={'triad':[0,2,4],'seventh':[0,2,4,6],'power':[0,4],'sus4':[0,3,4],'sus2':[0,1,4]}

arpNotes=arpeggify(bassNotes)
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|'+arpNotes[4]+'|\n'
for i in range(lines-1):
    for j in range(5):
        for k in arpNotes[j+(i+1)*5]:
        # Add each bar of the note list to the output
            output+=k # This can be changed so instead it outputs alternating octaved notes in half, quarter, or eighths, which should be a def
        # And put a | delimiter at the end of it.
        output+='|'
    # End of the line, unless end of song
    if i*j<(lines-1)*4:
        output+='\n'
# voice end
output+='z8|z8|]\n\n'
'''
# Arpeggiator is out for repairs, the arpeggating routines still hang about, but aren't called.
# So instead I now have a drum machine, this time it's going to make random bars that'll be repeated over and over for 2 lines.
# Later it'll be layering stuff.

# Add a line of rests.
output+='z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|z'+str(M*2)+'|\n'
# Since it's going over two lines, there needs a flag to see if a new roll has to be made.
first=True
# Make a drum roll.
roll=drumroll()
# Go through the whole song.
for i in range(lines-1):
    # A line is still 5 bars long
    for j in range(5):
        output+=roll+"|"
    # The makings of a new roll can perfectly fall in line with i.
    if first:
        first=False
    # But it's still cleaner to recycle, so only make a fresh one once the old one's done.
    else:
        first=True
        roll=drumroll()
    # The basic fanfare to see if the song has ended.
    if i*j<(lines-1)*4:
        output+='\n'
# voice end, add a last roll for good measure.
output+=drumroll()+'|z8|]\n\n'


# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
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
transpose={'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':-5,'G#':-4,'A':-3,'A#':-2,'B':-1}
# This is where the key is being actually used.
song.transpose(transpose[K],True)
# Drums don't get transposed.
song.parts[2].transpose(transpose[K]*-1,True)
# Open the song in Musescore for final touches.
print(scale+' in '+K+' at '+str(Q)+'BPM\nSong length is '+str(songLength)[0]+':'+str(int((songLength%1+.01)*60)))
song.show()
# Now everything works.
