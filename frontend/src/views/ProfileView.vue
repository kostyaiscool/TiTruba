<script setup>
import { ref, watch } from "vue";
import { useAuth } from "@/composables/useAuth";
import connection from "@/api";

const { user } = useAuth();

const videos = ref([]);
const loading = ref(false);

const editingVideo = ref(null);

const editTitle = ref("");
const editDescription = ref("");

const loadVideos = async () => {
  if (!user.value?.id) return;

  loading.value = true;

  try {
    const response = await connection.get(
      `/videos/get_video_by_author/${user.value.id}`
    );

    videos.value = response.data;

  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

watch(
  () => user.value,
  () => {
    loadVideos();
  },
  { immediate: true }
);

const deleteVideo = async (id) => {
  if (!confirm("Удалить видео?"))
    return;

  try {

    await connection.delete(
      `/videos/delete/${id}`
    );

    videos.value = videos.value.filter(
      video => video.id !== id
    );

  } catch (e) {
    console.error(e);
  }
};

const openEditor = (video) => {

  editingVideo.value = video;

  editTitle.value = video.public_name;

  editDescription.value = video.desc;

};

const saveVideo = async () => {

  try {

    await connection.patch(
      `/videos/edit_video/${editingVideo.value.id}`,
      null,
      {
        params: {
          title: editTitle.value,
          description: editDescription.value
        }
      }
    );

    editingVideo.value.public_name =
      editTitle.value;

    editingVideo.value.desc =
      editDescription.value;

    editingVideo.value = null;

  } catch (e) {

    console.error(e);

  }

};

const cancelEdit = () => {
  editingVideo.value = null;
};
</script>

<template>
<div class="profile-page">

<div class="profile-card">

<div class="avatar">
{{ user?.username?.[0]?.toUpperCase() || "U" }}
</div>

<h2 class="username">
{{ user?.username }}
</h2>

<p class="email">
{{ user?.email }}
</p>

<div class="stats">

<div class="stat">
<span class="number">
{{ videos.length }}
</span>
<span class="label">
Videos
</span>
</div>

<div class="stat">
<span class="number">
0
</span>
<span class="label">
Subscribers
</span>
</div>

</div>

<div class="actions">

<button class="btn ghost">
Edit profile
</button>

<button class="btn danger">
Delete account
</button>

</div>

</div>

<h2 class="videos-title">
Ваши видео
</h2>

<div
v-if="loading"
>
Загрузка...
</div>

<div
v-else-if="videos.length===0"
>
У вас пока нет видео.
</div>

<div
v-else
class="videos"
>

<div
v-for="video in videos"
:key="video.id"
class="video-card"
>

<img
src="https://placehold.co/320x180"
class="preview"
/>

<div class="info">

<h3>
{{ video.public_name }}
</h3>

<p>
{{ video.desc }}
</p>

<p>
👁 {{ video.views }}
</p>

</div>

<div class="buttons">

<button
class="edit"
@click="openEditor(video)"
>
Редактировать
</button>

<button
class="delete"
@click="deleteVideo(video.id)"
>
Удалить
</button>

</div>

</div>

</div>

<div
v-if="editingVideo"
class="editor"
>

<h2>
Редактирование
</h2>

<input
v-model="editTitle"
placeholder="Название"
/>

<textarea
v-model="editDescription"
placeholder="Описание"
/>

<div class="editor-buttons">

<button
class="edit"
@click="saveVideo"
>
Сохранить
</button>

<button
class="delete"
@click="cancelEdit"
>
Отмена
</button>

</div>

</div>

</div>
</template>

<style scoped>

.profile-page{
padding:40px;
background:#f9f9f9;
min-height:100vh;
}

.profile-card{
max-width:500px;
margin:auto;
background:white;
padding:24px;
border-radius:16px;
text-align:center;
box-shadow:0 8px 24px rgba(0,0,0,.1);
}

.avatar{
width:80px;
height:80px;
border-radius:50%;
background:red;
color:white;
display:flex;
justify-content:center;
align-items:center;
font-size:32px;
margin:auto;
}

.stats{
display:flex;
justify-content:space-around;
margin:20px 0;
}

.actions{
display:flex;
gap:10px;
}

.btn{
flex:1;
padding:10px;
border:none;
border-radius:8px;
cursor:pointer;
}

.ghost{
background:#eee;
}

.danger{
background:#f00;
color:white;
}

.videos-title{
margin-top:40px;
text-align:center;
}

.videos{
margin-top:20px;
display:flex;
flex-direction:column;
gap:20px;
}

.video-card{
display:flex;
gap:20px;
background:white;
padding:15px;
border-radius:12px;
align-items:center;
}

.preview{
width:220px;
border-radius:10px;
}

.info{
flex:1;
}

.buttons{
display:flex;
flex-direction:column;
gap:10px;
}

.edit{
background:#2196f3;
color:white;
border:none;
padding:10px;
border-radius:8px;
cursor:pointer;
}

.delete{
background:#f44336;
color:white;
border:none;
padding:10px;
border-radius:8px;
cursor:pointer;
}

.editor{
margin-top:40px;
background:white;
padding:20px;
border-radius:12px;
}

.editor input,
.editor textarea{
width:100%;
padding:10px;
margin-bottom:15px;
}

.editor-buttons{
display:flex;
gap:10px;
}

</style>