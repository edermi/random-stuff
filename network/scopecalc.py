import netaddr
import sys

def print_net(name: str, networks: netaddr.IPSet):
    print("########## {}: ##########".format(name))
    for network in networks.iter_cidrs():
        print(network)


def main():
    targets = netaddr.IPSet()
    excludes = netaddr.IPSet()
    includefile = sys.argv[1]

    with open(includefile, 'r') as ic:
        for line in ic.read().splitlines():
            try:
                targets.add(netaddr.IPNetwork(line))
            except:
                print("error on {}".format(line))

    if len(sys.argv) > 2:
        excludefile = sys.argv[2]
        with open(excludefile, 'r') as ec:
            for line in ec.read().splitlines():
                try:
                    excludes.add(netaddr.IPNetwork(line))
                except:
                    print("error on {}".format(line))

    without_excludes = targets - excludes
    print_net("Includes without excludes", without_excludes)
    print_net("Excludes only", excludes)



if __name__ == '__main__':
    main()

