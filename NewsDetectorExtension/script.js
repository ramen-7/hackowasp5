const input=document.getElementById("content");
const btn1=document.getElementById("btn1");
const out1=document.getElementById("output1");
const out3=document.getElementById("output2");
var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: input,
    redirect: 'follow'
};
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
function fun1(){
    fetch("https://api.arnav021.repl.co/predict", requestOptions)
        .then(response => response.text())
        .then(result =>
            {
            const out2=JSON.parse(result);
            out1.innerHTML=out2.value;
            out3.innerHTML=out2.value2;
            })
}

btn1.addEventListener('click',fun1);


