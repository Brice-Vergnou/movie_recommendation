const img_1 = document.getElementById("img1");
const img_2 = document.getElementById("img2");
var obj;

function setup(){
    fetch('http://127.0.0.1:8000/')
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => img_1.src = obj[0]["image_path"])
    .then(() => img_2.src = obj[1]["image_path"])
}


setup()