#pylint: skip-file

import unittest
from Atomic.backendutils import BackendUtils
from Atomic.backends._docker import DockerBackend
from Atomic.backends._ostree import OSTreeBackend

no_mock = True
try:
    from unittest.mock import MagicMock, patch
    no_mock = False
except ImportError:
    try:
        from mock import MagicMock, patch
        no_mock = False
    except ImportError:
        # Mock is already set to False
        pass


BACKENDS = [DockerBackend, OSTreeBackend]
d_images = [{u'Created': 1478116329, u'Labels': {u'build-date': u'20161102', u'vendor': u'CentOS', u'name': u'CentOS Base Image', u'license': u'GPLv2'}, u'VirtualSize': 196509652, u'ParentId': u'', u'RepoTags': [u'docker.io/centos:latest'], u'RepoDigests': [u'docker.io/centos@b2f9d1c0ff5f87a4743104d099a3d561002ac500db1b9bfa02a783a46e0d366c'], u'Id': u'0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a', u'Size': 196509652}, {u'Created': 1477910440, u'Labels': {u'Version': u'7.3', u'INSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'vendor': u'Red Hat, Inc.', u'vcs-ref': u'fabbc9b2d819e919444fced9b24db3953ab254e6', u'authoritative-source-url': u'registry.access.redhat.com', u'Vendor': u'Red Hat, Inc.', u'version': u'7.3', u'com.redhat.component': u'rsyslog-docker', u'distribution-scope': u'public', u'run': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'Name': u'rhel7/rsyslog', u'License': u'GPLv3', u'Build_Host': u'ip-10-29-120-226.ec2.internal', u'vcs-type': u'git', u'Architecture': u'x86_64', u'Release': u'8', u'BZComponent': u'rsyslog-docker', u'build-date': u'2016-10-31T06:37:07.885264Z', u'com.redhat.build-host': u'ip-10-29-120-226.ec2.internal', u'UNINSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh', u'RUN': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'name': u'rhel7/rsyslog', u'architecture': u'x86_64', u'install': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'release': u'8', u'uninstall': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh'}, u'VirtualSize': 205238327, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7/rsyslog:latest'], u'RepoDigests': [u'registry.access.redhat.com/rhel7/rsyslog@729f781838054ce6085ab96a8fed45b7fdb2ed3dab2f2e1fb1b081b32e74d86c'], u'Id': u'04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265', u'Size': 205238327}, {u'Created': 1477483353, u'Labels': {u'com.redhat.component': u'rhel-server-docker', u'authoritative-source-url': u'registry.access.redhat.com', u'distribution-scope': u'public', u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'vcs-type': u'git', u'name': u'rhel7/rhel', u'vcs-ref': u'7eeaf203cf909c2c056fba7066db9c1073a28d97', u'release': u'45', u'Version': u'7.3', u'Architecture': u'x86_64', u'version': u'7.3', u'Release': u'45', u'vendor': u'Red Hat, Inc.', u'BZComponent': u'rhel-server-docker', u'build-date': u'2016-10-26T07:54:17.037911Z', u'com.redhat.build-host': u'ip-10-29-120-48.ec2.internal', u'architecture': u'x86_64'}, u'VirtualSize': 192508958, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:latest'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@da8a3e9297da7ccd1948366103d13c45b7e77489382351a777a7326004b63a21'], u'Id': u'f98706e16e41e56c4beaeea9fa77cd00fe35693635ed274f128876713afc0a1e', u'Size': 192508958}, {u'Created': 1475874238, u'Labels': {}, u'VirtualSize': 1093484, u'ParentId': u'', u'RepoTags': [u'docker.io/busybox:latest'], u'RepoDigests': [u'docker.io/busybox@29f5d56d12684887bdfa50dcd29fc31eea4aaf4ad3bec43daf19026a7ce69912'], u'Id': u'e02e811dd08fd49e7f6032625495118e63f597eb150403d02e3238af1df240ba', u'Size': 1093484}, {u'Created': 1456801947, u'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img02.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'46', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, u'VirtualSize': 203247534, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:7.2-46'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@6b76f95ab3ed949c2ca3110765f310bf8f4c9333394efba11727b14863c73f10'], u'Id': u'32f8a1d5f01956ca38f3887a83b1736da4f450d6132563c665bdc0a7a4684c4d', u'Size': 203247534}, {u'Created': 1455812978, u'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'44', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, u'VirtualSize': 203243624, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:7.2-44'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@af41b2f4e4fd2260247f1450b27da021d319ca4413e57ae833313398334d6e6f'], u'Id': u'da3ab9be742254035a2736da5d41c0a941b9a12ddd29f70b6129748e3749dd01', u'Size': 203243624}]
d_containers = [{u'Status': u'Exited (0) 51 seconds ago', u'Created': 1478633817, u'Image': u'centos', u'Labels': {u'build-date': u'20161102', u'vendor': u'CentOS', u'name': u'CentOS Base Image', u'license': u'GPLv2'}, u'NetworkSettings': {u'Networks': {u'bridge': {u'NetworkID': u'', u'MacAddress': u'', u'GlobalIPv6PrefixLen': 0, u'Links': None, u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None, u'EndpointID': u'', u'IPPrefixLen': 0, u'IPAddress': u'', u'Gateway': u'', u'Aliases': None}}}, u'HostConfig': {u'NetworkMode': u'default'}, u'ImageID': u'0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a', u'Command': u'/bin/bash', u'Names': [u'/happy_darwin'], u'Id': u'7002c7a08bfd3427f7eee23a5f54981a8637d1b3b3c3787ca94255273a1d7e43', u'Ports': []}, {u'Status': u'Up About a minute', u'Created': 1478633803, u'Image': u'registry.access.redhat.com/rhel7/rsyslog', u'Labels': {u'Version': u'7.3', u'INSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'vendor': u'Red Hat, Inc.', u'vcs-ref': u'fabbc9b2d819e919444fced9b24db3953ab254e6', u'authoritative-source-url': u'registry.access.redhat.com', u'Vendor': u'Red Hat, Inc.', u'version': u'7.3', u'com.redhat.component': u'rsyslog-docker', u'distribution-scope': u'public', u'run': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'Name': u'rhel7/rsyslog', u'License': u'GPLv3', u'Build_Host': u'ip-10-29-120-226.ec2.internal', u'vcs-type': u'git', u'Architecture': u'x86_64', u'Release': u'8', u'BZComponent': u'rsyslog-docker', u'build-date': u'2016-10-31T06:37:07.885264Z', u'com.redhat.build-host': u'ip-10-29-120-226.ec2.internal', u'UNINSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh', u'RUN': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'name': u'rhel7/rsyslog', u'architecture': u'x86_64', u'install': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'release': u'8', u'uninstall': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh'}, u'NetworkSettings': {u'Networks': {u'host': {u'NetworkID': u'', u'MacAddress': u'', u'GlobalIPv6PrefixLen': 0, u'Links': None, u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None, u'EndpointID': u'e4c76518434d598f8bcfd86fa3c377cb7d1ff4fdcad17184e42ef51069aa7125', u'IPPrefixLen': 0, u'IPAddress': u'', u'Gateway': u'', u'Aliases': None}}}, u'HostConfig': {u'NetworkMode': u'host'}, u'ImageID': u'04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265', u'Command': u'/bin/rsyslog.sh', u'Names': [u'/rsyslog'], u'Id': u'3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64', u'Ports': []}]
_rsyslog_container_inspect = {u'ExecIDs': None, u'State': {u'Status': u'running', u'Pid': 3425, u'OOMKilled': False, u'Dead': False, u'Paused': False, u'Running': True, u'FinishedAt': u'0001-01-01T00:00:00Z', u'Restarting': False, u'Error': u'', u'StartedAt': u'2016-11-08T19:36:44.44460996Z', u'ExitCode': 0}, u'Config': {u'Tty': False, u'Cmd': [u'/bin/rsyslog.sh'], u'Volumes': None, u'Domainname': u'localdomain', u'WorkingDir': u'', u'Image': u'registry.access.redhat.com/rhel7/rsyslog', u'Hostname': u'atomic-baude', u'StdinOnce': False, u'Labels': {u'Version': u'7.3', u'INSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'vendor': u'Red Hat, Inc.', u'vcs-ref': u'fabbc9b2d819e919444fced9b24db3953ab254e6', u'authoritative-source-url': u'registry.access.redhat.com', u'Vendor': u'Red Hat, Inc.', u'version': u'7.3', u'com.redhat.component': u'rsyslog-docker', u'distribution-scope': u'public', u'run': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'Name': u'rhel7/rsyslog', u'License': u'GPLv3', u'Build_Host': u'ip-10-29-120-226.ec2.internal', u'vcs-type': u'git', u'Architecture': u'x86_64', u'Release': u'8', u'BZComponent': u'rsyslog-docker', u'build-date': u'2016-10-31T06:37:07.885264Z', u'com.redhat.build-host': u'ip-10-29-120-226.ec2.internal', u'UNINSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh', u'RUN': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'name': u'rhel7/rsyslog', u'architecture': u'x86_64', u'install': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'release': u'8', u'uninstall': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh'}, u'AttachStdin': False, u'User': u'', u'Env': [u'IMAGE=registry.access.redhat.com/rhel7/rsyslog', u'NAME=rsyslog', u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', u'container=docker'], u'Entrypoint': None, u'OnBuild': None, u'AttachStderr': False, u'AttachStdout': False, u'OpenStdin': False}, u'ResolvConfPath': u'/var/lib/docker/containers/3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64/resolv.conf', u'HostsPath': u'/var/lib/docker/containers/3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64/hosts', u'Args': [], u'Driver': u'devicemapper', u'Path': u'/bin/rsyslog.sh', u'HostnamePath': u'/var/lib/docker/containers/3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64/hostname', u'RestartCount': 0, u'Name': u'/rsyslog', u'Created': u'2016-11-08T19:36:43.024272115Z', u'GraphDriver': {u'Data': {u'DeviceName': u'docker-253:1-20984667-ca3eae26c63b8bd867536b53b7e5fade1eae923a2999864b31546f06eb19b123', u'DeviceSize': u'10737418240', u'DeviceId': u'10'}, u'Name': u'devicemapper'}, u'Mounts': [{u'RW': True, u'Source': u'/etc/pki/rsyslog', u'Destination': u'/etc/pki/rsyslog', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/var/lib/rsyslog', u'Destination': u'/var/lib/rsyslog', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/run', u'Destination': u'/run', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/etc/sysconfig/rsyslog', u'Destination': u'/etc/sysconfig/rsyslog', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/var/log', u'Destination': u'/var/log', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/etc/rsyslog.conf', u'Destination': u'/etc/rsyslog.conf', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/etc/machine-id', u'Destination': u'/etc/machine-id', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/etc/localtime', u'Destination': u'/etc/localtime', u'Mode': u'', u'Propagation': u'rslave'}, {u'RW': True, u'Source': u'/etc/rsyslog.d', u'Destination': u'/etc/rsyslog.d', u'Mode': u'', u'Propagation': u'rslave'}], u'ProcessLabel': u'', u'NetworkSettings': {u'Bridge': u'', u'Networks': {u'host': {u'NetworkID': u'f5f370f21b319d55187d4c05eabb4dfce1d866b8d5ad02069c16c9c59067bc2e', u'MacAddress': u'', u'GlobalIPv6PrefixLen': 0, u'Links': None, u'GlobalIPv6Address': u'', u'IPv6Gateway': u'', u'IPAMConfig': None, u'EndpointID': u'e4c76518434d598f8bcfd86fa3c377cb7d1ff4fdcad17184e42ef51069aa7125', u'IPPrefixLen': 0, u'IPAddress': u'', u'Gateway': u'', u'Aliases': None}}, u'SecondaryIPv6Addresses': None, u'LinkLocalIPv6Address': u'', u'HairpinMode': False, u'IPv6Gateway': u'', u'SecondaryIPAddresses': None, u'SandboxID': u'eb35aa677a88a07be28fd08c0bfae2d4eafc3a56637cc07f34acd31d8ac740de', u'MacAddress': u'', u'GlobalIPv6Address': u'', u'Gateway': u'', u'LinkLocalIPv6PrefixLen': 0, u'EndpointID': u'', u'SandboxKey': u'/var/run/docker/netns/default', u'GlobalIPv6PrefixLen': 0, u'IPPrefixLen': 0, u'IPAddress': u'', u'Ports': {}}, u'AppArmorProfile': u'', u'Image': u'04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265', u'LogPath': u'', u'HostConfig': {u'CpuPeriod': 0, u'MemorySwappiness': -1, u'ContainerIDFile': u'', u'MemorySwap': 0, u'BlkioDeviceReadIOps': None, u'CpuQuota': 0, u'Dns': [], u'ExtraHosts': None, u'PidsLimit': 0, u'DnsSearch': [], u'Privileged': True, u'Ulimits': None, u'CpusetCpus': u'', u'CgroupParent': u'', u'BlkioWeight': 0, u'RestartPolicy': {u'MaximumRetryCount': 0, u'Name': u'always'}, u'OomScoreAdj': 0, u'BlkioDeviceReadBps': None, u'VolumeDriver': u'', u'ReadonlyRootfs': False, u'CpuShares': 0, u'PublishAllPorts': False, u'MemoryReservation': 0, u'BlkioWeightDevice': None, u'ConsoleSize': [0, 0], u'NetworkMode': u'host', u'BlkioDeviceWriteBps': None, u'Isolation': u'', u'GroupAdd': None, u'Devices': [], u'BlkioDeviceWriteIOps': None, u'Binds': [u'/etc/machine-id:/etc/machine-id', u'/etc/localtime:/etc/localtime', u'/var/lib/rsyslog:/var/lib/rsyslog', u'/run:/run', u'/etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog', u'/etc/rsyslog.d:/etc/rsyslog.d', u'/var/log:/var/log', u'/etc/pki/rsyslog:/etc/pki/rsyslog', u'/etc/rsyslog.conf:/etc/rsyslog.conf'], u'CpusetMems': u'', u'KernelMemory': 0, u'UTSMode': u'', u'PidMode': u'host', u'VolumesFrom': None, u'CapDrop': None, u'DnsOptions': [], u'ShmSize': 67108864, u'Links': None, u'IpcMode': u'', u'PortBindings': {}, u'SecurityOpt': [u'label:disable'], u'CapAdd': None, u'Memory': 0, u'OomKillDisable': False, u'LogConfig': {u'Config': {}, u'Type': u'journald'}}, u'Id': u'3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64', u'MountLabel': u''}
_rsyslog_image_inspect = {u'Comment': u'', u'Container': u'', u'DockerVersion': u'1.9.1', u'Parent': u'', u'Created': u'2016-10-31T10:40:40.771883Z', u'Config': {u'Tty': False, u'Cmd': [u'/bin/rsyslog.sh'], u'Volumes': None, u'Domainname': u'', u'WorkingDir': u'', u'Image': u'91c58d6c27c4a47876f1851b70cbcd416e3f84466730385f7d663e87b1d63a4f', u'Hostname': u'', u'StdinOnce': False, u'Labels': {u'Version': u'7.3', u'INSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'vendor': u'Red Hat, Inc.', u'vcs-ref': u'fabbc9b2d819e919444fced9b24db3953ab254e6', u'authoritative-source-url': u'registry.access.redhat.com', u'Vendor': u'Red Hat, Inc.', u'version': u'7.3', u'com.redhat.component': u'rsyslog-docker', u'distribution-scope': u'public', u'run': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'Name': u'rhel7/rsyslog', u'License': u'GPLv3', u'Build_Host': u'ip-10-29-120-226.ec2.internal', u'vcs-type': u'git', u'Architecture': u'x86_64', u'Release': u'8', u'BZComponent': u'rsyslog-docker', u'build-date': u'2016-10-31T06:37:07.885264Z', u'com.redhat.build-host': u'ip-10-29-120-226.ec2.internal', u'UNINSTALL': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh', u'RUN': u'docker run -d --privileged --name NAME --net=host --pid=host -v /etc/pki/rsyslog:/etc/pki/rsyslog -v /etc/rsyslog.conf:/etc/rsyslog.conf -v /etc/sysconfig/rsyslog:/etc/sysconfig/rsyslog -v /etc/rsyslog.d:/etc/rsyslog.d -v /var/log:/var/log -v /var/lib/rsyslog:/var/lib/rsyslog -v /run:/run -v /etc/machine-id:/etc/machine-id -v /etc/localtime:/etc/localtime -e IMAGE=IMAGE -e NAME=NAME --restart=always IMAGE /bin/rsyslog.sh', u'name': u'rhel7/rsyslog', u'architecture': u'x86_64', u'install': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/install.sh', u'release': u'8', u'uninstall': u'docker run --rm --privileged -v /:/host -e HOST=/host -e IMAGE=IMAGE -e NAME=NAME IMAGE /bin/uninstall.sh'}, u'AttachStdin': False, u'User': u'', u'Env': [u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', u'container=docker'], u'Entrypoint': None, u'OnBuild': [], u'AttachStderr': False, u'AttachStdout': False, u'OpenStdin': False}, u'Author': u'Red Hat, Inc.', u'GraphDriver': {u'Data': {u'DeviceName': u'docker-253:1-20984667-37714020f437aa4430146d44e91f1c067ac18b42265acd265d20e7ad674474e6', u'DeviceSize': u'10737418240', u'DeviceId': u'5'}, u'Name': u'devicemapper'}, u'VirtualSize': 205238327, u'Os': u'linux', u'Architecture': u'amd64', u'ContainerConfig': {u'Tty': False, u'Cmd': None, u'Volumes': None, u'Domainname': u'', u'WorkingDir': u'', u'Image': u'', u'Hostname': u'', u'StdinOnce': False, u'Labels': None, u'AttachStdin': False, u'User': u'', u'Env': None, u'Entrypoint': None, u'OnBuild': None, u'AttachStderr': False, u'AttachStdout': False, u'OpenStdin': False}, u'Size': 205238327, u'RepoDigests': [u'registry.access.redhat.com/rhel7/rsyslog@729f781838054ce6085ab96a8fed45b7fdb2ed3dab2f2e1fb1b081b32e74d86c'], u'Id': u'04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265', u'RepoTags': [u'registry.access.redhat.com/rhel7/rsyslog:latest']}
_centos_name_search = [{'Created': 1478116329, 'RepoDigests': ['docker.io/centos@b2f9d1c0ff5f87a4743104d099a3d561002ac500db1b9bfa02a783a46e0d366c'], 'Id': '0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a', 'Labels': {'build-date': '20161102', 'license': 'GPLv2', 'name': 'CentOS Base Image', 'vendor': 'CentOS'}, 'Size': 196509652, 'RepoTags': ['docker.io/centos:latest'], 'VirtualSize': 196509652, 'ParentId': ''}]
_centos_inspect_image = {u'Comment': u'', u'Container': u'58aeaa4866c2845b48ab998b7cba3856a9fb64a681f92544cb035b85066b5102', u'DockerVersion': u'1.12.1', u'Parent': u'', u'Created': u'2016-11-02T19:52:09.463959047Z', u'Config': {u'Tty': False, u'Cmd': [u'/bin/bash'], u'Volumes': None, u'Domainname': u'', u'WorkingDir': u'', u'Image': u'5a2725191d75eb64e9b7c969cd23d8c67c6e8af9979e521a417bbfa34434fb83', u'Hostname': u'd6dcf178f680', u'StdinOnce': False, u'Labels': {u'build-date': u'20161102', u'vendor': u'CentOS', u'name': u'CentOS Base Image', u'license': u'GPLv2'}, u'AttachStdin': False, u'User': u'', u'Env': [u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'], u'Entrypoint': None, u'OnBuild': None, u'AttachStderr': False, u'AttachStdout': False, u'OpenStdin': False}, u'Author': u'https://github.com/CentOS/sig-cloud-instance-images', u'GraphDriver': {u'Data': {u'DeviceName': u'docker-253:1-20984667-e3af0c61256f885331fb1a3adc27ea509a10ba9a0ba9175c1a149f81bddcd30d', u'DeviceSize': u'10737418240', u'DeviceId': u'2'}, u'Name': u'devicemapper'}, u'VirtualSize': 196509652, u'Os': u'linux', u'Architecture': u'amd64', u'ContainerConfig': {u'Tty': False, u'Cmd': [u'/bin/sh', u'-c', u'#(nop) ', u'CMD ["/bin/bash"]'], u'Volumes': None, u'Domainname': u'', u'WorkingDir': u'', u'Image': u'5a2725191d75eb64e9b7c969cd23d8c67c6e8af9979e521a417bbfa34434fb83', u'Hostname': u'd6dcf178f680', u'StdinOnce': False, u'Labels': {u'build-date': u'20161102', u'vendor': u'CentOS', u'name': u'CentOS Base Image', u'license': u'GPLv2'}, u'AttachStdin': False, u'User': u'', u'Env': [u'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'], u'Entrypoint': None, u'OnBuild': None, u'AttachStderr': False, u'AttachStdout': False, u'OpenStdin': False}, u'Size': 196509652, u'RepoDigests': [u'docker.io/centos@b2f9d1c0ff5f87a4743104d099a3d561002ac500db1b9bfa02a783a46e0d366c'], u'Id': u'0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a', u'RepoTags': [u'docker.io/centos:latest']}
_rhel_images = [{'VirtualSize': 192508958, 'Id': 'f98706e16e41e56c4beaeea9fa77cd00fe35693635ed274f128876713afc0a1e', 'Labels': {'vcs-ref': '7eeaf203cf909c2c056fba7066db9c1073a28d97', 'build-date': '2016-10-26T07:54:17.037911Z', 'release': '45', 'Release': '45', 'Build_Host': 'rcm-img01.build.eng.bos.redhat.com', 'distribution-scope': 'public', 'Name': 'rhel7/rhel', 'vcs-type': 'git', 'com.redhat.build-host': 'ip-10-29-120-48.ec2.internal', 'vendor': 'Red Hat, Inc.', 'authoritative-source-url': 'registry.access.redhat.com', 'com.redhat.component': 'rhel-server-docker', 'architecture': 'x86_64', 'BZComponent': 'rhel-server-docker', 'Vendor': 'Red Hat, Inc.', 'version': '7.3', 'Version': '7.3', 'Architecture': 'x86_64', 'name': 'rhel7/rhel'}, 'ParentId': '', 'RepoDigests': ['registry.access.redhat.com/rhel7@da8a3e9297da7ccd1948366103d13c45b7e77489382351a777a7326004b63a21'], 'RepoTags': ['registry.access.redhat.com/rhel7:latest'], 'Created': 1477483353, 'Size': 192508958}]
_multiple_images = [{u'Created': 1477483353, u'Labels': {u'com.redhat.component': u'rhel-server-docker', u'authoritative-source-url': u'registry.access.redhat.com', u'distribution-scope': u'public', u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'vcs-type': u'git', u'name': u'rhel7/rhel', u'vcs-ref': u'7eeaf203cf909c2c056fba7066db9c1073a28d97', u'release': u'45', u'Version': u'7.3', u'Architecture': u'x86_64', u'version': u'7.3', u'Release': u'45', u'vendor': u'Red Hat, Inc.', u'BZComponent': u'rhel-server-docker', u'build-date': u'2016-10-26T07:54:17.037911Z', u'com.redhat.build-host': u'ip-10-29-120-48.ec2.internal', u'architecture': u'x86_64'}, u'VirtualSize': 192508958, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:latest'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@da8a3e9297da7ccd1948366103d13c45b7e77489382351a777a7326004b63a21'], u'Id': u'f98706e16e41e56c4beaeea9fa77cd00fe35693635ed274f128876713afc0a1e', u'Size': 192508958}, {u'Created': 1456801947, u'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img02.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'46', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, u'VirtualSize': 203247534, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:7.2-46'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@6b76f95ab3ed949c2ca3110765f310bf8f4c9333394efba11727b14863c73f10'], u'Id': u'32f8a1d5f01956ca38f3887a83b1736da4f450d6132563c665bdc0a7a4684c4d', u'Size': 203247534}, {u'Created': 1455812978, u'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'44', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, u'VirtualSize': 203243624, u'ParentId': u'', u'RepoTags': [u'registry.access.redhat.com/rhel7:7.2-44'], u'RepoDigests': [u'registry.access.redhat.com/rhel7@af41b2f4e4fd2260247f1450b27da021d319ca4413e57ae833313398334d6e6f'], u'Id': u'da3ab9be742254035a2736da5d41c0a941b9a12ddd29f70b6129748e3749dd01', u'Size': 203243624}]


@unittest.skipIf(no_mock, "Mock not found")
class TestDockerBackend(unittest.TestCase):


    def test_get_images(self):
        db = DockerBackend()
        db.d.images = MagicMock(return_value=d_images)
        images = db.get_images()
        self.assertTrue(len(images) > 0)

    def test_inspect_image(self):
        db = DockerBackend()
        db._inspect_image = MagicMock(return_value=_rsyslog_image_inspect)
        img_obj = db.inspect_image('registry.access.redhat.com/rhel7/rsyslog:latest')
        self.assertIsNotNone(img_obj)

    def test_long_version(self):
        db = DockerBackend()
        db._inspect_image = MagicMock(return_value=_rsyslog_image_inspect)
        img_obj = db.inspect_image('registry.access.redhat.com/rhel7/rsyslog:latest')
        self.assertEqual(img_obj.long_version, "7.3-8")

    def test_inspect_container(self):
        db = DockerBackend()
        db._inspect_container = MagicMock(return_value=_rsyslog_container_inspect)
        con_obj = db.inspect_container('3e014f35a7d0')
        self.assertIsNotNone(con_obj)

    def test_container_obj_id(self):
        db = DockerBackend()
        db._inspect_container = MagicMock(return_value=_rsyslog_container_inspect)
        con_obj = db.inspect_container('3e014f35a7d0')
        self.assertEqual(con_obj.id, '3e014f35a7d0a22579cdad033edefd287fe01cac0e52dd68162e477fc150dc64')
        self.assertEqual(con_obj.image, '04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265')

    def test_has_image_by_inspect(self):
        db = DockerBackend()
        db._inspect_image = MagicMock(return_value=_rsyslog_image_inspect)
        img_object = db.has_image('registry.access.redhat.com/rhel7/rsyslog:latest')
        self.assertEqual(img_object.id, '04f7e9543b939537000296e38c11d5d422653f74a6dd2a3905b931bb8f4c3265')

    def test_has_image_by_name(self):
        with patch('Atomic.util.image_by_name') as mockobj:
            mockobj.return_value = _centos_name_search
            db = DockerBackend()
            db.inspect_image = MagicMock(return_value=None)
            db._inspect_image = MagicMock(return_value=_centos_inspect_image)
            img_obj = db.has_image('centos')
            self.assertEqual(img_obj.id, '0584b3d2cf6d235ee310cf14b54667d889887b838d3f3d3033acd70fc3c48b8a')


    def test_has_image_not_found(self):
        with patch('Atomic.util.image_by_name') as mockobj:
            mockobj.return_value = []
            db = DockerBackend()
            db._inspect_image = MagicMock(return_value=None)
            self.assertIsNone(db.has_image('foobar'))

    def test_has_image_multiple(self):
        with patch('Atomic.util.image_by_name') as mockobj:
            mockobj.return_value = _multiple_images
            db = DockerBackend()
            db._get_images = MagicMock(return_value=d_images)
            db._inspect_image = MagicMock(return_value=None)
            self.assertRaises(ValueError, db.has_image, 'registry.access.redhat.com/rhel7')

o_images = [{'Labels': {u'com.redhat.component': u'rhel-server-docker', u'authoritative-source-url': u'registry.access.redhat.com', u'distribution-scope': u'public', u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'vcs-type': u'git', u'build-date': u'2016-10-26T07:54:17.037911Z', u'Release': u'45', u'Version': u'7.3', u'Architecture': u'x86_64', u'version': u'7.3', u'release': u'45', u'vendor': u'Red Hat, Inc.', u'BZComponent': u'rhel-server-docker', u'vcs-ref': u'7eeaf203cf909c2c056fba7066db9c1073a28d97', u'architecture': u'x86_64', u'com.redhat.build-host': u'ip-10-29-120-48.ec2.internal', u'name': u'rhel7/rhel'}, 'Names': [], 'Created': 1478630928, 'OSTree-rev': 'be942c330bde705f6dc5c82068927b671bbf1cf0c785ae7d93ae3d49f789fc2b', 'RepoTags': ['registry.access.redhat.com/rhel7:latest'], 'Id': u'da8a3e9297da7ccd1948366103d13c45b7e77489382351a777a7326004b63a21', 'ImageType': 'system', 'ImageId': u'da8a3e9297da7ccd1948366103d13c45b7e77489382351a777a7326004b63a21'}, {'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img01.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'44', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, 'Names': [], 'Created': 1478631019, 'OSTree-rev': 'f5c4a4dddaad670feb80aa272c6ea228831ee90f6dba93f0bbef246bfd96eb43', 'RepoTags': ['registry.access.redhat.com/rhel7:7.2-44'], 'Id': u'af41b2f4e4fd2260247f1450b27da021d319ca4413e57ae833313398334d6e6f', 'ImageType': 'system', 'ImageId': u'af41b2f4e4fd2260247f1450b27da021d319ca4413e57ae833313398334d6e6f'}, {'Labels': {u'Vendor': u'Red Hat, Inc.', u'Name': u'rhel7/rhel', u'Build_Host': u'rcm-img02.build.eng.bos.redhat.com', u'Version': u'7.2', u'Architecture': u'x86_64', u'Release': u'46', u'BZComponent': u'rhel-server-docker', u'Authoritative_Registry': u'registry.access.redhat.com'}, 'Names': [], 'Created': 1478631057, 'OSTree-rev': '6705ceedb07aad7040d2e7251117cb5d8a2b56750735c621b51f1969c7e55fbd', 'RepoTags': ['registry.access.redhat.com/rhel7:7.2-46'], 'Id': u'6b76f95ab3ed949c2ca3110765f310bf8f4c9333394efba11727b14863c73f10', 'ImageType': 'system', 'ImageId': u'6b76f95ab3ed949c2ca3110765f310bf8f4c9333394efba11727b14863c73f10'}, {'Labels': {}, 'Names': [], 'Created': 1478631019, 'OSTree-rev': 'c10f4558f1d0eddc51f0d060cfc99401963d8bcdc680ea972658560d4fcc63a3', 'RepoTags': ['<none>'], 'Id': '48ef8b1e90ce99f9716358e924be716c227b9b7fd55378cca04622f717acef55', 'ImageType': 'system', 'ImageId': '48ef8b1e90ce99f9716358e924be716c227b9b7fd55378cca04622f717acef55'}, {'Labels': {}, 'Names': [], 'Created': 1478630866, 'OSTree-rev': '3ee8339a98332077459ada306fc48e9bdcc664f9f06aae7d5be8ef8d8e77468a', 'RepoTags': ['<none>'], 'Id': '3690ec4760f95690944da86dc4496148a63d85c9e3100669a318110092f6862f', 'ImageType': 'system', 'ImageId': '3690ec4760f95690944da86dc4496148a63d85c9e3100669a318110092f6862f'}, {'Labels': {}, 'Names': [], 'Created': 1478630953, 'OSTree-rev': '54326755640d70b26b15d35295e4ffa7c01e9bc0a6b46049cbed8088a36dacc6', 'RepoTags': ['docker.io/library/busybox:latest'], 'Id': u'29f5d56d12684887bdfa50dcd29fc31eea4aaf4ad3bec43daf19026a7ce69912', 'ImageType': 'system', 'ImageId': u'29f5d56d12684887bdfa50dcd29fc31eea4aaf4ad3bec43daf19026a7ce69912'}, {'Labels': {}, 'Names': [], 'Created': 1478631057, 'OSTree-rev': '793efe11094a09d47b7e42f6de8689b2519bbb7eca98a8c2f48caca0db2be59f', 'RepoTags': ['<none>'], 'Id': 'f075d88cadb6e82d374f1dd04ca9e6e44a24bbb524cf5b235e92bffca89c04fa', 'ImageType': 'system', 'ImageId': 'f075d88cadb6e82d374f1dd04ca9e6e44a24bbb524cf5b235e92bffca89c04fa'}, {'Labels': {}, 'Names': [], 'Created': 1478630928, 'OSTree-rev': 'bd3d84f73d3424a61c5797688a2eea12e83b3a441c95448bfcf943cac9518571', 'RepoTags': ['<none>'], 'Id': '9b0dee6356a152d6cbac4adf6ce40ae4df40442d559931862ad65c78ed373979', 'ImageType': 'system', 'ImageId': '9b0dee6356a152d6cbac4adf6ce40ae4df40442d559931862ad65c78ed373979'}, {'Labels': {}, 'Names': [], 'Created': 1478630928, 'OSTree-rev': 'd10d6facaa596ea16ff7f30ce221669fce15a60ee643ad051a65f0d2ce855ec8', 'RepoTags': ['<none>'], 'Id': '972548a33962c6f466128fc90db5d224d8bb5f589ffd9a998a43f323c7111cf5', 'ImageType': 'system', 'ImageId': '972548a33962c6f466128fc90db5d224d8bb5f589ffd9a998a43f323c7111cf5'}, {'Labels': None, 'Names': [], 'Created': 1478630866, 'OSTree-rev': 'b42139867c4c55a28bee9d63801c3c892bfdf23fe59c4624a49f99b6aa138d1d', 'RepoTags': ['alpine:latest'], 'Id': u'1354db23ff5478120c980eca1611a51c9f2b88b61f24283ee8200bf9a54f2e5c', 'ImageType': 'system', 'ImageId': u'1354db23ff5478120c980eca1611a51c9f2b88b61f24283ee8200bf9a54f2e5c'}, {'Labels': {}, 'Names': [], 'Created': 1478630953, 'OSTree-rev': '5ba9ede4f40d0fb001906cedc45ae001015172042f50585924674f78e5b16ad0', 'RepoTags': ['<none>'], 'Id': '56bec22e355981d8ba0878c6c2f23b21f422f30ab0aba188b54f1ffeff59c190', 'ImageType': 'system', 'ImageId': '56bec22e355981d8ba0878c6c2f23b21f422f30ab0aba188b54f1ffeff59c190'}]


@unittest.skipIf(no_mock, "Mock not found")
class TestOSTreeBackend(unittest.TestCase):

    def test_get_images(self):
        pass

@unittest.skipIf(no_mock, "Mock not found")
class TestBackendUtils(unittest.TestCase):

    bu = BackendUtils()

    def test_get_backend_for_image_preferred(self):
        pass

    def test_get_backend_for_image(self):
        pass

if __name__ == '__main__':
    unittest.main()
