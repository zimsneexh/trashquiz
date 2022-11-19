from log import blog

def read_quiz_file():
    qf = open("quiz.lol", "r")

    qfa = qf.read().split("\n")


    qstr = None

    for prop in qfa:
        if(len(prop) == 0):
            continue

        if(prop[0] == '#'):
            continue
    
        prop_arr = prop.split("=")
        key = prop_arr[0]
        
        # answer mode
        if(key == "q"):
            qstr = prop_arr[1] 
        elif(key == "a"):
            if(qstr is None):
                print("error. broken quiz file.")
                exit(-1)
            
            
            res = parse_str_array(prop_arr[1])
            quiz.questions.append(question(qstr, res[0], res[1], res[2]))


def parse_str_array(string):
    vals = [ ]
    buff = ""

    for c in string:
        if(c == ']'):
            vals.append(buff)
            buff = ""
        elif(not c == '['):
            buff = buff + c
    
    return vals



class quiz():

    questions = [ ]

    def __init__(self):
        pass
    
    def add_question(self, qs):
        blog.info("Added question")
        quiz.questions.append(qs)

    def validate_answer(aself, anr, answ):
        if(quiz.questions[anr].answers[0] == answ):
            return True
        else:
            return False

class question():
    # answ1 = correct

    def __init__(self, quest, answ1, answ2, answ3):
        blog.info("Created new question object..")
        self.quest = quest

        self.answers = [ ]
        self.answers.append(answ1)
        self.answers.append(answ2)
        self.answers.append(answ3)


