import sys
import os

PORT_START = int(sys.argv[1])
PORT_END = int(sys.argv[2])
PID_PATH = sys.argv[3]


def read_sample(path):
    f = open(path)
    data = str(f.read())
    f.close()

    return data


def create_conf(data, port, pid_path, path):
    v1 = data.replace("{{port}}", str(port))
    v2 = v1.replace("{{pid_path}}", pid_path)
    wf = open(path, "w")
    wf.write(v2)
    wf.close()
    return True


if __name__ == "__main__":
    data = read_sample("./sample.conf")
    servers = []
    cwd = os.getcwd()
    for i in range(PORT_START, PORT_END+1):
        newname = f"{cwd}/{i}.conf"
        create_conf(data, i, PID_PATH, newname)
        servers.append(f"127.0.0.1:{i}")
        print(f"redis-server {cwd}/{i}.conf")
        
    print("redis-cli --cluster create " + " ".join(servers))
    print("redis-cli --cluster add-node {primary} {replica} --cluster-slave")
