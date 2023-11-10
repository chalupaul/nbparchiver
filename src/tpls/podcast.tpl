<button class="accordion">{{ title }}</button>
<div class="panel" id="{{ guid_url }}">
  <p>
    {{ pub_date }} |
    <a href="{{ link }}">Episode</a> |
    <a href="{{ mp3.local }}">MP3</a> |
    <a href="{{ transcript.local }}">Transcript</a>
  </p>
  <p>{{ description }}</p>
</div>