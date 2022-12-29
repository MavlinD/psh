from rich import print as rprint
from rich.console import Console
import sh
# from sh import ifconfig
# from sh import curl


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # sh.ls("-l", "/tmp", color="never")
    # uu = sh.ls("-al")
    uu = sh.bash("-c", "docker ps --format 'table {{.Names}}+{{.Status}}+{{.Networks}}+{{.Ports}}'")
    print(dir(uu))
    print()
    print(len(uu))
    # iter_length = len(list(uu))
    # print(iter_length)
    uul = list(uu)
    amount_rows = len(uul)
    for key, val in enumerate(uul):
        print(type(val))
        ii = val.strip('  ')
        # ii = val.splitlines(amount_rows)
        # ii = val.splitlines(' ')
        rprint(ii)
        rprint(len(ii[0]))
        rprint(val, end="")
        if key == 0:
            print('='*50)
        else:
            print('-'*50)
    # rprint(uu)
    # nums_list = [1, 2, 3, 4]
    # rprint(nums_list)
    # console = Console()
    # with console.capture() as capture:
    #     console.print("[bold magenta]Hello World[/]")
    # print(capture.get())

    # from sh import tail, curl
    # tt = curl("http://duckduckgo.com/", "-o", "page.html", "--silent")
    # print(tt)

    # for line in tail("-f", "/var/log/nginx/access.log", _iter=True):
    #     if "ERROR" in line:
    #         send_an_email_to_support(line)
    # print(ifconfig("wlan0"))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # uu = sh.ls("-l", "/tmp", color="never")
    # print(uu)
    # sh.bash("-c", "ls -al")
    # `
    # echo
    # test > test.txt
    # cat
    # test.txt
    # `
    # `ls -al`
    # result = `ls - l
    # print result.returncode
    # try:
    #     result = `ls - l
    #     non_existent_file
    # except NonZeroReturnCodeError as e:
    #     result = e.result
