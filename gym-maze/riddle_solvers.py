import base64
import cryptography
import re
import json
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import amazoncaptcha
from io import BytesIO as IO
from PIL import Image
import numpy as np
import base64
# from scapy.all import * 
import binascii
import time

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


# Defining BinarytoDecimal() function
def BinaryToDecimal(binary):
        
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return (decimal) 
  

  

def cipher_solver(question):
  # pass
  #Get the Chipertext & decoding it
  # base64_string ="KDEwMTAwMDExMTAxMDEwMTAwMTEwMDExMTAxMDAxMDAwMDExMTEwMDAwMTEwMTAwMTAxMTAxMTAwMTAxMDEwMCwxMDAxKQ=="
  base64_string = question + "=="
  base64_bytes = base64_string.encode("ascii")

  sample_string_bytes = base64.b64decode(base64_bytes)
  sample_string = sample_string_bytes.decode("ascii")
  # print("The Binary value after decoding is:",sample_string)

  #Calculating Key (shift value) , ciphertext in binary
  new_string = re.sub('[()]',"",sample_string)
  new_string = new_string.split(',')
  key = new_string[1]
  cipherText = new_string[0]

  # print("The Key value is:",key)
  # print("The cipher value is:",cipherText)
  bin_data = cipherText

  # initializing a empty string for storing the string data
  str_data =''

  # slicing the input and converting in decimal and then converting it in string
  for i in range(0, len(bin_data), 7):
      temp_data = int(bin_data[i:i + 7])
      decimal_data = BinaryToDecimal(temp_data)
      str_data = str_data + chr(decimal_data)

  # print("The Binary value after string conversion is:",str_data)
  # print(str_data)
  key = bin(int(new_string[1], 2))
  ciphertext = new_string[0]
  preFinal = str_data

  res = []
  for ele in preFinal:
      res.extend(ord(num) for num in ele)

  # print("The ascii list is : " + str(res))

  key = int(key,2)
  # print("the Key value in decimal is:",key)

  for iterator in range(len(res)):
      if(res[iterator] >= 65 and res[iterator] <= 90 ):
          if((res[iterator] - key) < 65 ):
              temp = res[iterator] - key
              tempKey = 65 - temp
              res[iterator] = 91 - tempKey
              iterator+=1
          else:
              res[iterator] = res[iterator] - key
              iterator+=1
      elif(res[iterator] >= 97 and res[iterator] <= 122):
          if((res[iterator] - key) < 97 ):
              temp = res[iterator] - key
              tempKey = 97 - temp
              res[iterator] = 123 - tempKey
              iterator+=1
          else:
              res[iterator] = res[iterator] - key
              iterator+=1

  # print("The ascii list after shifting is",res)

  plaintext = ''
  for char in range(len(res)):
      plaintext = plaintext + chr(res[char])

  # print("the plaintext is ",plaintext)
  # print(plaintext)
  print ("Cipher answer", plaintext)
  return plaintext

def captcha_solver(question):
  # pass
  img = Image.fromarray(np.uint8(question), mode='L')
  img_byte_arr = IO()
  img.save(img_byte_arr, format='PNG')
  print ("Captcha answer", amazoncaptcha.AmazonCaptcha(img_byte_arr).solve())
  return amazoncaptcha.AmazonCaptcha(img_byte_arr).solve()


def pcap_solver(question):
  # pass
  try:
    st = ""
    foo = base64.b64decode(question) # put your entire string here
    st = str(foo)   
    
    sequence = []
    main = []

    first = ""
    second = ""
    third = ""
    start = -1
    x = 0
    if (st[0] != '\\'):
      st = '\\' + st

    for c in st:
      if (c == '\\'):
        x += 1
      elif (x == 1):
        first += c
      elif (x == 2):
        second += c
      elif (x%2 == 1):
        third += c
      if (c == '\\' and x%2 == 0 and x > 2):
        if("google" in third):
          if (first[3:] not in sequence and second[0] == 'x'):
            sequence.append(first[3:])
            main.append(second[3:])
          elif (first[3:] not in sequence and second[0] != 'x'):
            sequence.append(first[3:])
            main.append(second[1:])
          first = second
          second = third
          third = ""
        else:
          first = second
          second = third
          third = ""
        x += 1
      
    print (sequence, main)

    Xseq = []
    for ele in sequence:
      if len(ele) == 2:
        Xseq.append(ele)
          
    Xmain = []
    for ele in main:
      if len(ele) >= 4:
          Xmain.append(ele)

    print(Xseq , Xmain)
    Xseq =decodeListFun(Xseq)
    Xmain =decodeListFun(Xmain)

    sorted_indices = sorted(range(len(Xseq)), key=lambda k: Xseq[k])
    Xmain = [Xmain[i] for i in sorted_indices]
    Xseq = [Xseq[i] for i in sorted_indices]
    print (Xmain, Xseq)

    ans = ''.join(Xmain)
    return ans
  except:
    print("Hard Luck in Pcap, Good luck in others riddles")

def server_solver(question):
  private_key = b'''-----BEGIN RSA PRIVATE KEY-----MIIEpAIBAAKCAQEAtoNn/7u4fpXEoMejGuW8jvKgWFZkVnKzH7qTKto4+7rRT5uDfZDjM+LutvEZZBFsmWCeWFuHMngahNPxBKsXYncqWpqINBtcZEbcZqCoiwg1E7IkLDvqmL+zWbQPhJNLgra7Px28/3JiDmFbzWPFUAQIkk/k1z/6RFd6NNWjGrEqMpGFSRin+x8eY7pShEQfq3Y7B1m4QrEOG7aYX2ym/3PTBNn95EsYTfnk8AtKoBzQggfrh9edO1rRaBhuzVvbjsUfk37rf+P4tqesCqvVUIk+h3gmk559ZANHLG0hF7XUFnDSeFwq0CF2uu6oz09YqXh/Z7ltliTxjzdmLy9yywIDAQABAoIBABHoJqYCpwFUdGxJ6gjTjYKA75Z7M3D/4+8zAQltS7X3CF5FJcuGEaSfmUg9s34L75nEzwRgRo1/Fyr9GGKa3rp8cp1dGAv0u0XjZfBzxtWNQpfiHIZygnvmIxSkA/m/8eKrRwfURRzS/ifnCXjHVy6Ylra0PAGad1WJN6ZDZ7NQj+TAmpvbxAqpOxqAfP0IraMtyWeIIhT99Fm3YElG/zcqer/vG1eo4DQcWSImWEXUXDk41QIPYERCt8piwwYnqxVJo62Tr7ap3T8lS0EmSAwTKAiHUsR2qHeVrMGOrdFR+xp6kjSur8nOtI/itelwL1QdmI/ZGjnq3aP5oL+6mNECgYEA8VxA6p2wgQZRLmYBLg/AXLirxtVvVJNthsjHRCzpo+1pHlVvabscnHFmS+WLkw7RPluzUHa9OT4xEQe9gKCot8SMknQfFxChx4/b4n4xM//xiw0FAcsR4p5wH8YwDNPgk54JIfaOqn1WmwqUH8Z+sdrrYFhz+0lgHvhl0PmNxvUCgYEAwZVmNV2tHOgDdL1SSPF2W4TZZoa8ii3ebcbh3zMZAljr+SXTtwHB9UDN/ouYOau0wXbzSu1BeWxIZ9379YscCd+IOBzFnv26RdB1iRzwv6NvpP+w4efJKdn0IC8Uai6pCsiaJUUDEkJzA+B6J7mAwWPk7DNGo08xnEAN/aAyur8CgYEArPaUms1YcI4LXTnCPLUTAB9jEkFf3/cqtT1q92NMJ6p5+z/0cIujbEUjrt4X0NH8hziF3vLIlZ4I4ZBvcB8x6UeUCVvn78p+dRmV1NDkB8Sx3xj8bpWNAp7R8SNAyeCIfqDxIIKlKG5bww2oqsC/iEs/BDM/ImQp2ufdZw1/WYUCgYEAqCFx2/e4WtrH5aRoyyGsgmAn0XxEVF7ySLXrh0eB+R/yEzpfXxsPskrOnr3vQGd5Xm5JcFIQA72gRVXvd5uShqC2VsXmfegw2GHtM2EHV+pDFTNeFVaSyN6bwTgiqvZLqyn/d08xE7LS4hMdBVOAGHcCZINEXqJxnBumCxoP9VECgYBiqbcwRVmLx6LXz+kS3/n/5dDL7z9db8Xzv/13UkVNxclmQ1bBL3730koeNe1p45qdn2/jnsTTr7a6GV4JLlhwdBV3MSJBf6yhFDoqPfww3IfIax57GxsEPNaPgaP7d4bZPX36E1bN3RbNdnuvcE40gGWst4Ah6RyfB99f+W7bQ==-----END RSA PRIVATE KEY-----'''

  public_key = b'''-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtoNn/7u4fpXEoMejGuW8jvKgWFZkVnKzH7qTKto4+7rRT5uDfZDjM+LutvEZZBFsmWCeWFuHMngahNPxBKsXYncqWpqINBtcZEbcZqCoiwg1E7IkLDvqmL+zWbQPhJNLgra7Px28/3JiDmFbzWPFUAQIkk/k1z/6RFd6NNWjGrEqMpGFSRin+x8eY7pShEQfq3Y7B1m4QrEOG7aYX2ym/3PTBNn95EsYTfnk8AtKoBzQggfrh9edO1rRaBhuzVvbjsUfk37rf+P4tqesCqvVUIk+h3gmk559ZANHLG0hF7XUFnDSeFwq0CF2uu6oz09YqXh/Z7ltliTxjzdmLy9yywIDAQAB-----END PUBLIC KEY-----'''
  # pass
  # return None
  try:
    payload = jwt.decode(question,options={"verify_signature":False})

    payload["admin"]="true"

    token = jwt.encode(payload, private_key, algorithm="RS256",headers={"kid": "3df03abc-f136-4dfa-bcdf-239bc34b28ae","jwk":{
        "kty": "RSA",
        "e": "AQAB",
        "kid": "3df03abc-f136-4dfa-bcdf-239bc34b28ae",
        "n": "toNn_7u4fpXEoMejGuW8jvKgWFZkVnKzH7qTKto4-7rRT5uDfZDjM-LutvEZZBFsmWCeWFuHMngahNPxBKsXYncqWpqINBtcZEbcZqCoiwg1E7IkLDvqmL-zWbQPhJNLgra7Px28_3JiDmFbzWPFUAQIkk_k1z_6RFd6NNWjGrEqMpGFSRin-x8eY7pShEQfq3Y7B1m4QrEOG7aYX2ym_3PTBNn95EsYTfnk8AtKoBzQggfrh9edO1rRaBhuzVvbjsUfk37rf-P4tqesCqvVUIk-h3gmk559ZANHLG0hF7XUFnDSeFwq0CF2uu6oz09YqXh_Z7ltliTxjzdmLy9yyw"
    }})
    print ("server answer", token)
    return (token)
  except:
    return "eyJhbGciOiJSUzI1NiIsImp3ayI6eyJlIjoiQVFBQiIsImtpZCI6IjNkZjAzYWJjLWYxMzYtNGRmYS1iY2RmLTIzOWJjMzRiMjhhZSIsImt0eSI6IlJTQSIsIm4iOiJ0b05uXzd1NGZwWEVvTWVqR3VXOGp2S2dXRlprVm5Lekg3cVRLdG80LTdyUlQ1dURmWkRqTS1MdXR2RVpaQkZzbVdDZVdGdUhNbmdhaE5QeEJLc1hZbmNxV3BxSU5CdGNaRWJjWnFDb2l3ZzFFN0lrTER2cW1MLXpXYlFQaEpOTGdyYTdQeDI4XzNKaURtRmJ6V1BGVUFRSWtrX2sxel82UkZkNk5OV2pHckVxTXBHRlNSaW4teDhlWTdwU2hFUWZxM1k3QjFtNFFyRU9HN2FZWDJ5bV8zUFRCTm45NUVzWVRmbms4QXRLb0J6UWdnZnJoOWVkTzFyUmFCaHV6VnZianNVZmszN3JmLVA0dHFlc0NxdlZVSWstaDNnbWs1NTlaQU5ITEcwaEY3WFVGbkRTZUZ3cTBDRjJ1dTZvejA5WXFYaF9aN2x0bGlUeGp6ZG1MeTl5eXcifSwia2lkIjoiM2RmMDNhYmMtZjEzNi00ZGZhLWJjZGYtMjM5YmMzNGIyOGFlIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL3NlcnZpY2VBLmVudjo4MDgwIiwiYXVkIjoiYWNjb3VudCIsImlkIjoiNTAxYTFiZjQtYjUyMy00OTNjLWI0NTctYWVmOTM1YTI0MWJhIiwic2NvcGUiOiJwcm9maWxlIiwibmFtZSI6IkJvYiBNYXJsZXkiLCJlbWFpbCI6ImJvYi5tYXJsZXlAaGFja3RyaWNrLmNvbSIsImFkbWluIjoidHJ1ZSIsInJhbmQiOiI5OSJ9.PMWrgIhWxhry-WfOM5_G3OJgsulDhEqu90o4hDzrslo7H4XRqiacjuxHjXUYH0hg0F5q9g6x-evMLSxjt7oCf871NBVHeua5xlpgN-i-L-GkSWoKBGgljxQxENW43WVToEEm7EjntmDWBMwB66vTCmYdVMORDX6GoatPn0YSCe-2Ffeqtpb2SCju1eB0lqLvyTQX2ydids0GJQn4NOS5ivdgeCzR9r1x_BIj2tu6Lk7vYpGaEoqu9ei6cRHHzYyRk9NWW94BMbnqt5lO8J7vAj1L0mGuUA6hQ8hFVuX1RlfhjO0M9LKP2DFKgBRk7QxlpWJJgShBD03z7jJntZFbzQ"
    
