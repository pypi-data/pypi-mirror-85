import threading
import time
import json
import socket
import os

class IOTClient(threading.Thread):
    """Class used to access IOR Server"""
    __port = 8000

    def __init__(self,code,token,to,time_delay = 90,debug=False,on_close = None,save_logs=False,server = "iorcloud.ml",isTunneled = False):
        """
        :param code: Current Device code
        :param token: Subscription Key
        :param to: Receiver Device Code
        :param time_delay: Time Delay for a Heartbeat @Deprecated
        :param debug: See all the message in I/O stream on the CLI
        :param on_close: a function that has to be called when the connection is closed
        :param save_logs: Save Logs of all the messages
        """
        threading.Thread.__init__(self)
        self.__code = code
        self.__token = token
        self.__to = to
        self.__time_delay = time_delay
        self.debug = debug
        self.__on_close = on_close
        self.__save_logs = save_logs
        self.__lock = threading.Lock()
        self.__isClosed = False
        self.__server = server
        self.isTunneled = isTunneled
        self.connected = False

        self._writeline("*" * 80)
        self._writeline("Using Beta - Version: %s" % self.version())
        self._writeline("Server Configuration IP: %s" % (self.__server))
        self._writeline("User Token %s" % self.__token)
        self._writeline("From Code: %d    To Code: %d" % (self.__code, self.__to))
        self._writeline("Time Delay(in Seconds): %d" % self.__time_delay)
        self._writeline("Tunneling Enabled: " + str(self.isTunneled))
        self._writeline("*" * 80)
        if not os.path.exists('./logs') and save_logs == True:
            os.mkdir('./logs')
        self.reconnect()

    @staticmethod
    def version():
        return "v0.3.7"

    def getSocket(self):
        if self.connected:
            return self.__s

    def reconnect(self):
        try:
            import requests
            r = requests.post('http://%s/IOT/dashboard/socket/subscribe/%s/%d/%d' % (self.__server, self.__token, self.__code,self.__to))
            if r.status_code == 404:
                self._writeline("Request Failed")
                return self.reconnect()
            if r.status_code != 201:
                raise Exception("Invalid Credentials")

            print("Request Successfully made to Server")
            s = r.content
            print(s)

            self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__s.connect((self.__server, self.__port))
            self.__s.sendall(s);
            self.file = self.__s.makefile('rw')
            #self.__s.settimeout(2);
            self._writeline("Connected to Socket Server")

            if not self.isTunneled:
                thread_0 = threading.Thread(target=self.__sendThread)
                thread_0.start()

            self.connected = True
        except Exception:
            self.connected = False
            print("Could not connect to server")

    def __del__(self):
        if not self.__isClosed:
            self.close();

    def __sendThread(self):
        time.sleep(10)
        self.__isClosed = False
        self._writeline("Starting Heartbeat Thread")
        while not self.__isClosed:
            self.sendMessage("<HEARTBEAT>")
            time.sleep(self.__time_delay)

    def set_on_receive(self,fn):
        self.on_receive = fn

    def _writeline(self,msg):
        if self.debug:
            print(msg)

    def __send(self,msg):
        if not self.__isClosed:
            try:
                data = json.dumps(msg)
                self.__lock.acquire()
                self.__s.send(data.encode() + b'\r\n')

                self._writeline("Sending Message:")
                self._writeline(data)
                self.time_start = time.time()*1000
            finally:
                self.__lock.release()


    def sendMessage(self,message,metadata = None):
        if self.__isClosed:
            return None

        msg = dict()
        if message == "<HEARTBEAT>":
            metadata = None

        msg["message"] = message
        if metadata is not None:
            msg["syncData"] = metadata

        self.__send(msg)

    def close(self):
        self.__isClosed = True

        self.__s.close()
        self.file.close()

        self._writeline("Socket Closed")
        if self.__on_close != None:
            self.__on_close()

    def readData(self):
        if self.__isClosed:
            return None
        dataString = self.file.readline()
        print("DataString: ",dataString)
        data = json.loads(dataString)
        self.sendMessage("ack");
        return data

    def run(self):
        self._writeline("Starting Thread")
        while not self.__isClosed:
            try:
                msg = self.readData()
                if msg is not None:
                    self._writeline("Message Received:")
                    self._writeline(msg)
                    try:
                        self.on_receive(msg)
                    except Exception as ex:
                        self._writeline("Error Occured while invoking Receive Function")
                        self._writeline(ex)
            except socket.timeout:
                print("socket timeout")
            except Exception as cae:
                print("Error Occured!!!")
                print(cae)
                break;
            time.sleep(0.01)
        print("Thread Terminated")
        self.close()


