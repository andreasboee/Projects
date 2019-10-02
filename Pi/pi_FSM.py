import stmpy


class pi_fsm:
    def __init__(self, name, component):
        self.name = name
        self.component = component
        self.error_count = 0
        self.error_limit = 3
        self.wait_time = 180000
        self.state = "" #needed to specify the state name so added this variable
        self.data = ""

        t0 = {'source' : 'initial',
              'target' : 'scan'}

        t1 = {'trigger' : 'data_msg',
              'source' : 'scan',
              'function' : self.check_msg}

        t2 = {'trigger' : 'arbitrator',
              'source' : 'choose_state',
              'function': self.get_state}

        t3 = {'trigger' : 't',
              'source' : "good",
              'target' : 'scan'}

        t4 = {'trigger' : 't',
              'source' : 'cold',
              'target' : 'scan'}

        t5 = {'trigger': 't',
              'source': 'hot',
              'target': 'scan'}

        t6 = {'trigger' : 't',
              'source' : 'dry',
              'target' : 'scan'}

        t7 = {'trigger': 't',
              'source': 'moist',
              'target': 'scan'}

        t8 = {'trigger': 'update',
              'source': "good",
              'target': 'scan'}

        t9 = {'trigger': 'update',
              'source': 'cold',
              'target': 'scan'}

        t10 = {'trigger': 'update',
              'source': 'hot',
              'target': 'scan'}

        t11 = {'trigger': 'update',
              'source': 'dry',
              'target': 'scan'}

        t12 = {'trigger': 'update',
              'source': 'moist',
              'target': 'scan'}

        t13 = {'trigger' : 'update',
              'source' : 'error_check',
              'function':  self.check_error_limit}
        
        # the states:
        scan = {'name': 'scan',
                'entry': 'get_sensor_values'}

        choose_state = {'name': 'choose_state',
                        'entry': 'init_choose_state',
                        'exit': 'exit_choose_state'}

        good = {'name': 'good',
                'entry': 'good'}

        #bad = {'name': 'bad',
        #       'entry': 'bad'}
        cold = {'name': 'cold',
                'entry': 'cold'}

        hot = {'name': 'hot',
                'entry': 'warm'}

        dry = {'name': 'dry',
               'entry': 'dry'}

        moist = {'name': 'moist',
                 'entry': 'moist'}

        error = {'name': 'error_check',
                 'entry': 'error_iterate'}

        end_state = {'name': 'end_state',
                     'entry': 'terminate'}

        self.stm = stmpy.Machine(name=name, transitions=[t0, t1, t2, t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13],
                                 obj=self, states=[scan, choose_state, good, cold, hot, dry, moist, error, end_state])

    def get_sensor_values(self):
        print("requesting sensor values from controller...")
        self.component.requesting_sensor_values()

    def init_choose_state(self):
        print("now in init_choose_state")
        self.component.arbitrator_evaluation(self.data)           # Don't know about this one seems to be a bit much back and forth


    def exit_choose_state(self):
        self.component.publish_state(self.data, self.state)
        self.data = ""      # resets data

        print("leaving choose state, start 3 minute timer")
        self.stm.start_timer("t", self.wait_time)

    def good(self):
        self.state = "good"
        print("in good state, set light green")

    #def bad(self):
    #    print("in bad state, set light red")
    def cold(self):
        self.state = "cold"
        print("in cold state, set light red")

    def warm(self):
        self.state = "warm"
        print("in warm state, set light red")

    def dry(self):
        self.state = "dry"
        print("in dry state, set light red")

    def moist(self):
        self.state = "moist"
        print("in moist state, set light red")

    def set_data(self, data_json):
        self.data = data_json

    def set_state(self, state_string):
        self.state = state_string

    def get_state(self):
        return self.state

    def check_msg(self):
        if self.data == "":
            return "error_check"
        else:
            return "choose_state"

    def error_iterate(self):
        self.stm.start_timer("t", self.wait_time)
        self.error_count += 1
        print("Data error")

    def check_error_limit(self):
        if self.error_count >= self.error_limit:
            return "end_state"
        else:
            return "scan"

    def terminate(self):
        self.component.terminate()
        self.stm.terminate()

