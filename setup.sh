echo "export PYTHONPATH=~/.pip/packages" >> ~/.profile
cat > ~/.pip/pip.conf << EOF
[install]
install-option=--install-purelib=~/.pip/packages
EOF