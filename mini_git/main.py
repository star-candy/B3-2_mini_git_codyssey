# main.py
import shlex
from core import MiniGit

def main():
    repo = MiniGit()
    
    while True:
        try:
            user_input = input("mini-git> ").strip()
            if not user_input:
                continue
                
            # shlex를 이용해 따옴표 안의 공백 유지
            tokens = shlex.split(user_input)
            cmd = tokens[0].upper()

            if cmd in ("EXIT", "QUIT"):
                break
                
            if not repo.is_initialized and cmd != "INIT":
                print("Error: Please run INIT <user_name> first.")
                continue

            if cmd == "INIT":
                if len(tokens) < 2:
                    print("Invalid args. Usage: INIT <user_name>")
                else:
                    repo.init(tokens[1])
                    
            elif cmd == "BRANCH":
                if len(tokens) < 2: print("Invalid args.")
                else: repo.branch(tokens[1])
                    
            elif cmd == "SWITCH":
                if len(tokens) < 2: print("Invalid args.")
                else: repo.switch(tokens[1])
                    
            elif cmd == "COMMIT":
                if len(tokens) < 2: print("Invalid args.")
                else: repo.commit(tokens[1])
                    
            elif cmd == "LOG":
                if len(tokens) > 1 and tokens[1].startswith("--sort-by="):
                    sort_option = tokens[1].split("=")[1].lower()
                    if sort_option in ("date", "author"):
                        repo.log(sort_by=sort_option)
                    else:
                        print("Invalid sort option. Use date or author.")
                else:
                    repo.log()
                    
            elif cmd == "PATH":
                if len(tokens) < 3: print("Invalid args.")
                else: repo.path(tokens[1], tokens[2])
                    
            elif cmd == "ANCESTORS":
                if len(tokens) < 2: print("Invalid args.")
                else: repo.ancestors(tokens[1])
                    
            elif cmd == "SEARCH":
                if len(tokens) < 2: print("Invalid args.")
                else:
                    arg = tokens[1]
                    if arg.startswith("--author="):
                        author = arg.split("=", 1)[1]
                        repo.search(author=author)
                    else:
                        repo.search(keyword=arg)
            else:
                print("Unknown command.")
                
        except ValueError:
            print("Invalid args: Mismatched quotes.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()