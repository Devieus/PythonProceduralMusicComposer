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
import music21 as mu

mu.converter.parse(song).show()"""
