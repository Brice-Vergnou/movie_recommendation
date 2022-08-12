const url = "ngrok api server url"; 
const cors_url = 'heroku url to your proxy' + url

const img_1 = document.getElementById("img1");
const img_2 = document.getElementById("img2");
const img_3 = document.getElementById("img3");
const img_4 = document.getElementById("img4");
const img_5 = document.getElementById("img5");
const title_1 = document.getElementById("title1");
const title_2 = document.getElementById("title2");
const title_3 = document.getElementById("title3");
const title_4 = document.getElementById("title4");
const title_5 = document.getElementById("title5");
const year_1 = document.getElementById("year1");
const year_2 = document.getElementById("year2");
const year_3 = document.getElementById("year3");
const year_4 = document.getElementById("year4");
const year_5 = document.getElementById("year5");
const genres_1 = document.getElementById("genres1");
const genres_2 = document.getElementById("genres2");
const genres_3 = document.getElementById("genres3");
const genres_4 = document.getElementById("genres4");
const genres_5 = document.getElementById("genres5");
const overview_1 = document.getElementById("overview1");
const overview_2 = document.getElementById("overview2");
const overview_3 = document.getElementById("overview3");
const overview_4 = document.getElementById("overview4");
const overview_5 = document.getElementById("overview5");
const mean_rating_1 = document.getElementById("mean_rating1");
const mean_rating_2 = document.getElementById("mean_rating2");
const mean_rating_3 = document.getElementById("mean_rating3");
const mean_rating_4 = document.getElementById("mean_rating4");
const mean_rating_5 = document.getElementById("mean_rating5");
const movieId_1 = document.getElementById("movieId1");
const movieId_2 = document.getElementById("movieId2");
const movieId_3 = document.getElementById("movieId3");
const movieId_4 = document.getElementById("movieId4");
const movieId_5 = document.getElementById("movieId5");
const button = document.getElementById('post-btn');
var obj;

function setup(){
    fetch(url)
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => img_1.src = obj[0]["image_path"])
    .then(() => img_2.src = obj[1]["image_path"])
    .then(() => img_3.src = obj[2]["image_path"])
    .then(() => img_4.src = obj[3]["image_path"])
    .then(() => img_5.src = obj[4]["image_path"])
    .then(() => title_1.textContent = obj[0]["title"])
    .then(() => title_2.textContent = obj[1]["title"])
    .then(() => title_3.textContent = obj[2]["title"])
    .then(() => title_4.textContent = obj[3]["title"])
    .then(() => title_5.textContent = obj[4]["title"])
    .then(() => year_1.textContent = obj[0]["movie_Year"])
    .then(() => year_2.textContent = obj[1]["movie_Year"])
    .then(() => year_3.textContent = obj[2]["movie_Year"])
    .then(() => year_4.textContent = obj[3]["movie_Year"])
    .then(() => year_5.textContent = obj[4]["movie_Year"])
    .then(() => genres_1.textContent = obj[0]["genres"].join(', '))
    .then(() => genres_2.textContent = obj[1]["genres"].join(', '))
    .then(() => genres_3.textContent = obj[2]["genres"].join(', '))
    .then(() => genres_4.textContent = obj[3]["genres"].join(', '))
    .then(() => genres_5.textContent = obj[4]["genres"].join(', '))
    .then(() => overview_1.textContent = obj[0]["overview"])
    .then(() => overview_2.textContent = obj[1]["overview"])
    .then(() => overview_3.textContent = obj[2]["overview"])
    .then(() => overview_4.textContent = obj[3]["overview"])
    .then(() => overview_5.textContent = obj[4]["overview"])
    .then(() => mean_rating_1.textContent = obj[0]["mean_rating"])
    .then(() => mean_rating_2.textContent = obj[1]["mean_rating"])
    .then(() => mean_rating_3.textContent = obj[2]["mean_rating"])
    .then(() => mean_rating_4.textContent = obj[3]["mean_rating"])
    .then(() => mean_rating_5.textContent = obj[4]["mean_rating"])
    .then(() => movieId_1.textContent = obj[0]["movieId"])
    .then(() => movieId_2.textContent = obj[1]["movieId"])
    .then(() => movieId_3.textContent = obj[2]["movieId"])
    .then(() => movieId_4.textContent = obj[3]["movieId"])
    .then(() => movieId_5.textContent = obj[4]["movieId"])
}


setup()

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    } 
  });
}

button.addEventListener('click', async _ => {    
    const response = await fetch(cors_url, {
      method: 'post',
      body: JSON.stringify({
        "movie_1_rating":document.querySelector('input[name="input1"]:checked').value,
        "movie_1_id": movieId_1.textContent,
        "movie_2_rating": document.querySelector('input[name="input2"]:checked').value,
        "movie_2_id": movieId_2.textContent,
        "movie_3_rating": document.querySelector('input[name="input3"]:checked').value,
        "movie_3_id": movieId_3.textContent,
        "movie_4_rating": document.querySelector('input[name="input4"]:checked').value,
        "movie_4_id": movieId_4.textContent,
        "movie_5_rating":document.querySelector('input[name="input5"]:checked').value,
        "movie_5_id": movieId_5.textContent
    }),
      headers:{
        "Access-Control-Allow-Origin":"*",
        "Content-type": "application/json"
      }
    })
    .then(res => res.json())
    .then(data => obj = data)
    .then(() => img_1.src = obj[0]["image_path"])
    .then(() => img_2.src = obj[1]["image_path"])
    .then(() => img_3.src = obj[2]["image_path"])
    .then(() => img_4.src = obj[3]["image_path"])
    .then(() => img_5.src = obj[4]["image_path"])
    .then(() => title_1.textContent = obj[0]["title"])
    .then(() => title_2.textContent = obj[1]["title"])
    .then(() => title_3.textContent = obj[2]["title"])
    .then(() => title_4.textContent = obj[3]["title"])
    .then(() => title_5.textContent = obj[4]["title"])
    .then(() => year_1.textContent = obj[0]["movie_Year"])
    .then(() => year_2.textContent = obj[1]["movie_Year"])
    .then(() => year_3.textContent = obj[2]["movie_Year"])
    .then(() => year_4.textContent = obj[3]["movie_Year"])
    .then(() => year_5.textContent = obj[4]["movie_Year"])
    .then(() => genres_1.textContent = obj[0]["genres"].join(', '))
    .then(() => genres_2.textContent = obj[1]["genres"].join(', '))
    .then(() => genres_3.textContent = obj[2]["genres"].join(', '))
    .then(() => genres_4.textContent = obj[3]["genres"].join(', '))
    .then(() => genres_5.textContent = obj[4]["genres"].join(', '))
    .then(() => overview_1.textContent = obj[0]["overview"])
    .then(() => overview_2.textContent = obj[1]["overview"])
    .then(() => overview_3.textContent = obj[2]["overview"])
    .then(() => overview_4.textContent = obj[3]["overview"])
    .then(() => overview_5.textContent = obj[4]["overview"])
    .then(() => mean_rating_1.textContent = obj[0]["mean_rating"])
    .then(() => mean_rating_2.textContent = obj[1]["mean_rating"])
    .then(() => mean_rating_3.textContent = obj[2]["mean_rating"])
    .then(() => mean_rating_4.textContent = obj[3]["mean_rating"])
    .then(() => mean_rating_5.textContent = obj[4]["mean_rating"])
    .then(() => movieId_1.textContent = obj[0]["movieId"])
    .then(() => movieId_2.textContent = obj[1]["movieId"])
    .then(() => movieId_3.textContent = obj[2]["movieId"])
    .then(() => movieId_4.textContent = obj[3]["movieId"])
    .then(() => movieId_5.textContent = obj[4]["movieId"])
});
