from time import sleep
import conf, json, time, math, statistics
from boltiot import Sms, Bolt
import sys, requests


class BoltConf:
    mybolt = Bolt(conf.bolt_api_key, conf.device_id)


class bolted(BoltConf):
    def fetchValue(self, pin):
        response = json.loads(self.mybolt.analogRead(pin))
        if response["success"] != 1:
            func_name = sys._getframe().f_code.co_name
            print(f"{func_name}: Data wasn't received from the BOLT device")
        else:
            return int(response["value"])
        return -99999

    def getTemperature(self):
        "Returns the temperature value in Celcius"
        voltage_output = self.fetchValue("A0")
        temperature = voltage_output / 10.24  # in Celcius
        return temperature

    def getLight(self):
        "Returns the light intensity in the environment given be LDR"
        LDR_out = self.fetchValue("A0")
        return LDR_out

    def outLightWithLDR(self):
        "Returns the light intensity required based on the LDR input"
        LDR_out = self.fetchValue("A0")
        lightIn = 255 - int(LDR_out / (1024 / 255))
        return lightIn


class anamolyDetection(bolted):
    percepts = []
    frame_size = 10
    factor = 3

    def calculate_Z(self):
        history_data = self.percepts
        if len(history_data) < self.frame_size:
            return None
        if len(history_data) > self.frame_size:
            history_data = history_data[-self.frame_size :]
        Mean = statistics.mean(history_data)
        Variance = 0
        for i in history_data:
            Variance += math.pow((i - Mean), 2)
        Zn = self.factor * math.sqrt(Variance / self.frame_size)
        high_bound = history_data[self.frame_size - 1] + Zn
        low_bound = history_data[self.frame_size - 1] - Zn
        return (high_bound, low_bound)

    def sendMessageTele(self, value):
        """Sends message via Telegram"""
        message = f"ALERT DEAR CUSTOMER\nValue[{value}] has been breached the normal range of values"
        url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
        data = {"chat_id": conf.telegram_chat_id, "text": message}
        try:
            response = requests.request("POST", url, params=data)
            telegram_data = json.loads(response.text)
            return telegram_data["ok"]
        except Exception as e:
            print(f"sendMessageTele: {e}")
            return False

    def start(self):
        while 100:
            value = self.getLight()
            Z_response = self.calculate_Z()
            self.percepts.append(value)
            if Z_response == None:
                continue
            upper_bound, lower_bound = Z_response
            print(f"{lower_bound} <= {value} <= {upper_bound}")
            if value >= upper_bound or value < lower_bound:
                print(f"{lower_bound} <= {value} <= {upper_bound}")
                self.sendMessageTele(value)
                self.percepts.pop


obj = anamolyDetection()
obj.start()
