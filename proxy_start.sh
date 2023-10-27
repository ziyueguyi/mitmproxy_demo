bashrc="/root/.bashrc"
sed -i '$a export proxy="http://127.0.0.1:8080"' $bashrc
sed -i '$a export http_proxy=$proxy' $bashrc
sed -i '$a export https_proxy=$proxy' $bashrc
sed -i '$a export no_proxy="localhost, 127.0.0.1, ::1"' $bashrc
source $bashrc

