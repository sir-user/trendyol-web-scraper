import os


def console_writer(percent):
    if os.name == "nt":
        os.system("cls")
        print("["+("|"*int(percent/5))+(" "*(20-int(percent/5)))+"]", f"  %{percent}")
    elif os.name == "posix":
        os.system("clear")
        print("["+("|"*int(percent/5))+(" "*(20-int(percent/5)))+"]", f"  %{percent}")
