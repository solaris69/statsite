###############################
# 
#
# This vagrant is modified to use with BAMS 
# and VMWARE Workstation + vagrant plugin.
# 
#
###############################
VAGRANTFILE_API_VERSION = "2"

$script = <<CODE

echo
echo Provisioning started...
echo

sudo apt-get update
sudo apt-get -y install build-essential scons python-setuptools lsof git automake
sudo easy_install pip
sudo pip install pytest

cd /vagrant/deps/check-0.9.8/
./configure
make
make install
ldconfig

CODE

$script_yum = <<CODE

echo
echo Provisioning started...
echo

sudo yum update
sudo yum -y install build-essential scons python-setuptools lsof git automake
sudo easy_install pip
sudo pip install pytest

cd /vagrant/deps/check-0.9.8/
./configure
make
make install
ldconfig

CODE


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.provider "vmware_workstation" do |v|
#    v.gui = true
    v.vmx["memsize"] = "2048"
    v.vmx["numvcpus"] = "2"
  end

#  config.vm.box_url = "http://bams-sami-api.int.thomsonreuters.com/artifactory/default.vagrant.local/compass/cudl/williamyeh_ubuntu-trusty64-docker_1.8.2.20150914.box"
#  config.vm.box = "ubuntu-trusty64-docker"
#  config.vm.box_url = "http://bams-sami-api.int.thomsonreuters.com/artifactory/default.vagrant.local/compass/cudl/centos-6.6-x86_64-vmware-puppet-1.0.1.box"
  config.vm.box = "centos-6.6-x86_64-vmware-puppet-1.0.1"
  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  # Provision using the shell to install fog
  config.vm.provision :shell, :inline => $script_yum


  config.vm.post_up_message = <<MSG

     The box is ready. Statsite is in /vagrant.
     When making changes to configure.ac or Makefile.am, run bootstrap.sh,
     and when you have your dependencies in order, ./configure again.

     Dependencies were already installed, they are:
     - build-essential
     - automake
     - check
     - scons
     - pytest

     To build: use make, to test: make test.


MSG

end
