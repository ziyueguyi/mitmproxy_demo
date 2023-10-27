bashrc="/root/.bashrc"
sed -i '/export proxy=/d' $bashrc
sed -i '/export http_proxy=$proxy/d' $bashrc
sed -i '/export https_proxy=$proxy/d' $bashrc
sed -i '/export no_proxy="localhost, 127.0.0.1, ::1"/d' $bashrc
unset http_proxy
unset https_proxy
unset no_proxy
source $bashrc

