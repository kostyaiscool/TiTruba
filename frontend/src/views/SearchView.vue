<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import connection from "@/api";
import VideoThumbnail from "@/components/VideoThumbnail.vue";
const route = useRoute();
const router = useRouter();

const videos = ref([]);
const loading = ref(false);

const loadVideos = async () => {

    loading.value = true;

    try{

        const response = await connection.get(
    `/videos/search/${route.params.query}`
);

console.log(response.data);

videos.value = response.data;

    }catch(err){

        console.error(err);

    }finally{

        loading.value = false;

    }

}

const openVideo = (id) => {

    router.push(`/video/${id}`);

}

watch(
    () => route.params.query,
    loadVideos
);

onMounted(loadVideos);
</script>

<template>

<div class="page">

<h1>
Поиск:
"{{ route.params.query }}"
</h1>

<div
v-if="loading"
>
Загрузка...
</div>

<div
v-else-if="videos.length===0"
>
Ничего не найдено.
</div>

<div
v-else
class="videos"
>

<div
class="video"
v-for="video in videos"
:key="video.id"
@click="openVideo(video.id)"
>

<VideoThumbnail
    :video-src="`http://localhost:8000/videos/watch/${video.id}`"
/>

<div>

<h3>{{ video.public_name }}</h3>

<p>{{ video.author }}</p>

<p>👁 {{ video.views }}</p>

</div>

</div>

</div>

</div>

</template>

<style scoped>

.page{
padding:25px;
}

.videos{
display:flex;
flex-direction:column;
gap:18px;
}

.video{
display:flex;
gap:15px;
padding:15px;
background:#f5f5f5;
border-radius:15px;
cursor:pointer;
transition:.2s;
}

.video:hover{
background:#ececec;
}

.preview{
width:250px;
border-radius:10px;
}

</style>