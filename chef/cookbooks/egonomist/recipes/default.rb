#
# Cookbook Name:: egonomist
# Recipe:: default
#
# Copyright 2013, YOUR_COMPANY_NAME
#
# All rights reserved - Do Not Redistribute
#

include_recipe "python"

directory "/home/vagrant/.venv" do
	owner "vagrant"
	group "vagrant"
	mode 00755
	action :create
end

python_virtualenv "/home/vagrant/.venv" do
  options "--system-site-packages"
  action :create
  owner "vagrant"
  group "vagrant"
end

package "libjpeg62" do
  action :install
end

package "libjpeg62-dev" do
  action :install
end

package "libfreetype6" do
  action :install
end

package "libfreetype6-dev" do
  action :install
end

package "zlib1g-dev" do
  action :install
end

execute "install_requirements" do
	cwd "/vagrant"
	path ["/home/vagrant/.venv/bin"]
	environment ({'VIRTUAL_ENV' => '/home/vagrant/.venv', 'HOME' => '/tmp/.pip'})
	command "/home/vagrant/.venv/bin/pip install -r requirements.txt"
	user "vagrant"
end

execute "sync_db" do
	cwd "/vagrant"
	path ["/home/vagrant/.venv/bin"]
	environment ({'VIRTUAL_ENV' => '/home/vagrant/.venv', 'HOME' => '/tmp/.pip'})
	command "/home/vagrant/.venv/bin/python egonomist/manage.py syncdb --noinput"
	user "vagrant"
end
