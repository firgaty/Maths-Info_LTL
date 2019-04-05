from statemachine import StateMachine

positive_adjectives = ["magnifique","super", "connu", "joli", "important"]
negative_adjectives = ["futile", "difficile", "stressant", "bad"]

def start_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "Paris7":
        newState = "statu_Paris7"
    else:
        newState = "statu_error"
    return (newState, txt)

def paris7_state_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "est":
        newState = "statu_est"
    else:
        newState = "statu_error"
    return (newState, txt)

def statu_est_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word == "non":
        newState = "statu_non"
    elif word in positive_adjectives:
        newState = "statu_pos"
    elif word in negative_adjectives:
        newState = "statu_neg"
    else:
        newState = "statu_error"
    return (newState, txt)

def statu_non_transitions(txt):
    splitted_txt = txt.split(None,1)
    word, txt = splitted_txt if len(splitted_txt) > 1 else (txt,"")
    if word in positive_adjectives:
        newState = "statu_neg"
    elif word in negative_adjectives:
        newState = "statu_pos"
    else:
        newState = "statu_error"
    return (newState, txt)

def statu_neg(txt):
    print("Hallo")
    return ("statu_neg", "")

if __name__== "__main__":
    m = StateMachine()
    m.add_state("Start", start_transitions)
    m.add_state("statu_Paris7", paris7_state_transitions)
    m.add_state("statu_est", statu_est_transitions)
    m.add_state("statu_non", statu_non_transitions)
    m.add_state("statu_neg", None, end_state=1)
    m.add_state("statu_pos", None, end_state=1)
    m.add_state("statu_error", None, end_state=1)
    m.set_start("Start")
    
    '''
    m.run("Paris7 est super")
    m.run("Paris7 est connu")
    m.run("Paris6 est futile")
    m.run("Paris7 est non magnifique")
    '''
    print('Vous devez entrer une phrase, telle que : ')
    print('Paris7 est super ou Paris7 est non super')
    print('Adjectif positif : magnifique, super, connu, joli, important')
    print('Adjectif négatif : futile, difficile, stressant, bad')


    while(True): 
        val = input('\nVueiller entrer votre phrase : \n')
        m.run(val)
