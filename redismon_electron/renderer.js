const electron = require('electron');
const {ipcRenderer} = electron;

const submitFormButton = docuemnt.queryySelector("#redisAddressForm")

submitFormButton.addEventListener("submit", function(e) {
    e.preventDefault();
    console.log("sended redisAddressForm")
//    ipcRenderer.send('redisAddressSubmit', document.getElementById('redisAddressText').value);
});
