'''
* * *
Sheet music generator using ABC notation
* * *
'''
import abcutil
import random as r
K=abcutil.K
M=abcutil.M
M2=abcutil.M2
L=abcutil.L
L2=abcutil.L2
Q=abcutil.Q

# Title
T="111" # Song title
output='X:'+abcutil.X+'\nT:'+T+'\nK:'+K+'\nM:'+str(M)+'/'+str(M2)+'\nQ:'+str(Q)+'\nL:'+str(L)+'/'+str(L2)+'\n'
# A place for all the songs.
songDic={
    "lead":[], # The other lead.
    "lead2":[], # The bass lead.
    "lead3":[], # More variety is better.
    "bass":[],
    "arp":[], # Arpeggios.
    "drum1":[], # Basic drums.
    "drum2":[], # Extra drums.
    "drum3":[], # Not used.
    "voiceCount":[], # Syllables per bar.
    "voice":[], # Words
    "bars":[], # Bar numbers.
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "chordNotes":[] # A list of chord notes represented as notes from the notes list.
}
# The chorus part of the song, which will be appended into the songDic.
chorusDic={
    "lead":[],
    "bass":[],
    "arp":[], # Arpeggios.
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
    "arp":[], # Arpeggios.
    "drum1":[], # Basic drums.
    "drum2":[], # Extra drums.
    "drum3":[], # Not used.
    "voiceCount":[], # Syllables per bar.
    "voice":[], # Words
    "state":[], # A list of states the generator is currently in.
    "chord":[], # A list of chord names being played per bar.
    "chordNotes":[] # A list of chord notes represented as notes from the notes list.
}

'''
Building the song
'''
# First make the chorus
# All the bass notes.
chorus=abcutil.bassify(abcutil.state)
chorusDic["bass"]=chorus["bass"]*2
chorusDic["state"]=chorus["state"]*2
chorusDic["chord"]=chorus["chord"]*2
chorusDic["chordNotes"]=chorus["chordNotes"]*2
# Make the whole lead section from the bass notes.
chorusDic["lead"]=abcutil.leadify(chorusDic["state"],chorusDic["bass"])
drums=abcutil.drumriff()
chorusDic["drum1"]=drums["accent"]
chorusDic["drum2"]=drums["drums"]
drums=abcutil.drumriff()
chorusDic["drum1"]+=drums["accent"]
chorusDic["drum2"]+=drums["drums"]
chorusDic["arp"]=abcutil.arpeggify(chorusDic["chordNotes"])
# The length of the chorus in bars.
chorusLength=len(chorusDic["bass"])
# The vocals.
chorusDic["voiceCount"]=abcutil.vocals(r.choice([chorusDic["bass"],chorusDic["lead"]]))
chorusDic["voice"]=abcutil.lyrics(chorusLength,chorusDic["voiceCount"])

# Do it again for the other.
other=abcutil.bassify(abcutil.state)
otherDic["bass"]=other["bass"]*2
otherDic["state"]=other["state"]*2
otherDic["chord"]=other["chord"]*2
otherDic["chordNotes"]=other["chordNotes"]*2
otherDic["lead"]=abcutil.leadify(otherDic["state"],otherDic["bass"])
drums=abcutil.drumriff()
otherDic["drum1"]=drums["accent"]
otherDic["drum2"]=drums["drums"]
drums=abcutil.drumriff()
otherDic["drum1"]+=drums["accent"]
otherDic["drum2"]+=drums["drums"]
otherDic["arp"]=abcutil.arpeggify(otherDic["chordNotes"])
# The length of the other in bars.
otherLength=len(otherDic["bass"])
# The vocals
otherDic["voiceCount"]=abcutil.vocals(r.choice([otherDic["bass"],otherDic["lead"]]))
otherDic["voice"]=abcutil.lyrics(otherLength,otherDic["voiceCount"])

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
    songDic["drum1"].append("z"+str(int((M/M2)/(L/8)))) if x<otherLength*2/3 else songDic["drum1"].append(otherDic["drum1"][x%2])
    songDic["drum2"].append("z"+str(int((M/M2)/(L/8)))) if x<otherLength*2/3 else songDic["drum2"].append(otherDic["drum2"][x%2])
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
for x in range(abcutil.songLength):
    # A cycle the song consists of is the chorus followed by an other
    for y in range(chorusLength):
        songDic["bass"].append(chorusDic["bass"][y])
        songDic["lead2"].append(chorusDic["lead"][y])
        songDic["drum1"].append(chorusDic["drum1"][y%2])
        # Since there's two of them in a list now, flip between them.
        songDic["drum2"].append(chorusDic["drum2"][y%2])
        songDic["state"].append(chorusDic["state"][y])
        songDic["lead"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["chord"].append(chorusDic["chord"][y])
        songDic["chordNotes"].append(chorusDic["chordNotes"][y])
        songDic["arp"].append(chorusDic["arp"][y])
        songDic["voiceCount"].append(chorusDic["voiceCount"][y])
        songDic["voice"].append(chorusDic["voice"][y])
    totalLength+=chorusLength
    # It's possible at this point to regenerate the otherDic.
    # For instance, new scale.
    scale=abcutil.scaleGen()
    print(scale)
    # And use that to make a new everything.
    other=abcutil.bassify(abcutil.state)
    otherDic["bass"]=other["bass"]*2
    otherDic["state"]=other["state"]*2
    otherDic["chord"]=other["chord"]*2
    otherDic["chordNotes"]=other["chordNotes"]*2
    otherDic["lead"]=abcutil.leadify(otherDic["state"],otherDic["bass"])
    otherLength=len(otherDic["bass"])
    # And some new lyrics to go with that.
    otherDic["voiceCount"]=abcutil.vocals(r.choice([otherDic["bass"], otherDic["lead"]]))
    otherDic["voice"]=abcutil.lyrics(otherLength,otherDic["voiceCount"])
    # And a new drum riff.
    drums=abcutil.drumriff()
    otherDic["drum1"]=drums["accent"]
    otherDic["drum2"]=drums["drums"]
    drums=abcutil.drumriff()
    otherDic["drum1"]+=drums["accent"]
    otherDic["drum2"]+=drums["drums"]
    # So basically a whole new otherDic.
    otherDic["arp"]=abcutil.arpeggify(otherDic["chordNotes"])
    for y in range(otherLength):
        songDic["bass"].append(otherDic["bass"][y])
        songDic["lead"].append(otherDic["lead"][y])
        songDic["drum1"].append(otherDic["drum1"][y%2])
        songDic["drum2"].append(otherDic["drum2"][y%2])
        songDic["state"].append(otherDic["state"][y])
        songDic["lead2"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["chord"].append(otherDic["chord"][y])
        songDic["chordNotes"].append(otherDic["chordNotes"][y])
        songDic["arp"].append(otherDic["arp"][y]) if x%2==0 else songDic["arp"].append(["z"+str(int((M/M2)/(L/L2)))])
        songDic["voiceCount"].append(otherDic["voiceCount"][y])
        songDic["voice"].append(otherDic["voice"][y])
    totalLength+=otherLength

# Add the outro, starting with new lyrics.
otherDic["voice"]=abcutil.lyrics(otherLength,otherDic["voiceCount"])
# Then do the same as the intro.
for x in range(otherLength):
# Fill in the songDic with the gathered information
    songDic["bass"].append(otherDic["bass"][x])
    # Starting with an intro of just the basic other tracks
    songDic["lead"].append(otherDic["lead"][x])
#    songDic["drum1"].append(otherDic["drum1"])
#    songDic["drum2"].append(otherDic["drum2"])
    songDic["drum1"].append("z"+str(int((M/M2)/(L/8))))
    songDic["drum2"].append("z"+str(int((M/M2)/(L/8))))
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
    #print(i,songDic["lead"][i])
    # Write down the bar.
    for j in songDic["lead"][i]:
            output+=j
    output+='|'
output+=']\n\n'

# Second voice, the chorus lead.
output+='V:2\n'
# The full song should be in the songDic.
for i in songDic["bars"]:
    #print(i,songDic["lead2"][i])
    # Write down the bar.
    for j in songDic["lead2"][i]:
            output+=j
    output+='|'
output+=']\n\n'

# Third voice, whatever.
output+='V:3\n'
# Make a copy.
songDic["lead3"]=songDic["lead2"]
for i in songDic["bars"]:
    #print(i)
    # Write down the bar with 1/2 chance of success.
    if r.choice([True,False]):
        output+='z'+str(int((M/M2)/(L/L2)))
    else:
        for j in songDic["lead3"][i]:
            output+=j
    output+='|'
output+=']\n\n'

# Fourth voice (bass).
output+='V:4\n'
# The protocol is much the same as the leads.
for i in songDic["bars"]:
    #print(i,songDic["bass"][i])
    for j in songDic["bass"][i]:
        output+=j
    output+='|'
output+=']\n\n'

# Fifth voice (arp).
output+='V:5\n'
# The protocol is much the same as the leads.
for i in songDic["bars"]:
    #print(i,songDic['arp'][i])
    for j in songDic["arp"][i]:
        output+=j
    output+='|'
output+=']\n\n'
#print(L2)
# Third voice (drums).
output+='L:1/8\n' # It's actually possible to change L, which it should to 1/8.
L2=8
output+='V:6\n'
for i in songDic['bars']:
    #print(i,songDic['drum1'][i])
    # Unlike the other tracks, the drums are stored in a list of strings, rather than a list of lists of strings.
    output+=str(songDic['drum1'][i])+'|'
# Closing statements
output+=']\n\n'

# Fourth voice, the basic drums.
output+='V:7\n'
# Go through the whole song.
for i in songDic['bars']:
    #print(i,songDic['drum2'][i])
    # Unlike the other tracks, the drums are stored in a list of strings, rather than a list of lists of strings.
    output+=songDic['drum2'][i]+'|'
# Closing statements
output+=']\n\n'

# Output is now a genuine, bonafide ABC file, write it to a .abc file and it will work.
fileStream=open(T+'.abc','w')
# Write the entire output into the file.
fileStream.write(output)
# Close it again. I wasn't born in a church.
fileStream.close()
output=str(songDic["voice"])
# Write the lyrics.
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
print(T+' in '+K+' at '+str(Q)+'BPM\nSong length is '+str(int(t))+':'+str(int(t%1*60)))
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
# And finally the third lead going up one octave.
song.parts[2].transpose(transpose[K]+12,True)
# The bass goes down two octaves as well, to make it a bass.
song.parts[3].transpose(transpose[K]-24,True)
# As does the arpeggio one octave
song.parts[4].transpose(transpose[K]-12,True)
# Drums don't get transposed.
# Open the song in Musescore for final touches.
song.show()

# Now everything works.
print()