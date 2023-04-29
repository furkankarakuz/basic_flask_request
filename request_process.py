from request_functions import RequestProcess


def help():
    message = '''
    ============================================
    0 -> runs register_request function
    1 -> runs login_request function
    2 -> runs dashboard_request function
    3 -> runs article_detail_request function
    4 -> runs add_article_request function
    5 -> runs delete_article_request function
    6 -> runs update_article_request function
    7 -> runs logout_request function
    q -> quit
    help -> show all commands
    ============================================
    '''
    return (message)


print("Hi !, you can use these codes")
print(help())

check_login = False
process_type = None
while process_type != "q":
    if check_login == False:
        username = input("Your Username : ")
        email = input("Your Mail : ")
        password = input("Your Password : ")

        user = RequestProcess(username, email, password)

    process_type = input("Select Process Type : ")
    
    if process_type == "0":
        user.register_request()

    elif process_type == "1":
        user.login_request()
        if user.result_status_code == 200:
            check_login = True

    elif process_type == "2":
        user.dashboard_request()

    elif process_type == "3":
        article_id = int(input("Article ID : "))
        user.article_detail_request(article_id=article_id)

    elif process_type == "4":
        title = input("Title : ")
        content = input("Content : ")
        user.add_article_request(title=title, content=content)

    elif process_type == "5":
        article_id = int(input("Article ID : "))
        user.delete_article_request(article_id=article_id)

    elif process_type == "6":
        article_id = int(input("Article ID : "))
        title = input("Title : ")
        content = input("Content : ")
        user.update_article_request(
            article_id=article_id, title=title, content=content)
        
    elif process_type == "7":
        user.logout_request()
        if user.result_status_code == 200:
            check_login = False

    if process_type == "help":
        print(help())
