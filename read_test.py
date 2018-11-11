import json

output = []
# reads all twitter data from a file and loads the json to a arrray
with open("output.json",'r') as f:
	while(True):
		raw = f.readline() # read a line
		if(raw == ''): # exit if we have reached EOF
			break
		output.append(json.loads(raw)) # append loaded json to array
print(output[0])
