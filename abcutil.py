import random as r
def scaleGen():
    # A second way of generating scales.
    # It's essentially the same as filling a bar.
    deltaScale=[]
    while len(deltaScale)<5:
        # There are many, many ways of making sure it's at least 5 notes long, but rebooting deltaScale is the easiest.
        deltaScale=[]
        y=12
        while y>0:
            fitting=False
            while not fitting:
                x=int(r.gauss(1,2)+.5)
                if sum(deltaScale)+x<=12 and x>0:
                    fitting=True
                    y-=x
            deltaScale.append(x)
    # Make sure it's at least 5 notes long.
    # A delta scale indicating the sum of all previous steps, so they correspond to the notes 1:1.
    resultScale=[0]
    # Double the deltaScale.
    for x in range(len(deltaScale)):
        deltaScale.append(deltaScale[x])
# Add the previous steps in summation to the deltaScale.
    for x in range(len(deltaScale)):
        # It's entirely possible to make a summation routine, but whatever, this is science.
        resultScale.append(resultScale[x]+deltaScale[x])
    return resultScale

def scaleGen2():
    # Default scale is blank, but make sure there're two whole notes in there.
    # The reason for this is because it favors a heptatonic scale, favoring hexatonic and octatonic scale second.
    deltaScale=[0,0,0,2,0,0,2,0,0,2,0,0]
    # Add one to a random step in the scale eight times to make it 12 steps, or a whole octave.
    for x in range(6):
        # Select a random index of the scale and add 1 to it.
        deltaScale[r.randint(0,len(deltaScale)-1)]+=1
    # Prune all the zeroes from the scale
    while deltaScale.count(0)>0:
        deltaScale.remove(0)
    # If the scale is minor i.e. skips the fourth key, make it hit the fourth anyway.
    y=0
    n=0
    for x in range(len(deltaScale)):
        y+=deltaScale[x]
        # Check to see if it hits the third, but not the fourth
        if y==3 and y+deltaScale[x+1]>4:
            n=x
            # Transfer one from somewhere so it hits the fourth
            deltaScale[r.randint(x,len(deltaScale)-1)]-=1
            if deltaScale.count(0)>0:
                deltaScale.remove(0)
            # Then either transfer it before it hits three (possibly skipping 3), or after (still hitting 3)
            deltaScale.insert(x,1) if r.choice([True,False]) else deltaScale.insert(x+1,1)
            break
        elif y>3:
            break
    # Do it again for 8 (Ab)
    y=0
    for z in range(len(deltaScale)):
        y += deltaScale[z]
        if y == 8:
            # I don't want it to shift back to a minor, or shift the Ab back in there.
            deltaScale[r.randint(n+1, z)] -= 1
            # Move that one further up ahead.
            deltaScale[r.randint(z, len(deltaScale)-1)] += 1
            if deltaScale.count(0) > 0:
                # It's possible to remove a number this way, a 1 becomes a 0 and a note is repeated. Best not have that.
                deltaScale.remove(0)
            break
        if y > 8:
            break
    # Alternatively, it could hit both, or hit neither. Right now it's both.
    # Append the scale to itself so all chords can be played.
    for x in range(len(deltaScale)):
        deltaScale.append(deltaScale[x])
    # A the result scale indicating the sum of all previous steps, so they correspond to the notes 1:1.
    resultScale=[0]
    # scale's next value is its previous value plus scale's previous value
    for x in range(len(deltaScale)):
        # Store the value in another variable.
        resultScale.append(resultScale[x]+deltaScale[x])
    return resultScale

"""scale=scaleGen()
# Append the scale to itself so all chords can be played.
# for x in range(len(scale)):
#     scale.append(scale[x])
# Two octaves of notes starting from C.
notes=['C','_D','D','_E','E',
       'F','_G','G','_A','A',
       '_B','B' ,'c','_d','d',
       '_e','e' ,'f','_g','g',
       '_a','a','_b','b','c\'']
song=''
for x in scale:
    song+=notes[x]
song+='|'
scale=scaleGen()
for x in scale:
    song+=notes[x]
song+="|]"
#write out the notes of the deltascale from the notes
# for x in deltaScale:
#     song+=notes[x]
print("X:1\nT:test\nK:C#\nQ:200\nL:1/8\nV:1\n"+song)
song="X:1\nT:test\nK:C#\nM:4/4\nQ:200\nL:1/8\nV:1\n"+song
#song=open("Gamma.abc")
# Chords can be extracted thusly:
'''
I: [notes[deltaScale[0]],notes[deltaScale[2]],notes[deltaScale[4]]]
    this makes for example C, _E, G, or C minor
II: [notes[deltaScale[1]],notes[deltaScale[3]],notes[deltaScale[5]]]
    this makes for example _D, F, A, or _D aug
ii: [notes[deltaScale[1]],notes[deltaScale[3]]-1,notes[deltaScale[5]]]
    this makes for example _D, E, A, or _D aug sus2
'''
# These chords can be extracted and put into states.
# A progression would/could be made of I(0)->?(1)->?(2)->I(3)
# States then follow naturally and can be controlled, for example, state 2 shan't have a minor.


def randomScale():
    # Default scale is anything, so the base is 12 zeroes.
    scale=[0,0,2,0,0,0,0,0,0,2,0,0]
    # Add one to a random step in the scale 12 times to make it 12 steps, or a whole octave.
    import random as r
    for x in range(8):
        scale[r.randint(0,len(scale)-1)]+=1

    # Prune all the zeroes.
    while scale.count(0)>0:
        scale.remove(0)
    return scale

lengths=[0,0,0,0,0,0,0,0,0,0,0,0,0]
for x in range(10000):
    lengths[len(randomScale())]+=1
print(lengths)"""

scale=scaleGen()
# additional definitions that are placed elsewhere, but are otherwise part of the code.
# Some basic values related to ABC:
# Song number
X='1' # First song, increase this to make an opus
# Tempo
Q=r.randint(90,240) # Choose a tempo between 1.5b/s and 4b/s.
# Key
keys=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
K=keys[Q%12] # Based on tempo, they're all the same mostly, though this will favor the upper half very slightly.
# and will only be used at the end for transposition.

# Meter, x/4 for now
M=int(abs(r.gauss(4,2))+1) # Beats per bar, it will be at least 1, and maybe as high as 8, or 10.
M2=4*(r.choice([1,2])) # note that is said beat (inverted), will be 4 or 8
# Choose a song length between 3 and 5 progression cycles, taking tempo into account.
songLength=int(r.randint(3,5)*Q/180+0.5)

# Default note length.
L=1 # eighths if tempo is high, otherwise maybe sixteenths.
L2=r.choice([8,16]) if Q<180 else 8
# These are important in some way. The variables are what makes ABC
sequence=1 # track 1
# Make the basic output

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
# First choose which snare drum and base drum to use, since there's two of each.
snare=r.choice(['snare1','snare2'])
# No use in using both just yet, the difference is too minimal.
bassdrum=r.choice(['base1','base2'])
drum=['hatclose','clave','tomlow','tommidlow','tommid','tommidhi','tomhi','snare1','snare2',bassdrum]
drumDic={'hatopen':'_B,,','hatclose':'_G,,','base1':'_C,,','base2':'=C,,',
        'snare1':'=D,,','snare2':'=E,,','clave':'_e',
         'tomlow':'=F,,','tommidlow':'=G,,','tommid':'=A,,','tommidhi':'=B,,','tomhi':'=C,'}
#=['z',drumDic[snare],drumDic[bassdrum],'['+drumDic[snare]+drumDic[bassdrum]+']']

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
           '3':{'name':'m','notes':[0,-1,0],'next':['4','5','6','7','8']}, # as well as minors and can jump out.
           '4':{'name':'M','notes':[0,0,0],'next':['4','8']}, # State 4 will feature majors chords.
           '5':{'name':'m','notes':[0,-1,0],'next':['4','5','6','7','8']}, # Minors chords.
           '6':{'name':'Aug','notes':[0,1,1],'next':['4','5','6','7','8']}, # Augmented chords.
           '7':{'name':'Dim','notes':[0,-1,-1],'next':['4','5','6','7','8']}, # And diminished chords, and can jump out if it has to.
           '8':{'name':'M','notes':[0,0,0],'next':['0']}} # State 8 will bring it back to the tonic and will resolve the cadence.
# A basic chord
basic=[0,3,5]
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
            # See if the note is a grace note.
            elif y[0]=="{":
                # Nothing happens, nothing gets added, nothing gets written.
                pass
            # The next thing is a note.
            else:
                # If this next note is an accidental, increase the index.
                if y[0] == '_':
                    index += 1
                # Check to see if the current number is 0 (because it's the first) or positive or 4 syllables long.
                if result[x][len(result[x])-1]<0 or result[x][len(result[x])-1]>=4:
                    # If it isn't, add a new number to work on.
                    result[x].append(0)
                # If y doesn't have a number, i.e. it's length 1, (this is also true if the note is c', it just doesn't have a number)
                if len(y)==1+index or y[-1]=='\'':
                    # Add that 1 from the count.
                    result[x][len(result[x])-1]+=1
                else:
                    # Add the note length from the number.
                    result[x][len(result[x])-1] += int(y[-1])
    return result

def lyrics(length,voiceCount):
    result=[]
    for x in range(length):
        result.append([])
        for y in voiceCount[x]:
            result[x].append(word(y))
    return result

"""
Bass
"""
# Make a bass bar based on the progressions.
def bassBar():
    # The result list where everything is added to.
    result=[]
    # A counter that counts the notes in a bar.
    x=(M/M2)/(L/L2)
    while x>0:
        # Pick a random note from the available selection, or a rest with probability equal to the signature.
        note=notes[r.choice(scale)] if r.randint(1,10)>M/2 else 'z'
        # Pick a length for the note.
        fitting=False
        # It has to fit.
        while not fitting:
            # A random note length that goes up to a little over a quarter bar.
            noteLength=int(abs(r.gauss(0,((M/M2)/(L/L2))/4))+1)
            # Check if the note fits.
            if noteLength<=x:
                fitting=True
                # Subtract the note from x for future length checks.
                x-=noteLength
        # If the note is longer than the default note length, add the number to the note.
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
    result["bass"].append(bassBar())
    # Add the chord notes for future use.
    result["chordNotes"].append(statesDic[state]['notes'])
    # Elevate the state to the next one
    state=r.choice(statesDic[state]['next'])
    # Do that again until the state is back to the first.
    while state!="0" and state!="8":
        # Make sure the increment is between 1 and whatever's in the scale,
        # (except the last which would be I one octave higher and the first which is I).
        incrementalValue=scale[r.randint(1,len(scale)-2)]
        # Grab the notes belonging to that state.
        bassChord=[]
        for x in statesDic[state]['notes']:
            bassChord.append(x)
        for x in range(len(bassChord)):
            # Elevate all notes of the chord to match with the notes.
            bassChord[x]+=incrementalValue
        # Add this new list to the track.
        limited=[]
        for x in range(len(bassChord)):
            limited.append(bassChord[x]%12)
        result["chordNotes"].append(limited)
        # Make the bass bar and add it to the bass track.
        result["bass"].append(bassBar())
        # Add the state to the state track.
        result["state"].append(state)
        # Add the name of the chord played to the right track.
        if statesDic[state]['name']=='m':
            # This is, what passes for, a minor chord.
            result["chord"].append(str(notes[bassChord[0]]).upper()+'m')
        elif statesDic[state]['name']=='Dim':
            # This is, what passes for, a dim chord.
            result["chord"].append(str(notes[bassChord[0]]).upper()+'o')
        elif statesDic[state]['name']=='Aug':
            # This is, what passes for, an aug chord.
            result["chord"].append(str(notes[bassChord[0]]).upper()+'+')
        else:
            # This is, what passes for, a regular chord.
            result["chord"].append(notes[bassChord[0]].upper())
        # Change the state.
        state=r.choice(statesDic[state]['next'])
        # Add the current state,
    # Right now, state=8, so do the same thing as before.
    result["state"].append(state)
    # The chord name,
    result["chord"].append(str(notes[statesDic[state]['notes'][0]]))
    # And the bass bar.
    result["bass"].append(bassBar())
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
        if scale.count(notes.index(note))>0:
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
    # Resolve cadence if the progression has ended.
    if state=='8':
        x-=1
    # Store the note in a backup, that way if a rest is implemented, the note isn't lost.
    backupNote=note
    while x>0:
        fitting=False
        while not fitting:
            noteLength=int(abs(r.gauss(1,1.5))+0.5) if note!="z" else int(abs(r.gauss(0,1.5))+1)
            if noteLength<=x:
                fitting=True
                x-=noteLength
        if noteLength==0:
        # Make a grace note if length is 0.
            result.append("{"+note+"}")##DON'T GRACE FUCKING RESTS‼
        elif noteLength>1:
            # If the note is longer than L's default value, add the number
            result.append(note+str(noteLength))
        else:
            # Otherwise, it's just the note itself.
            result.append(note)
        # Retrieve the backup to calculate the next note.
        note=backupNote
        # Check to see if the next note should be a rest.
        if r.randint(1,M)<1:
            note='z'
        else:
            # Choose a random note from the scale to be the next note up to 5 notes away with some variance.
            y=abs(scale.index(notes.index(note))+int(r.gauss(0,2.5))) # abs() bounces negatives up.
            # It has to still be on the scale list.
            if y>len(scale)-1:
                # Bounce down the excess
                y=y-(y-len(scale))-1
            note=notes[scale[y]]
            backupNote=note
    if state=='8':
        # Mandatory break time.
        result+='z'
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
## From now on, just one drum thing, with 4 tracks, or 5, or 20, or none, whatever.

def drumriff():
    # The result dictionary
    result={
        "accent":"",
        "drums":"",
    }
    riffdrum=drumDic[r.choice(drum)] # It may seem petty, but if there's 2 of them, you'll be glad it's not the bass.
    while riffdrum==drumDic[bassdrum]:  # Make sure the grace notes aren't bass drums.
        riffdrum=drumDic[r.choice(drum)]  # The reason for this is because they don't make for good grace notes.
    startingGrace=int(r.gauss(0,1.3)) # Define the number of starting grace notes.
    if startingGrace>1: # If there is one,
        result["drums"]+="{" # add the opening bracket to denote grace notes.
        for x in range(startingGrace): # Fill the dictionary with said drum.
            result["drums"]+=riffdrum # This will add as many of the drums as needed.
        result["drums"]+="}"  # add the closing bracket to denote grace notes.
    # Now for the accent portion.
    riffdrum=drumDic[bassdrum]# Make sure it's a bass drum.
    result["accent"]+=riffdrum
    result["drums"]+="z" # I add a rest to the drums track,
    # this wasn't needed for the grace notes on the accents track, because grace notes have no length.
    riffdrum=otherDrum(riffdrum)
    # The gap, such as it is, is to be filled with a beat count equal to a remnant value, which in essence is (M/M2)/(2*L/L2)-2
    remnant=int((M/M2)*4)-1 # The second 2 is there because of the accents. Ideally there'd be more accents. The first 2 is to have 4 beats in 4/4.
    while remnant>0:
        remnant-=1
        reps=r.choice([0,1,2]) # There are various things a gap could be filled in with.
        if reps==0: # For instance, it could be filled with nothing.
            result["drums"]+="z2"
        elif reps==1: # Or it could be filled with one thing.
            if r.choice([True,False]): # There's 2 things that comply to the description of "one thing".
                result["drums"]+=riffdrum # Make 2 hits with a grace note in between.
                riffdrum=otherDrum(riffdrum)
                result["drums"]+="{"+riffdrum+"}"
                riffdrum=otherDrum(riffdrum)
                result["drums"]+=riffdrum # Triplets would not work, because Music21 doesn't communicate that well with musescore.
            else:
                result["drums"]+=riffdrum+"2" # Or a single hit.
        else: # For the two hitter, there's either none, one or two hits.
            for x in range(reps):
                pick=r.choice([0,1,2]) # They can mix.
                if pick==0:
                    # Either add a rest
                    result["drums"]+="z"
                elif pick==1:
                    result["drums"]+=riffdrum # Or add one note
                else: # Regular time.
                    result["drums"]+=riffdrum+"/" # Half time.
                    riffdrum=otherDrum(riffdrum)
                    result["drums"]+=riffdrum+"/"
    result["accent"]+="z"+str(int((M/M2)/(L/8))-2) # The accent will be seated during this portion of the riff.
    riffdrum=otherDrum(riffdrum) # The final accent drum can be anything.
    result["accent"]+=riffdrum if r.choice([True,False]) else "z" # end on an accent, or not.
    # possibly with a leading rest later on for more funky drums.
    # this goes for all drums, really.
    result["drums"]+="z"
    # Wrap both results into a list.
    result["drums"]=[result["drums"]]
    result["accent"]=[result["accent"]]
    return result # return the result dictionary, which looks something like {C,,C,,}G,,,F,,B,,G,,, with both G,,, in different tracks for accents.
    # These will be put into different voices so they can get more power.

def otherDrum(inputDrum):
    result=drumDic[r.choice(drum)]
    while result==inputDrum:  # Make sure the result is different.
        result=drumDic[r.choice(drum)]
    return result


"""
Arps
"""

# Every bar has a chord of 3 notes in length, which will be used for the arp. These chords are major, minor, aug and dim.
def arpeggio(chord,method):
    note0=notes[chord[0]+scale[basic[0]]]
    note1=notes[chord[1]+scale[basic[1]]]
    note2=notes[chord[2]+scale[basic[2]]]
    # The result string.
    result=''
    # Choose a length, which is actually going to be really small and should be constant
    reps=r.choice([1,2])
    # One edge case.
    if M==2 and reps==2:
        result+=note0+str(L2/8)+"["+note1+str(L2/8)+note2+str(L2/8)+"]"
        result+=note0+str(L2/8)+"["+note1+str(L2/8)+note2+str(L2/8)+"]"
        return result
    # Assign a length that the notes will be getting depending on the number of reps and the length of both the default note and the bar.
    length=int(L2/M2) if reps==1 else int(L2/(2*M2))
    if length==0:
        length='/'
    # This will mean the length will now be at least 2.
    for y in range(reps):
        # Separate activity based on the method.
        if method==0:
            # Go up, then down.
            for x in range(M):
                # When the last note is reached, go back down by negating x and level it. Note that M can be 6 or higher.
                result+=notes[chord[x]+scale[basic[x]]]+str(length) if x<3 and x<6 else notes[chord[M-(x+M%4)]+scale[basic[M-(x+M%4)]]]+str(length)
        if method==1:
            # Go down, then up.
            for x in range(M):
                # This method is much the same, but in reverse order.
                result+=notes[chord[(M-(x+M-2))%3]+scale[basic[M-(x+M-2)]]]+str(length) if x<3 and x<6 else notes[chord[x-2%3]+scale[basic[x-2]]]+str(length)
        if method==2:
            # Go up, stay up. This one places the first few notes, then lets the last linger.
            result+=note0+str(length)+note1+str(length)+note2+str(length*(M-2)) \
            if M>2 else note0+str(length)+note1+str(length)
        if method==3:
            # Go down, stay down.
            # This method is much the same as the second, but staying up.
            # result+=notes[chord[M-(x+M-2)]]+str(length) if x<3 else notes[chord[2]]+str(length)
            # This method is much the same as the previous.
            result+=note0+str(length)+note1+str(length)+note2+str(length*(M-2)) if M>2 else note0+str(length)+note1+str(length)
        if method==4:
            # All at once for half the rep.
            result+="["+note0+str((M/M2)/(L/L2)/(2*reps))+note1+str((M/M2)/(L/L2)/(2*reps))+note2+str((M/M2)/(L/L2)/(2*reps))+"]"+"z"+str((M/M2)/(L/L2)/(2*reps))
        if method==5:
            # Play the first note, then the other two; repeat.
            for x in range(M):
                # This is similar to the edge case.
                result+=note0+str(length) if x%2==1 else "["+note1+str(length)+note2+str(length)+"]"
        if method==6:
            # Play the first note, then the other two over and over.
            for x in range(M):
                result+=note0+str(length) if x==0 else "["+note1+str(length)+note2+str(length)+"]"
        if method==7:
            # Play the first note, then the other two, holding them.
            result+=note0+str(length)+"["+note1+str(length*(M-1))+note2+str(length*(M-1))+"]"
        if method==8:
            for x in range(M):
                # Play the first note, then the top one, then the mid one, then the top one again.
                if x%4==0:
                    result+=note0+str(length)
                elif x%4==2:
                    result+=note1+str(length)
                else:
                    result+=note2+str(length)
        if method==9:
            result+=note0+str(length)
            for x in range(M-1):
                # Play the first note, then the other two, then a rest; repeat the last two steps. This is the reggae/funk arp.
                result+="["+note1+str(length)+note2+str(length)+"]" if x%2==0 else "z"+str(length)
    return result

# The arp writing routine
def arpeggify(chords):
    # Choose the method. Either 8 or 9, the new ones.
    method=r.choice([8,9])
    # The result list.
    result=[]
    # A bar has to be made for every bass bar
    for i in chords:
        # This then gets added.
        result.append(arpeggio(i,method))
    return result
