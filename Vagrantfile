# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"
  config.vm.network :private_network, ip: "192.168.33.33"
  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "chef/cookbooks"
    chef.roles_path = "chef/roles"
 	# chef.data_bags_path = "../my-recipes/data_bags"
    # chef.add_recipe "redis::server"
    chef.add_role "web"

    # You may also specify custom JSON attributes:
    # chef.json = { :mysql_password => "foo" }
  end
end
