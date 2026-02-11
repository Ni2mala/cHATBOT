training_data=[
    ("hi", "greetings"),
    ("hello", "greetings"),
    ("bye", "farewell"),
]

def add_new_intent():
    print(training_data)
    user_intent = input("which intent? ").strip().lower()
    found = False
    for phrase, label in training_data:
        if label == user_intent:
            found = True
            print(phrase)
            new_phrase = input("enter new example ").strip().lower()
    
    if found:
        new_phrase= input("enter new phrase ").strip.lower()
        if new_phrase =="done":
            training_data.append((new_phrase, user_intent))
            print(training_data)

      
    if not found:
           
           print(f"invalid intent", user_intent)
           create = input("create it? (yes/No)")
           if create == "yes":
                
                new_intent=input("enter new intent: ") .strip().lower()
                

    while True:
        new_phrase = input("new example: ").strip().lower()
        if new_phrase =="done":
            break
        if not new_phrase:
            print("can't add empty example")
            continue

        training_data.append((new_phrase, user_intent))
         
        
add_new_intent()
        