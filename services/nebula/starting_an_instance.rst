##########################################
Introduction to Starting a Nebula Instance
##########################################

Getting Started
===============

Visit http://nebula.ncsa.illinois.edu in a browser to log into the Horizon Interface of the NCSA Nebula OpenStack.

After logging in, you should see the LSST project space on Nebula, with main menu options on the left, and an Overview of the LSST project's resource usage and limits will be displayed:

.. image:: /_static/services/nebula/nebula_intro_s1.png

Select the **Compute** → **Instances** menu item to bring up a list of the current set of LSST instances (also referred to as VMs or 'servers').
The list of instances provides information such as the Instance name, the base Image from which the instance was booted, internal and external IP numbers, the Size or flavor of the instance, current status, and more.
In addition to the information on instances, the interface for launching a new instance can be initialized from this page. 

.. image:: /_static/services/nebula/nebula_intro_s2.png

Working from the submenu above Instance list, select the **Launch Instance** item (to the left of the red **Terminate Instances** button)  to get started with the process of creating a new instance.

.. image:: /_static/services/nebula/nebula_intro_s3.png

Select an instance type
-----------------------

The first Panel of the Launch Instance interface has a number of fields to consider.
For the first, Availability Zone, select "nova".
The Instance Name field is initially blank, so proceed by entering a name/label to designate the instance.
Using your username with the Instance Name is a reasonable way to eventually locate your instance within the full list of project instances, but there are certainly other ways.
Next, the choice of "Flavor" is an important one relating to the planned use of instance/server.
Options such as ``m1.tiny`` and ``m1.small`` are primarily used for testing OpenStack functionality itself (along the lines of 'hello world'), and may not be useful for practical work.
Additional  options include ``m1.medium``, ``m1.large``,  ``m1.xlarge``, which offer  more significant disk, memory:

+---------------+----------+-----------------+-------+
|               | RAM (MB) | Total Disk (GB) | VCPUS |
+===============+==========+=================+=======+
| ``m1.medium`` | 4096     | 40              | 2     |
+---------------+----------+-----------------+-------+
| ``m1.large``  | 8192     | 80              | 4     |
+---------------+----------+-----------------+-------+
| ``m1.xlarge`` | 16384    | 160             | 8     |
+---------------+----------+-----------------+-------+

But it should be noted that these configurations offer  2 GB/core memory.
This ratio of memory per core may be unsuitable for default LSST stack builds and individual applications.
If your plan is to build the LSST Stack or if your application benefits from more memory per core, then it is better to consider options ``r1.medium`` or ``r2.medium`` which offer different profiles.


+---------------+----------+-----------------+-------+
|               | RAM (MB) | Total Disk (GB) | VCPUS |
+===============+==========+=================+=======+
| ``r1.medium`` | 8192     | 40              | 2     |
+---------------+----------+-----------------+-------+
| ``r2.medium`` | 16384    | 40              | 2     |
+---------------+----------+-----------------+-------+

For **Instance Count**, selecting ``1`` is appropriate for the base case of starting up a single server, but you can select  a higher count if you are ready to start up a working cluster on Nebula.

For **Instance Boot Source** the selection ``Boot From Image`` is a standard approach for initial OpenStack work, and will present an **Image Name** choice box that includes standard cloud base images for CentOS 6, CentOS 7, Ubuntu 14.04, Ubuntu 15.04, cirros 0.3.4, as well  options for Fedora, Debian, CoreOS, etc.
For this Intro we'll proceed with CentOS 7 selected.

Security groups
---------------

.. image:: /_static/services/nebula/nebula_intro_s4.png

The second Panel of the Launch Instance interface has fields pertinent to secure access and firewall type configuration.
First, select a "Key Pair" to be used for ssh access to the instance (refer to the separate page "Generating or Uploading a Key Pair" for background).
Second, selecting the proper Security Groups is important to prevent problems/blockers down the line.
To enable ssh access into the instance after startup, select the ``remote SSH`` security group.
If the instance may run web servers/services, select ``remote http``, ``remote https``, to ensure that the standard ports will be open.
Another useful option is the ``localtest`` security group which will open a wide range of ports within the NCSA realm.
This is useful for opening communication with other DM Development servers in the 'LSST cluster'  (e.g., ``lsst-dev.ncsa.illinois.edu``), and can be used to debug firewall issues between OpenStack instances and realms outside NCSA.

Networking
----------

.. image:: /_static/services/nebula/nebula_intro_s5.png

The third Panel involves networking.
For the standard path, select or drag into the box the option ``LSST-net``.
It is possible to create user-defined networks and attach instances to such networks, though this case would be for specific applications and is beyond our current scope.
The last two panels, **Post-creation** and **Advanced Options**, provide the ability to customize the instance after the initial startup in a scripted manner (**Post-creation**) and to manually partition the disk of the instance (**Advanced Options**).
We skip these for our current test case, and proceed to press the blue **Launch** button at the lower right to initiate the startup process.

Launch
------

.. image:: /_static/services/nebula/nebula_intro_s6.png

After pressing **Launch** we should observe the new instance to be "Spawning."
For most instances the startup should fairly quick (less than a minute), though the startup could take longer if the base image or snapshot that is being used is large (several GB for example).

.. image:: /_static/services/nebula/nebula_intro_s7.png

After a short time we observe the newly created instance to be in the  "Running" state.
We can view the parameters that characterize the instance as per our specifications:, the instance name, the base image, the flavor/size, the keys configured for access, etc..
Under **IP address** we find the IP on the internal ``LSST-net`` network that was used in starting the instance, in this case ``172.16.1.168``.
While this locates the instance on the internal network, it is not usable for access from the outside.

Associating a floating IP
-------------------------

To enable external access we proceed to **Associate Floating IP** by selecting this option on the **Actions** menu on the very right of the Instance list (each instance has such a menu):

.. image:: /_static/services/nebula/nebula_intro_s8.png

.. image:: /_static/services/nebula/nebula_intro_s9.png

With the **Manage Floating IP Associations** window open, we can now select a public IP address to use (for NCSA Nebula, these will be in the range ``141.142.208.xxx``).
If the list of available of public IP addresses happens to be empty, one can generate an IP for use by clicking on the "+" sign to the right of the selection box.
After pressing "Associate" (and a possibly refreshing the Instance List) , we should observe the Floating IP for the instance, in this example ``141.142.208.193``.

.. image:: /_static/services/nebula/nebula_intro_s10.png

We should now be able to work in a Unix shell and log in to the new instance, issuing in this example the command

.. code-block:: bash

   ssh -i lsst-daues4.pem centos@141.142.208.193

.. image:: /_static/services/nebula/nebula_intro_s11.png

Because the base image used in this exercise was a CentOS 7 image, we log in making use of a user ``centos`` that by default exists on the base image.
For other base images/OS's,  this user is different though sensibly named: on Ubuntu the user is ``ubuntu``, on cirros the user is ``cirros``,  on CoreOS the user is ``core``. 

One should also observe the ability to become superuser on the system, i.e., after issuing

.. code-block:: bash

   sudo su -

the ``centos`` user should become ``root`` in a passwordless manner.
As ``root`` one can now configure the instance as wanted.
