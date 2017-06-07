output='X:1\nT:Test\nK:C\nM:4/4\nQ:120\nL:1/4\n\nV:1\n'
output+='[aA,B][a]'
output+='|]'
print(output)
import music21 as mu
song=mu.converter.parse(output)
song.show()
