import base64
from scapy.all import * 
import binascii

# decode base64
def decodeFun(msg64):  
    base64_message = msg64 +"=="
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return(message)
#decode list of base64
def decodeListFun(list64):
    ans = []
    for i in list64:
        ans.append(decodeFun(i))
    return(ans)

#data from saml file
# data = ""
with open(r"D:\Github\DigitalSquad\gym-maze\maze_pcap.txt", "r") as f:
   data = f.read()

start = time.process_time()
# decode to saml data
foo = base64.b64decode(data) # put your entire string here
print(foo)

#Get the sequance & the main
# with open(r"saml.txt", "r") as f:
#     str = f.read()

str = str(foo)   
sequence = []
main = []

first = ""
second = ""
third = ""
start = -1
x = 0
if (str[0] != '\\'):
  str = '\\' + str

# print (str)
for c in str:
  if (c == '\\'):
    x += 1
  elif (x == 1):
    first += c
  elif (x == 2):
    second += c
  elif (x%2 == 1):
    third += c
  if (c == '\\' and x%2 == 0 and x > 2):
    # print("hello")
    if("google" in third):
      if (first[3:] not in sequence):
        sequence.append(first[3:])
        main.append(second[3:])
      
      first = second
      second = third
      third = ""
      # x += 1
    else:
      # print ("fhasj")
      first = second
      second = third
      third = ""
    x += 1
  # print (first, second, third)
  

print (sequence, main)
# list of strings from saml file 
# li = ['WW9V', 'Z090', 'VGhF', 'c0VjUmVU']

sequence = decodeListFun(sequence)
main = decodeListFun(main)
print(sequence)
print(main)


# sequence.sort()
sorted_indices = sorted(range(len(sequence)), key=lambda k: sequence[k])
main = [main[i] for i in sorted_indices]
sequence = [sequence[i] for i in sorted_indices]
print (main, sequence)
#rearange the list

ans = ''.join(main)
print(ans)
print(time.process_time() - start)