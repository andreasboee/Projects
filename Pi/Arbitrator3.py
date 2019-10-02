import json

class arbitrator:
    @staticmethod
    def evaluate_data(arr):
        normal_min_values = [19, 23, 1000, 0]
        normal_max_values = [22, 46, 1030, 20]
        inNormalRange = [True, True, True, True]

        if (arr[0] < normal_min_values[0] or arr[0] > normal_max_values[0]):
            inNormalRange[0] = False
        if (arr[1] < normal_min_values[1] or arr[1] > normal_max_values[1]):
            inNormalRange[1] = False
        if (arr[2] < normal_min_values[2] or arr[2] > normal_max_values[2]):
            inNormalRange[2] = False
        if (arr[3] < normal_min_values[3] or arr[3] > normal_max_values[3]):
            inNormalRange[3] = False

        ideal_value = [21,36]
        importance_factor = [6,1]
        importance = [0,0]

        diff1 = (arr[0] - ideal_value[0])
        diff2 = (arr[1] - ideal_value[1])
        if diff1 < 0:
            importance[0] += (-1)*(importance_factor[0])*diff1
        if diff1 > 0:
            importance[0] += (importance_factor[0]*diff1)
        if diff2 < 0:
            importance[1] += (-1) * (importance_factor[1]) * diff2
        if diff2 > 0:
            importance[1] += (importance_factor[1]) * diff2

        if inNormalRange[0] == True && inNormalRange[1] == True:
                #It checks if the sound is too loud first.
                #(prioritized over air pressure)
                if inNormalRange[3] == False:
                    return ('loud')

                if inNormalRange[2] == False:
                    return ('bad airpressure')

                #if none of these apply, it will just return "good"
                return "good"
        else:
            #this is the same as arbitrator2.py
            if importance[0] > importance[1]:
                if diff1 < 0:
                    return ('cold')
                else:
                    return ('hot')
            else:
                if diff2 < 0:
                     return ('dry')
                else:
                    return ('moist')

    @staticmethod
    def choose_action(arr):
        x = []
        j = json.loads(arr)
        x.extend([j['temp:'],j['humidity:'],j['airPressure:'],j['sound:'],])
        return arbitrator.evaluate_data(x)

