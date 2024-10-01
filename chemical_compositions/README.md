AWS IP - http://52.66.18.249
admin pwd odoo - admin
postgresql user - odoo17
postgresql pwd - odoo17
oddo_user - info@sinsglasteel.in
odoo_pwd = shivam


Installing wkhtmltopdf
======================
`sudo su`
`cd /opt`
`wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz`
`tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz`
`mv wkhtmltox/bin/wkhtmlto* /usr/bin/`

$ wkhtmltopdf --version
wkhtmltopdf 0.12.3 (with patched qt)

###### That's it

# More over.....

#for debian stretch version
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.stretch_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.stretch_amd64.deb


# for other
https://github.com/wkhtmltopdf/wkhtmltopdf/releases/0.12.5











# long way procedue if above not works 
# How to Fix it:
#################


1. Remove wkhtmltopdf and related package
$ sudo apt-get remove libqt4-dev qt4-dev-tools wkhtmltopdf

$ sudo apt-get autoremove

2. Install requirement package for compiling
$ sudo apt-get install openssl build-essential libssl-dev libxrender-dev git-core libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig -y

3. Clone from git wkhtmltopdf and qt source
$ git clone git://github.com/wkhtmltopdf/wkhtmltopdf.git wkhtmltopdf

$ mkdir qt-wkhtmltopdf && cd qt-wkhtmltopdf

$ git clone https://www.github.com/wkhtmltopdf/qt --depth 1 --branch wk_4.8.7 --single-branch .

4. Compile qt
$ sudo ./configure -nomake tools,examples,demos,docs,translations -opensource -prefix "`pwd`" `cat ../wkhtmltopdf/static_qt_conf_base ../wkhtmltopdf/static_qt_conf_linux | sed -re '/^#/ d' | tr '\n' ' '`

$ sudo make -j3

$ sudo make install

5. Compile wkhtmltopdf
$ cd ../wkhtmltopdf

$ sudo ../qt-wkhtmltopdf/bin/qmake

$ sudo make -j3

$ sudo make install

6. Reboot
$ sudo reboot













#http://www.grobak.net/id/blog/how-fix-wkhtmltopdf-failed-error-code-6