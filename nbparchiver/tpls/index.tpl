<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
.accordion {
  background-color: #eee;
  color: #444;
  cursor: pointer;
  padding: 18px;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
  transition: 0.4s;
}

.active, .accordion:hover {
  background-color: #ccc;
}

.accordion:after {
  content: '\002B';
  color: #777;
  font-weight: bold;
  float: right;
  margin-left: 5px;
}

.active:after {
  content: "\2212";
}

.panel {
  padding: 0 18px;
  background-color: white;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}
</style>
</head>
<body>

<h2>Naked Bible Podcast Archive</h2>
<p>Below are the shows for the Naked Bible Podcast. This data has been archived and will not be updated. </p>
<p>Thank you, Dr. Heiser. We miss you.</p>
<p>You can find a playlist of all the podcasts in order <a href="content/naked_bible_podcast.m3u">here</a></p>
{% for item in items -%}
    <button class="accordion">{{ item.title }}</button>
    <div class="panel" id="{{ item.guid_url }}">
    <p>
        {{ item.pub_date }} |
        <a href="{{ item.link }}">Episode</a> |
        <a href="{{ item.mp3.local }}">MP3</a> |
        <a href="{{ item.transcript.local }}">Transcript</a>
    </p>
    <p>{{ item.description }}</p>
    </div>
{%endfor %}

<script>
var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    } 
  });
}
</script>

</body>
</html>
