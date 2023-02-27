from controller import Controller, stdin_int
from sys import exit
from colorama import init, Fore, Back, Style
from mysql.connector.errors import DatabaseError


init(convert=True)


def start_controller(con:Controller) -> None:
    # Attempt to connect to database, exit if no connection
    if not con.is_connected():
        con.connect()


# Refresh Configs
def refresh_configs(con: Controller) -> None:
    con.refresh_configs()
    print_available_creds(con)



# print the API objects avilable to us.
def print_available_creds(con: Controller) -> None:
    apis = con.get_api_list()
    # Print nunmber of configs.
    print("\n--------- CREDS AVAILABLE -----------\n")
    print(f"TOTAL: {len(apis)} \n")
    for api in apis:
        print(f"{api.get_number()}")
    print("\n-------------------------------------")

# Visualize our existing database's follower interactions.
def visualize(con: Controller):
    print("\n----------- GRAPH -------------\n")
    num = stdin_int("Account Sample Size")
    con.visualize_followers(num)
    print("\n-------------------------------------")


# Deploy workers
def deploy(con: Controller) -> None:
    con.deploy()



def menu_no_workers() -> None:
    print("""
[1] Connect to database
[2] View Credential List
[3] Reload API Configs
\033[1;30m[4] Deploy\033[0m
[5] Visualize Data
[6] Exit
""")



def menu_has_workers():
    print("""
[1] Connect to database
[2] View Credential List
[3] Reload API Configs
[4] Deploy
[5] Visualize Data
[6] Exit
""")



def main():
    print("\n\tWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n------------- CONNECTION ------------\n")
     # Try to create controller and connect to database instance.
    # Initialize the controller and db connections
    con = Controller()
    valid = False
    try:
        if con.is_connected() and len(con.get_api_list()) > 0:
            valid = True
        else:
            valid = False
    except DatabaseError as error:
        print("\n\033[91mERROR: Could not connect to database instance.\033[0m\n\t└", error.msg)
        valid = False


    while True:
        if valid:
            menu_has_workers()
        else: 
            menu_no_workers()


        choice = input("\033[0;36m>> \033[0m").strip()


        match choice:
            case '1': 
                start_controller(con)
            case '2':
                print_available_creds(con)
            case '3':
                refresh_configs(con)
            case '4':
                if not con.is_connected(): 
                    print("\n\033[91mERROR: No Database Connection.\033[0m \n")
                elif len(con.get_api_list()) == 0:
                    print("\n\033[91mERROR: No valid credentials.\033[0m \n")
                else:
                    deploy(con)
            case '5':
                visualize(con)
            case '6':
                break
            case _:
                print("\n\033[91mInvalid Selection.\033[0m \n")


if __name__ == "__main__":
    main()
    print("\nSee You Later (⌐ ͡■ ͜ʖ ͡■) \n\n--------- EXIT ---------\n")