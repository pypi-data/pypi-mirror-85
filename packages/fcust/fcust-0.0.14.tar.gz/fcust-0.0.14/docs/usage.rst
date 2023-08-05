.. highlight: shell

==============================
Setting Up a Common Folder
==============================

We go through an example of how a Fedora Workstation administrator can set up a common folder.::

    $ cd /home
    # Let's create two hupothetical users (in a real installation those users would be Fedora Workstation users)
    $ sudo useradd -ms /bin/bash user1
    $ sudo useradd -ms /bin/bash user2
    # Let's create the folder that will be shared across users
    $ sudo mkdir family
    # create new group
    $ sudo groupadd family
    # Let's add our two users to the new group
    $ sudo usermod -a -G family user1
    $ sudo usermod -a -G family user2
    # Change ownership of folder
    $ sudo chown :family ./family/
    # Set common folder's permissions. We can also set the setguid sticky bit for the new folder.
    # This option forces newly created objects within the folder to inherit the foler's group rather than their default group.
    $ sudo chmod 2775 ./family/

Note that even though we used the same name for the group and the folder that is not required.

The common folder is now ready to be used. The ``fcust`` package enforces that all files and
folders in the common folder belong to the common group and that the group has read and write
permissions.



=====
Usage
=====

The package provides a command line option to enfoce group ownership and permissions:

    $ fcust /path/to/folder

``fcust`` will assume the folder is set up correctly and will try to enforce group ownership
and permissions within it.
