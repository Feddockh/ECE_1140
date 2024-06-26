import paramiko
class RaspberryPI:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def send_command_via_ssh(self, message):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.hostname, username=self.username, password=self.password)
            
            # Use echo command to send the message and print it
            command = f'echo "{message}"'
            stdin, stdout, stderr = ssh.exec_command(command)
            print("STDOUT:")
            print(stdout.read().decode())
            print("STDERR:")
            print(stderr.read().decode())

            # Close the connection
            ssh.close()
        except paramiko.AuthenticationException as auth_exc:
            print(f"Authentication failed: {auth_exc}")
        except paramiko.SSHException as ssh_exc:
            print(f"SSH connection failed: {ssh_exc}")
        except Exception as exc:
            print(f"Exception occurred: {exc}")

# Example usage:
hostname = 'raspberrypi'
username = 'garrett'
password = 'Cornell@26'

pi = RaspberryPI(hostname, username, password)
pi.send_command_via_ssh("Hello, Raspberry Pi!")
