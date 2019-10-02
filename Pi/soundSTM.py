import stmpy

class pi_fsm:
    def __init__(self, name, component):
        self.name = name
        self.component = component
        self.recording_interval = 1000

        t0 = {'source' : 'initial',
              'target' : 'idle'}

        t1 = {'trigger' : 'update',
              'source' : 'idle',
              'target' : 'Send_data'}

        t2 = {'trigger' : 't',
              'source' : "Send_data",
              'target' : 'idle'}

        # the states:
        idle = {'name': 'idle'}

        Send_Data = {'name': 'Send_data',
                        'entry': 'init_send_data',
                        'exit': 'publish_send_data'}

        self.stm = stmpy.Machine(name=name, transitions=[t0, t1, t2],
                                 obj=self, states=[idle,Send_Data])

    def publish_send_data(self):
        print("publishing sensor values...")
        #self.component.stop_recording
        self.component.publish_sound_values()

    def init_Send_Data(self):
        print("Starting to record...")
        #self.component.start_recording

        self.stm.start_timer("t", self.recording_interval)




