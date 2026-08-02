<script setup>
import {ref,onMounted} from "vue";
import {useRouter} from "vue-router";
import connection from "@/api";
import VideoThumbnail from "@/components/VideoThumbnail.vue";
const router = useRouter();

const videos = ref([]);

const loading = ref(true);

const load = async () => {

    try{

        const response =
            await connection.get("/likes/dislikes");

        videos.value =
            response.data;

    }catch(e){

        console.error(e);

    }finally{

        loading.value=false;

    }

}

const openVideo=(id)=>{

    router.push(`/video/${id}`);

}

onMounted(load);
</script>

<template>

<div class="page">

<h1>Не понравившиеся</h1>

<div
v-if="loading"
>
Загрузка...
</div>

<div
v-else-if="videos.length===0"
>
Вы ещё ничего не дизлайкнули.
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

<div class="info">

<h3>
{{video.public_name}}
</h3>

<p>
{{video.author}}
</p>

<p>
👁 {{video.views}}
</p>

</div>

</div>

</div>

</div>

</template>

<style scoped>

.page{

padding:30px;

}

.videos{

display:flex;

flex-direction:column;

gap:20px;

}

.video{

display:flex;

gap:18px;

padding:15px;

border-radius:15px;

background:#f5f5f5;

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

.info{

display:flex;

flex-direction:column;

justify-content:center;

}

</style>