def display_msg(msg):
    print(
        '\033[93m', 
        msg, 
        sep='', 
        end='\033[0m\n'
    )

msg = "hello world - Python"

display_msg(msg)
