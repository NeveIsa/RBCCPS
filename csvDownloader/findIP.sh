curl https://dweet.io/get/latest/dweet/for/rbccpsIP > .tempIP
cat .tempIP | grep -Po "\d+\.\d+\.\d+\.\d+"
rm .tempIP
