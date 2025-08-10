import random
import json
import os

# Colors for terminal
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
YELLOW = "\033[93m"

# Files
history_file = "asked_questions.json"
score_file = "user_name_scores.json"

# Question bank (100 questions)
question_bank = [
    # --- First 50 ---
    {"question": "Who developed Python?", "options": ["a) Dennis Ritchie", "b) Guido van Rossum", "c) James Gosling"], "answer": "b"},
    {"question": "Which year was Python first released?", "options": ["a) 1991", "b) 1989", "c) 2000"], "answer": "a"},
    {"question": "Keyword to define a function?", "options": ["a) func", "b) def", "c) function"], "answer": "b"},
    {"question": "Output of print(type([]))?", "options": ["a) <class 'list'>", "b) <class 'tuple'>", "c) <class 'dict'>"], "answer": "a"},
    {"question": "Which is a tuple?", "options": ["a) [1, 2, 3]", "b) (1, 2, 3)", "c) {1, 2, 3}"], "answer": "b"},
    {"question": "Module for random numbers?", "options": ["a) math", "b) random", "c) statistics"], "answer": "b"},
    {"question": "File extension for Python?", "options": ["a) .py", "b) .python", "c) .pt"], "answer": "a"},
    {"question": "Immutable data type?", "options": ["a) List", "b) Set", "c) String"], "answer": "c"},
    {"question": "Insert comment in Python?", "options": ["a) //", "b) /* */", "c) #"], "answer": "c"},
    {"question": "Output of print(2 ** 3)?", "options": ["a) 6", "b) 8", "c) 9"], "answer": "b"},
    {"question": "Output of print(10//3)?", "options": ["a) 3", "b) 3.3", "c) 4"], "answer": "a"},
    {"question": "Which function to read input?", "options": ["a) input()", "b) scan()", "c) get()"], "answer": "a"},
    {"question": "Which keyword for loop?", "options": ["a) for", "b) loop", "c) iterate"], "answer": "a"},
    {"question": "Output of bool(0)?", "options": ["a) True", "b) False", "c) None"], "answer": "b"},
    {"question": "Which data type is []?", "options": ["a) list", "b) dict", "c) tuple"], "answer": "a"},
    {"question": "What does len('Python') return?", "options": ["a) 5", "b) 6", "c) 7"], "answer": "b"},
    {"question": "Which method adds an item to a list?", "options": ["a) add()", "b) append()", "c) insert()"], "answer": "b"},
    {"question": "Output of print(5 % 2)?", "options": ["a) 1", "b) 2", "c) 0"], "answer": "a"},
    {"question": "Which is NOT a Python data type?", "options": ["a) list", "b) set", "c) arraylist"], "answer": "c"},
    {"question": "Which keyword is used for exceptions?", "options": ["a) try", "b) catch", "c) except"], "answer": "c"},
    {"question": "Output of print('a' * 3)?", "options": ["a) aaa", "b) 3a", "c) error"], "answer": "a"},
    {"question": "Which function gives absolute value?", "options": ["a) abs()", "b) fabs()", "c) absolute()"], "answer": "a"},
    {"question": "Which operator is for exponent?", "options": ["a) ^", "b) **", "c) ^^"], "answer": "b"},
    {"question": "What is Python?", "options": ["a) Programming language", "b) Snake", "c) Both"], "answer": "c"},
    {"question": "Which library for data analysis?", "options": ["a) pandas", "b) numpy", "c) flask"], "answer": "a"},
    {"question": "Output of print(3 == 3.0)?", "options": ["a) True", "b) False", "c) Error"], "answer": "a"},
    {"question": "Which is mutable?", "options": ["a) tuple", "b) list", "c) string"], "answer": "b"},
    {"question": "How to create a set?", "options": ["a) {}", "b) set()", "c) both"], "answer": "c"},
    {"question": "Output of print(10 != 5)?", "options": ["a) True", "b) False", "c) Error"], "answer": "a"},
    {"question": "Which library for web framework?", "options": ["a) django", "b) matplotlib", "c) numpy"], "answer": "a"},
    {"question": "Which is a Python boolean?", "options": ["a) TRUE", "b) True", "c) true"], "answer": "b"},
    {"question": "Which keyword for class?", "options": ["a) class", "b) define", "c) object"], "answer": "a"},
    {"question": "Which is used for string formatting?", "options": ["a) %", "b) format()", "c) f-string"], "answer": "c"},
    {"question": "Output of print(min([2,5,1]))?", "options": ["a) 5", "b) 2", "c) 1"], "answer": "c"},
    {"question": "Which method removes last list item?", "options": ["a) remove()", "b) pop()", "c) delete()"], "answer": "b"},
    {"question": "Which data type is {'a':1}?", "options": ["a) list", "b) dict", "c) set"], "answer": "b"},
    {"question": "Output of print(4 // 2)?", "options": ["a) 2", "b) 2.0", "c) 2.00"], "answer": "a"},
    {"question": "Which operator is for 'or'?", "options": ["a) ||", "b) or", "c) |"], "answer": "b"},
    {"question": "Which is a Python IDE?", "options": ["a) PyCharm", "b) Eclipse", "c) NetBeans"], "answer": "a"},
    {"question": "Which function to get type?", "options": ["a) typeof()", "b) type()", "c) gettype()"], "answer": "b"},
    {"question": "Output of print(7 % 3)?", "options": ["a) 1", "b) 2", "c) 3"], "answer": "b"},
    {"question": "Which keyword to stop loop?", "options": ["a) exit", "b) stop", "c) break"], "answer": "c"},
    {"question": "Which is a comment?", "options": ["a) #comment", "b) //comment", "c) /*comment*/"], "answer": "a"},
    {"question": "Which is a list method?", "options": ["a) extend()", "b) enlarge()", "c) expand()"], "answer": "a"},
    {"question": "Which is not a keyword?", "options": ["a) pass", "b) eval", "c) while"], "answer": "b"},
    {"question": "Output of print(len([1,2,3]))?", "options": ["a) 2", "b) 3", "c) 4"], "answer": "b"},
    {"question": "Which library is for plotting?", "options": ["a) matplotlib", "b) flask", "c) pandas"], "answer": "a"},
    {"question": "Which is a tuple method?", "options": ["a) count()", "b) append()", "c) pop()"], "answer": "a"},
    {"question": "Output of print(2 in [1,2,3])?", "options": ["a) True", "b) False", "c) Error"], "answer": "a"},
    {"question": "Which keyword defines a function?", "options": ["a) func", "b) def", "c) define"], "answer": "b"},

    # --- Second 50 (Advanced + Basics) ---
    {"question": "Which keyword is used to create an anonymous function?", "options": ["a) lambda", "b) anon", "c) def"], "answer": "a"},
    {"question": "Which function is used to get user input in Python 3?", "options": ["a) get()", "b) scan()", "c) input()"], "answer": "c"},
    {"question": "What does PEP stand for?", "options": ["a) Python Execution Plan", "b) Python Enhancement Proposal", "c) Python Extra Package"], "answer": "b"},
    {"question": "Which symbol is used for list slicing?", "options": ["a) :", "b) ;", "c) |"], "answer": "a"},
    {"question": "Which built-in function returns the length of an object?", "options": ["a) count()", "b) length()", "c) len()"], "answer": "c"},
    {"question": "Which data type is created using {} but without key-value pairs?", "options": ["a) list", "b) set", "c) tuple"], "answer": "b"},
    {"question": "Which function converts a string to lowercase?", "options": ["a) lower()", "b) toLower()", "c) downcase()"], "answer": "a"},
    {"question": "Which statement is used to exit a loop?", "options": ["a) break", "b) stop", "c) exit"], "answer": "a"},
    {"question": "Which method returns a list of dictionary keys?", "options": ["a) keys()", "b) getkeys()", "c) keylist()"], "answer": "a"},
    {"question": "Which function returns the largest number?", "options": ["a) large()", "b) max()", "c) biggest()"], "answer": "b"},
    {"question": "Which operator checks for equality?", "options": ["a) =", "b) ==", "c) equals"], "answer": "b"},
    {"question": "Which function is used to round numbers?", "options": ["a) round()", "b) approx()", "c) around()"], "answer": "a"},
    {"question": "Which method removes all items from a list?", "options": ["a) clear()", "b) delete()", "c) removeAll()"], "answer": "a"},
    {"question": "Which operator is used for integer division?", "options": ["a) /", "b) //", "c) %"], "answer": "b"},
    {"question": "Which keyword is used to create a generator?", "options": ["a) yield", "b) return", "c) generate"], "answer": "a"},
    {"question": "Which function can convert a list to a tuple?", "options": ["a) tuple()", "b) toTuple()", "c) listToTuple()"], "answer": "a"},
    {"question": "Which method finds the position of a substring?", "options": ["a) find()", "b) indexOf()", "c) search()"], "answer": "a"},
    {"question": "Which function is used to get the ASCII value of a character?", "options": ["a) ord()", "b) chr()", "c) ascii()"], "answer": "a"},
    {"question": "Which function returns the character for an ASCII value?", "options": ["a) ord()", "b) chr()", "c) ascii()"], "answer": "b"},
    {"question": "Which module is used for working with dates?", "options": ["a) datetime", "b) time", "c) calendar"], "answer": "a"},
    {"question": "Which symbol is used for comments in Python?", "options": ["a) //", "b) #", "c) --"], "answer": "b"},
    {"question": "Which keyword is used to define a module?", "options": ["a) module", "b) def", "c) import"], "answer": "c"},
    {"question": "Which function is used to open files?", "options": ["a) file()", "b) open()", "c) fopen()"], "answer": "b"},
    {"question": "Which mode is used to write to a file in Python?", "options": ["a) w", "b) r", "c) a"], "answer": "a"},
    {"question": "Which mode is used to append to a file?", "options": ["a) w", "b) a", "c) r+"], "answer": "b"},
    {"question": "Which function is used to sort a list?", "options": ["a) sort()", "b) order()", "c) arrange()"], "answer": "a"},
    {"question": "Which function returns the type of a variable?", "options": ["a) typeof()", "b) type()", "c) vartype()"], "answer": "b"},
    {"question": "Which keyword creates an infinite loop?", "options": ["a) forever", "b) while True", "c) loop"], "answer": "b"},
    {"question": "Which exception is raised when dividing by zero?", "options": ["a) DivideByZeroError", "b) ZeroDivisionError", "c) MathError"], "answer": "b"},
    {"question": "Which function generates a sequence of numbers?", "options": ["a) range()", "b) seq()", "c) generate()"], "answer": "a"},
    {"question": "Which method joins list elements into a string?", "options": ["a) join()", "b) concat()", "c) combine()"], "answer": "a"},
    {"question": "Which method removes whitespace from the start and end of a string?", "options": ["a) strip()", "b) trim()", "c) clean()"], "answer": "a"},
    {"question": "Which keyword is used to handle exceptions?", "options": ["a) try-except", "b) catch", "c) handle"], "answer": "a"},
    {"question": "Which symbol is used for multiplication?", "options": ["a) x", "b) *", "c) mul"], "answer": "b"},
    {"question": "Which data type is returned by range() in Python 3?", "options": ["a) list", "b) range", "c) tuple"], "answer": "b"},
    {"question": "Which method returns the number of occurrences of a value in a list?", "options": ["a) count()", "b) occurrences()", "c) times()"], "answer": "a"},
    {"question": "Which keyword is used to create a subclass?", "options": ["a) subclass", "b) inherit", "c) class"], "answer": "c"},
    {"question": "Which method adds multiple items to a list?", "options": ["a) append()", "b) extend()", "c) addMany()"], "answer": "b"},
    {"question": "Which function converts a number to a string?", "options": ["a) str()", "b) tostring()", "c) convert()"], "answer": "a"},
    {"question": "Which function converts a string to an integer?", "options": ["a) str()", "b) int()", "c) parseInt()"], "answer": "b"},
    {"question": "Which function returns the sum of elements in a list?", "options": ["a) total()", "b) sum()", "c) addAll()"], "answer": "b"},
    {"question": "Which keyword is used to return from a function?", "options": ["a) stop", "b) return", "c) exit"], "answer": "b"},
    {"question": "Which statement is used for debugging?", "options": ["a) debug", "b) assert", "c) check"], "answer": "b"},
    {"question": "Which method converts a list into a set?", "options": ["a) set()", "b) toSet()", "c) listToSet()"], "answer": "a"},
    {"question": "Which function is used to find the minimum value?", "options": ["a) least()", "b) min()", "c) minimum()"], "answer": "b"},
    {"question": "Which function is used to find the power of a number?", "options": ["a) pow()", "b) power()", "c) **"], "answer": "a"},
    {"question": "Which module is used for regular expressions?", "options": ["a) regex", "b) re", "c) regexp"], "answer": "b"},
    {"question": "Which operator is used for logical AND?", "options": ["a) &&", "b) and", "c) &"], "answer": "b"},
    {"question": "Which operator is used for logical NOT?", "options": ["a) !", "b) not", "c) ~"], "answer": "b"}
]

# Load scores
if os.path.exists(score_file):
    with open(score_file, "r") as f:
        user_scores = json.load(f)
else:
    user_scores = {}

# Load history
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        history_data = json.load(f)
else:
    history_data = {}

# Ask username
username = input("Enter your name (type 'delete' to remove a player): ").strip()

# Delete player feature
if username.lower() == "delete":
    name_to_delete = input("Enter username to delete (or type 'all' to delete all): ").strip()
    deleted = False

    if name_to_delete.lower() == "all":
        user_scores.clear()
        history_data.clear()
        with open(score_file, "w") as f:
            json.dump(user_scores, f)
        with open(history_file, "w") as f:
            json.dump(history_data, f)
        print(f"{GREEN}✅ All usernames and records deleted successfully!{RESET}")
        exit()

    if name_to_delete in user_scores:
        del user_scores[name_to_delete]
        deleted = True
    if name_to_delete in history_data:
        del history_data[name_to_delete]
        deleted = True

    with open(score_file, "w") as f:
        json.dump(user_scores, f)
    with open(history_file, "w") as f:
        json.dump(history_data, f)

    if deleted:
        print(f"{GREEN}✅ Deleted {name_to_delete} from records.{RESET}")
    else:
        print(f"{RED}❌ Username '{name_to_delete}' not found.{RESET}")
    exit()

# Game loop
while True:
    asked_indexes = history_data.get(username, [])
    remaining_indexes = [i for i in range(len(question_bank)) if i not in asked_indexes]

    if len(remaining_indexes) < 10:
        asked_indexes = []
        remaining_indexes = list(range(len(question_bank)))
        print(f"{YELLOW}\n🔄 All questions completed for you, starting again!\n{RESET}")

    selected_indexes = random.sample(remaining_indexes, 10)

    score = 0
    for idx, i in enumerate(selected_indexes, start=1):
        q = question_bank[i]
        print(f"\n{YELLOW}Q{idx}/10:{RESET} {CYAN}{q['question']}{RESET}")

        for opt in q["options"]:
            print(opt)

        # Input validation
        ans = input("Enter your answer (a/b/c): ").lower()
        while ans not in ["a", "b", "c"]:
            ans = input("Invalid input! Please enter only a, b, or c: ").lower()

        if ans == q["answer"]:
            print(f"{GREEN}✅ Correct!{RESET}\n")
            score += 1
        else:
            print(f"{RED}❌ Wrong! Correct answer: {q['answer']}{RESET}\n")

    asked_indexes.extend(selected_indexes)
    history_data[username] = asked_indexes
    with open(history_file, "w") as f:
        json.dump(history_data, f)

    if username not in user_scores:
        user_scores[username] = []
    user_scores[username].append(score)
    with open(score_file, "w") as f:
        json.dump(user_scores, f)

    print(f"{YELLOW}Your final score: {score}/10{RESET}")
    percentage = (score / 10) * 100
    print(f"{YELLOW}Your percentage: {percentage}%{RESET}")

    # Leaderboard
    print(f"\n🏆 {YELLOW}Top 5 Leaderboard:{RESET}")
    avg_scores = {user: sum(scores) / len(scores) for user, scores in user_scores.items()}
    ranking = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    for rank, (user, avg) in enumerate(ranking, 1):
        print(f"{rank}. {user} - Avg Score: {avg:.2f}/10 (Games Played: {len(user_scores[user])})")

    choice = input("\nDo you want to play again? (y/n): ").lower()
    if choice != "y":
        print(f"{CYAN}Thanks for playing, {username}! 👋{RESET}")
        break
