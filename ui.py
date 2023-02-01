from controller import Controller
from sys import exit
from colorama import init, Fore, Back, Style
from mysql.connector.errors import DatabaseError


init(convert=True)


def start_controller(con):
    # Attempt to connect to database, exit if no connection
    if not con.is_connected():
        con.connect()


# Create nodes
def create_nodes(con: Controller):
    print("\n----------- CREDENTIAL'[]; CREATION ------------\n")
    # Try to create nodes
    con.create_nodes()
    print("--------------------------------------")



# Refresh Configs
def refresh_configs(con: Controller):
    print("\n---------- CONFIG REFRESH -----------\n")
    # Try to refresh configs
    con.refresh_configs()
    print("  Configs:  ||\t", len(con.get_configs()))
    print("\n-------------------------------------")



# print number of nodes and config files used
def print_node_number(con: Controller):
    # Print nunmber of configs
    print("\n--------- CONFIG-NODE NO. -----------\n")
    print("  Configs:  ||\t", len(con.get_configs()))
    # Print number of nodes:
    print("  Nodes:    ||\t", len(con.get_nodes()))
    print("\n-------------------------------------")



# Deploy nodes
def deploy_nodes(con):
    con.deploy_nodes()



def menu_no_nodes():
    print("""
[1] Connect to database
[2] Create Nodes
[3] See Node Authentication Numbers
[4] Reload Node Configs
\033[1;30m[5] Deploy Nodes\033[0m
[6] Exit
""")



def menu_has_nodes():
    print("""
[1] Connect to database
[2] Create Nodes
[3] See Node Authentication Numbers
[4] Reload Node Configs
[5] Deploy Nodes
[6] Exit
""")



def main():
    print("\nWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n------------- CONNECTION ------------\n")
    print("\n-------------------------------------")

    while True:
        # Try to create controller and connect to database instance.
        # Initialize the controller and db connections
        con = Controller()
        try:
            if con.is_connected() and len(con.get_api_list()) > 0:
                menu_has_nodes()
            else:
                menu_no_nodes()
        except DatabaseError as error:
            print("\nERROR: Could not connect to database instance.\n\t└", error.msg)
            menu_no_nodes()


        choice = input("\033[0;36m>> \033[0m").strip()
        
        match choice:
            case '1': 
                start_controller(con)
            case '2':
                create_nodes(con)
            case '3':
                print_node_number(con)
            case '4':
                refresh_configs(con)
            case '5':
                if not con.is_connected(): 
                    print("\n\033[91mERROR: No Database Connection.\033[0m \n")
                elif len(con.get_nodes()) == 0:
                    print("\n\033[91mERROR: No Nodes to deploy.\033[0m \n")
                else:
                    deploy_nodes(con)
            case '6':
                break
            case _:
                print("\n\033[91mInavlid Selection.\033[0m \n")


if __name__ == "__main__":
    main()
    print("\nSee You Later (⌐ ͡■ ͜ʖ ͡■) \n\n--------- EXIT ---------\n")