# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # as of feb 10th, there's an issue with the default server as
  # hashicorp hasn't fixed this issue yet. Read more about the issue
  # here: https://github.com/hashicorp/vagrant/issues/9442
  Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  # config.vm.box = "ubuntu/trusty64"

  # If you don't want to run the install script then comment the last section
  # and the shell script provisioning down below. I've prepackaged all of the
  # requirements for the project since Jan 31, 2018

  config.vm.box = "wgma/quadbot"
  config.vm.box_version = "0.0.1"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder "../quadbot", "/home/vagrant/quadbot", create: true

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", path: "install.sh", privileged: true
end
