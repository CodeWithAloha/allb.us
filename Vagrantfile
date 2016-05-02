# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.require_version ">= 1.7.2"

Vagrant.configure(2) do |config|

  config.ssh.insert_key = true

  config.vm.box = "geerlingguy/ubuntu1604"
  config.vm.box_check_update = false
  config.vm.define "allbus_vm"

  config.vm.network "private_network", ip: "192.168.50.50"
  config.vm.network "forwarded_port", guest: 80, host: 50808, auto_correct: true

  config.vm.provider "virtualbox" do |vm|
    vm.name = "allbus_vm"
    vm.cpus = 2
    vm.memory = 2048
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/allbus.yml"
    ansible.raw_arguments = Shellwords.shellsplit(ENV['VAGRANT_ANSIBLE_ARGS']) if ENV['VAGRANT_ANSIBLE_ARGS']
  end
end
