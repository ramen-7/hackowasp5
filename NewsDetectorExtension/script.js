const btn1=document.getElementById("btn1");
const out1=document.getElementById("output1");
const out3=document.getElementById("output2");
var input=document.getElementById("content");
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
// var requestOptions = {
//     method: 'POST',
//     headers: myHeaders,
//     body:input.value,
//     redirect: 'follow'
// };
function fun1(){
    var r1=document.getElementById('result1');
    r1.style.setProperty('display','flex');
    console.log(input.value);
    fetch("https://api.arnav021.repl.co/predict", {
        method: 'POST',
        headers: myHeaders,
        body:input.value,
        redirect: 'follow'
    })
        .then(response => response.text())
        .then(result =>
            {
            console.log(result);
            var out2=JSON.parse(result);
            // out1.innerHTML=out2.value;
            if(out2.value<=0.4)
            {
                out1.innerHTML="HUMAN";
            }else if(out2.value>=0.6)
            {
                out1.innerHTML="MACHINE";
            }else{
                out1.innerHTML="NOT SURE";
            }
            out3.innerHTML=out2.value2;
            console.log(out2.value);
        }
            )
}

btn1.addEventListener('click',fun1);
