from openpyn import __basefilepath__
import subprocess


def install_service():
    openpyn_options = input("Enter Openpyn options to be stored in systemd \
service file (/etc/systemd/system/openpyn.service, \
Default(Just Press Enter) is, uk : ") or "uk"
    update_service(openpyn_options)


def update_service(openpyn_options, run=False):
    if "--silent" not in openpyn_options:
        openpyn_options += " --silent "
    if "-f" in openpyn_options or "--force-fw-rules" in openpyn_options:
        kill_option = "--kill-flush"
    else:
        kill_option = "--kill"
    openpyn_options = openpyn_options.replace("-d ", "")
    openpyn_options = openpyn_options.replace("--daemon", "")
    openpyn_location = str(subprocess.check_output(["which", "openpyn"]))[2:-3]
    sleep_location = str(subprocess.check_output(["which", "sleep"]))[2:-3]

    service_text = '\n'.join([
        '[Unit]',
        'Description=NordVPN Connection Manager',
        'Wants=network-online.target',
        'After=network-online.target',
        'After=multi-user.target',
        '[Service]',
        'Type=simple',
        'User=root',
        'WorkingDirectory={basefilepath}',
        'ExecStartPre={sleep} 10',
        'ExecStart={openpyn} {openpynopts}',
        'ExecStop={openpyn} {killopts}',
        'StandardOutput=syslog',
        'StandardError=syslog',
        '[Install]',
        'WantedBy=multi-user.target',
    ]).format(openpyn=openpyn_location, openpynopts=openpyn_options, 
              killopts=kill_option, sleep=sleep_location, 
              basefilepath=__basefilepath__)

    with open("/etc/systemd/system/openpyn.service", "w+") as service_file:
        service_file.write(service_text)

    print("\nThe Following config has been saved in openpyn.service.",
          "You can Run it or/and Enable it with: 'sudo systemctl start openpyn',",
          "'sudo systemctl enable openpyn' \n\n", service_text)

    subprocess.run(["systemctl", "daemon-reload"])
    if run:
        print("Started Openpyn by running 'systemctl start openpyn'\n\
To check VPN status, run 'systemctl status openpyn'")
        subprocess.run(["systemctl", "start", "openpyn"])
