from __future__ import division
import re, random, math
from pymongo import Connection, errors as PyMongoErrors
connection = Connection()
db = connection["fritbot"]
history = db.history
markov = db.markov

log = history.find()

stats = {}

splitter = re.compile("([,\.!\?-_:;]+( +|$))|(-)|([^,!\?\-_:;\(\)\" ]+)")
punc = re.compile("[,\.!\?-_:;]( +|$)")

END = "__end__"

maximum = 1

state = [""]
cache = {}
output = []
while len(output) < 20:	
	segments = {}
	total = 0.
	for delay in range(min(len(state), maximum)): #len(state)):
		if state[delay] not in cache:
			cursor =  db.markov.find({'from': state[delay]})
			cache[state[delay]] = {}
			data = cache[state[delay]]
			for word in cursor:
				data[word['to']] = word['stats']
		else:		
			data = cache[state[delay]]

		for word in data:
			if delay < 3:
				power = data[word][delay] / math.pow(delay + 1, 2)
			if word not in segments:
				segments[word] = power
			else:
				segments[word] += power
			total += power

	rand = random.randrange(math.floor(total))
	#print state, total, rand
	for seg in segments:
		rand -= segments[seg] 
		#print seg, stat[seg], rand
		if rand <= 0:
			break
	if seg == END:
		if len(output) > 6:
			break
		else:
			state.insert(0, "")
	else:
		output.append(seg)
		state.insert(0, seg)

	print "."

string = ""
for out in output:
	if punc.match(out):
		string += out.rstrip()
	else:
		string += " " + out

print string.lstrip()
