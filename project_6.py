# from boltiot import Bolt
# import json

# api_key = "11c628d5-b70b-4cc0-a6c2-5feff9545500"
# device_id = "BOLT14855432"
# mybolt = Bolt(api_key, device_id)
# for _ in range(100):
#     response = json.loads(mybolt.analogRead("A0"))
#     temp = int(response["value"]) / 10.24
#     print(temp)


# base = 10000
# value = base
# tot = 1
# times = 20
# for j in range(2, times + 1):
#     i = 1
#     while value < base * j:
#         profit = value * 0.05
#         # print(f"Week {i}: {round(value,2)} + {round(profit,2)} = {round(value+profit,2)}")
#         value += profit
#         i += 1
#         tot += 1
#     print(f"x{j} in +{i} weeks")
# print(f"x{times} in {tot} weeks")


from boltiot import Bolt

api_key = "Paste_Your_API_Key"
device_id = "BOLTXXXX"
mybolt = Bolt(api_key, device_id)
response = mybolt.isOnline()
print(response)
