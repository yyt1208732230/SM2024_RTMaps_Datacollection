import rtmaps.types
from rtmaps.base_component import BaseComponent  # base class

from biopacndt import *
# from biopacndt import 

# Python class that will be called from RTMaps.
class rtmaps_python(BaseComponent):
    
    # If you change something in the __init__ function, you will need to use the "Update Inputs, Outputs and Properties"
    # action on the Python component (via RTMaps) for your changes to be taken into account.
    def __init__(self):
        BaseComponent.__init__(self)  # call base class constructor
        self._acqServer = None
        self._acqServerData = None
        self._host = None
        self._port = None
        self._found_server = False

    def Dynamic(self):
# Define the output. The type is set to AUTO which means that the output will be typed automatically.
# You don’t need to set the buffer_size, in that case it will be set automatically. 

        serverList = FindAcqNdtServers()

        enumServer = f'{len(serverList)}|-1'
        for host, port in serverList:
            enumServer += f'|{host} - {port}'

        self.add_property("Servers", enumServer, rtmaps.types.ENUM)
        if self.properties["Servers"].get_selected() >= 0:
            self._found_server = True
            server = self.properties['Servers'].get_selected_value()
        
            host, port = server.split(' - ')
            if self._host is not host or self._port is not port:
                if self._acqServer is not None:
                    self._acqServer = None
                self._acqServer = AcqNdtServer(host, port)
                self._host = host
                self._port = port

            channels = self._acqServer.GetAllChannels()
            for channel in channels:
                label = self._acqServer.GetChannelLabel(channel).replace(" ", "")
                outputName = label.replace("-","_") 
                self.add_output(outputName, rtmaps.types.AUTO)
        else:
            self._found_server = False
            print("Server not found or need to select a good server.")

    def write_frame_to_rtmaps_output(self, hardwareIndex, frame, chanInfo):
        print(f'Hardware Idx : {hardwareIndex}')
        print(f'Frame : {frame}')
        print(f'chanInfo : {chanInfo}')
        for i in range(0, len(chanInfo)):
            label = self._acqServer.GetChannelLabel(chanInfo[i]).replace(" ", "")
            outputName = label.replace("-", "_")
            self.outputs[outputName].write(frame[i])
   
# Birth() will be called once at diagram execution startup
    def Birth(self):
        if self._found_server == True:
            self._acqServerData = AcqNdtDataServer(self._acqServer.getSingleConnectionModePort(), 
                                                self._acqServer.GetAllChannels())
            self._acqServerData.RegisterCallback('write_frame_to_rtmaps', self.write_frame_to_rtmaps_output)
            self._acqServer.DeliverAllEnabledChannels()
            if not self._acqServer.getAcquisitionInProgress():
                self._acqServer.toggleAcquisition()
            self._acqServerData.Start()
        else:
            print("Before running, you need to choose the Acqknowledge Server. The component will die.")
            self.commit_suicide()
# Core() is called every time you have a new input
    def Core(self):
        pass

# Death() will be called once at diagram execution shutdown
    def Death(self):
        if self._found_server == True:
            self._acqServerData.Stop()
            if self._acqServer.getAcquisitionInProgress():
                self._acqServer.toggleAcquisition()
