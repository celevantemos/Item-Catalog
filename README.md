# Catalog App

This is an Item Catalog application made with Flask. It is an app that provide a list of items for each category. It also has a registration and authentication system. The project uses RESTful web application that allows only users to perform CRUD operations.

# Applications Needed
- [Vagrant](https://www.vagrantup.com)
- [VirtualBox](https://www.virtualbox.org)
- [Udacity VagrantFile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)

# How To Run
- Install Vagrant.
- Install VirtualBox.
- Clone the Vagrantfile from Udacity Repo.
- Clone the repo `catalog` found in this vagrant directory.
- Run `vagrant up` to start the virtual machine.
- Run `vagrant ssh` to login to the virtual machine.
- `cd` to the directory where `install.txt` is located.
- Run `sudo pip install -r install.txt` to install all requirements.
- Run `python database_setup.py` then `python categoriesItems.py` to initialize the database and load it with demo data.
- Finally run the application `python application.py`.
- To open the application, open `http://localhost:5000/catalog`.

# JSON links
- To get all categories with their items open `http://localhost:5000/catalog.JSON`.
- To get all categories only opne `http://localhost:5000/catalog/categories/JSON`.
- To get all items for a selected category open `http://localhost:5000/catalog/<Catalog Name>/JSON`. Note: replace `Catalog Name` with the catalog name you desire.
- To get a specific item, open `http://localhost:5000/catalog/<Catalog Name>/items/<Item Name>`. Note: replace both `Catalog Name` and `Item Name` with the catalog name and the item name you desire.

# Issues
* Cannot have the same item name.
* Only google users can register and can Add, Edit and Delete items that they created.
