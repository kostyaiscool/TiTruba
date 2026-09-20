<script setup>
import {
  ref,
  computed,
  onMounted,
  onUnmounted,
} from "vue";

import connection from "@/api";

const props = defineProps({
  videoId: {
    type: [String, Number],
    required: true,
  },
});

/*
|--------------------------------------------------------------------------
| Пользователь
|--------------------------------------------------------------------------
*/

const currentUser = ref(
  localStorage.getItem("username")
);

/*
|--------------------------------------------------------------------------
| Подписка
|--------------------------------------------------------------------------
*/

const isSubscribed = ref(false);

/*
|--------------------------------------------------------------------------
| Рейтинг
|--------------------------------------------------------------------------
*/

const likes = ref(0);
const dislikes = ref(0);

/*
|--------------------------------------------------------------------------
| Информация о видео
|--------------------------------------------------------------------------
*/

const videoInfo = ref({
  title: "",
  description: "",
  author: "",
  views: 0,
  created_at: null,
});

/*
|--------------------------------------------------------------------------
| Видео
|--------------------------------------------------------------------------
*/

const videoUrl = computed(() => {
  return `http://localhost:8000/videos/watch/${props.videoId}`;
});

const isOwnChannel = computed(() => {
  return (
    currentUser.value &&
    videoInfo.value.author &&
    currentUser.value === videoInfo.value.author
  );
});

/*
|--------------------------------------------------------------------------
| Просмотр видео
|--------------------------------------------------------------------------
|
| Мы храним интервалы реально просмотренного видео.
|
| Например:
|
| 0 -> 10
| 10 -> 20
| перемотка -> 100
| 100 -> 110
|
| Результат:
|
| 0-20 + 100-110 = 30 секунд
|
| Перемотка вперед не считается просмотром.
|--------------------------------------------------------------------------
*/

const watchedIntervals = ref([]);

const lastVideoTime = ref(0);
const isVideoInitialized = ref(false);

/*
|--------------------------------------------------------------------------
| Добавление просмотренного интервала
|--------------------------------------------------------------------------
*/

const addWatchedInterval = (start, end) => {
  if (end <= start) {
    return;
  }

  watchedIntervals.value.push({
    start,
    end,
  });

  /*
  |--------------------------------------------------------------------------
  | Объединяем пересекающиеся интервалы
  |--------------------------------------------------------------------------
  */

  const intervals = [...watchedIntervals.value]
    .sort((a, b) => a.start - b.start);

  const merged = [];

  for (const interval of intervals) {
    const last = merged[merged.length - 1];

    if (!last || interval.start > last.end) {
      merged.push({
        start: interval.start,
        end: interval.end,
      });
    } else {
      last.end = Math.max(
        last.end,
        interval.end
      );
    }
  }

  watchedIntervals.value = merged;
};

/*
|--------------------------------------------------------------------------
| Получение общего количества реально просмотренных секунд
|--------------------------------------------------------------------------
*/

const getWatchedSeconds = () => {
  return watchedIntervals.value.reduce(
    (total, interval) => {
      return total + (interval.end - interval.start);
    },
    0
  );
};

/*
|--------------------------------------------------------------------------
| Отслеживание времени видео
|--------------------------------------------------------------------------
*/

const updateWatchTime = (event) => {
  const currentTime = event.target.currentTime;

  if (!isVideoInitialized.value) {
    lastVideoTime.value = currentTime;
    isVideoInitialized.value = true;
    return;
  }

  /*
  |--------------------------------------------------------------------------
  | Нормальное воспроизведение
  |--------------------------------------------------------------------------
  |
  | Если время увеличилось незначительно,
  | считаем этот интервал просмотренным.
  |
  */

  if (currentTime > lastVideoTime.value) {
    const difference =
      currentTime - lastVideoTime.value;

    /*
    |--------------------------------------------------------------------------
    | Защита от перемотки вперед
    |--------------------------------------------------------------------------
    |
    | timeupdate обычно вызывается несколько раз в секунду.
    | Если скачок слишком большой, скорее всего пользователь перемотал видео.
    |
    */

    if (difference <= 2) {
      addWatchedInterval(
        lastVideoTime.value,
        currentTime
      );
    }
  }

  lastVideoTime.value = currentTime;
};

/*
|--------------------------------------------------------------------------
| Отправка просмотра
|--------------------------------------------------------------------------
*/

const sendWatched = async () => {
  const watchedSeconds = getWatchedSeconds();

  console.log(
    "Отправляем просмотр:",
    watchedSeconds,
    "секунд"
  );

  /*
  |--------------------------------------------------------------------------
  | Ничего не отправляем, если видео фактически не смотрели
  |--------------------------------------------------------------------------
  */

  if (watchedSeconds <= 0) {
    console.log(
      "Видео фактически не смотрели"
    );

    return;
  }

  const token =
    localStorage.getItem("token");

  /*
  |--------------------------------------------------------------------------
  | Пользователь не авторизован
  |--------------------------------------------------------------------------
  */

  if (!token) {
    console.log(
      "Пользователь не авторизован, просмотр не отправляется"
    );

    return;
  }

  try {
    const response = await fetch(
      `http://localhost:8000/videos/watched/${props.videoId}`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },

        body: JSON.stringify({
          watched_seconds: watchedSeconds,
        }),

        /*
        |--------------------------------------------------------------------------
        | Очень важно при уходе со страницы
        |--------------------------------------------------------------------------
        |
        | Браузер постарается завершить запрос,
        | даже если страница закрывается.
        |
        */

        keepalive: true,
      }
    );

    console.log(
      "watched status:",
      response.status
    );

    /*
    |--------------------------------------------------------------------------
    | Не обязательно читать response body.
    |--------------------------------------------------------------------------
    */

    if (!response.ok) {
      console.error(
        "Ошибка сохранения просмотра:",
        response.status
      );

      return;
    }

    console.log(
      "Просмотр успешно сохранён"
    );

  } catch (err) {
    /*
    |--------------------------------------------------------------------------
    | Ошибка сети не должна ломать приложение
    |--------------------------------------------------------------------------
    */

    console.error(
      "Ошибка отправки watched:",
      err
    );
  }
};

/*
|--------------------------------------------------------------------------
| Защита от повторной отправки
|--------------------------------------------------------------------------
*/

let watchedSent = false;

const sendWatchedOnce = () => {
  if (watchedSent) {
    return;
  }

  watchedSent = true;

  /*
  |--------------------------------------------------------------------------
  | Намеренно не await.
  |
  | Компонент/страница уже покидается.
  |--------------------------------------------------------------------------
  */

  void sendWatched();
};

/*
|--------------------------------------------------------------------------
| Отслеживание ухода со страницы /watch
|--------------------------------------------------------------------------
|
| Важно:
|
| Мы не просто полагаемся на onUnmounted.
| Проверяем текущий URL.
|
| Если компонент будет размонтирован по другой причине,
| просмотр не отправится.
|--------------------------------------------------------------------------
*/

const handleBeforeUnload = () => {
  sendWatchedOnce();
};

/*
|--------------------------------------------------------------------------
| Информация о видео
|--------------------------------------------------------------------------
*/

const loadVideoInfo = async () => {
  try {
    const response =
      await connection.get(
        `/videos/video_info/${props.videoId}`
      );

    videoInfo.value =
      response.data;

  } catch (err) {
    console.error(
      "Ошибка загрузки информации о видео:",
      err
    );
  }
};

/*
|--------------------------------------------------------------------------
| Подписка
|--------------------------------------------------------------------------
*/

const loadSubscription = async () => {
  /*
  |--------------------------------------------------------------------------
  | Пока автор видео неизвестен,
  | запрос отправлять нельзя.
  |--------------------------------------------------------------------------
  */

  if (!videoInfo.value.author) {
    return;
  }

  try {
    const response =
      await connection.get(
        `/subscribers/status/${videoInfo.value.author}`
      );

    isSubscribed.value =
      response.data.subscribed;

  } catch (err) {
    if (err.response?.status !== 401) {
      console.error(
        "Ошибка проверки подписки:",
        err
      );
    }

    isSubscribed.value = false;
  }
};

const toggleSubscribe = async () => {
  try {
    if (isOwnChannel.value) {
      return;
    }

    const response =
      await connection.post(
        `/subscribers/subscribe/${videoInfo.value.author}`
      );

    isSubscribed.value =
      response.data.subscribed;

  } catch (err) {
    console.error(
      "Ошибка подписки:",
      err
    );
  }
};

/*
|--------------------------------------------------------------------------
| Лайки
|--------------------------------------------------------------------------
*/

const loadRating = async () => {
  try {
    const response =
      await connection.get(
        `/likes/rating/${props.videoId}`
      );

    likes.value =
      response.data.likes;

    dislikes.value =
      response.data.dislikes;

  } catch (err) {
    console.error(
      "Ошибка загрузки рейтинга:",
      err
    );
  }
};

const likeVideo = async () => {
  try {
    await connection.post(
      `/likes/like/${props.videoId}`
    );

    await loadRating();

  } catch (err) {
    console.error(
      "Ошибка лайка:",
      err
    );
  }
};

const dislikeVideo = async () => {
  try {
    await connection.post(
      `/likes/dislike/${props.videoId}`
    );

    await loadRating();

  } catch (err) {
    console.error(
      "Ошибка дизлайка:",
      err
    );
  }
};

/*
|--------------------------------------------------------------------------
| Lifecycle
|--------------------------------------------------------------------------
*/

onMounted(async () => {
  console.log(
    "VideoPlayer mounted:",
    props.videoId
  );

  /*
  |--------------------------------------------------------------------------
  | Отслеживаем закрытие/уход со страницы
  |--------------------------------------------------------------------------
  */

  window.addEventListener(
    "beforeunload",
    handleBeforeUnload
  );

  /*
  |--------------------------------------------------------------------------
  | Загружаем информацию о видео
  |--------------------------------------------------------------------------
  */

  await loadVideoInfo();

  /*
  |--------------------------------------------------------------------------
  | Теперь автор уже известен
  |--------------------------------------------------------------------------
  */

  await loadSubscription();

  /*
  |--------------------------------------------------------------------------
  | Загружаем рейтинг
  |--------------------------------------------------------------------------
  */

  await loadRating();
});

onUnmounted(() => {
  console.log(
    "VideoPlayer unmounted"
  );

  window.removeEventListener(
    "beforeunload",
    handleBeforeUnload
  );

  /*
  |--------------------------------------------------------------------------
  | Проверяем, действительно ли мы покидаем /watch
  |--------------------------------------------------------------------------
  |
  | Это важно для Vue Router.
  |
  | Если компонент размонтировался по другой причине,
  | запрос не отправляем.
  |
  */

  const currentPath =
    window.location.pathname;

  const isWatchPage =
    currentPath.startsWith("/watch");

  if (isWatchPage) {
    console.log(
      "Остались на странице /watch — просмотр пока не отправляем"
    );

    return;
  }

  console.log(
    "Пользователь покинул /watch — отправляем просмотр"
  );

  sendWatchedOnce();
});
</script>

<template>
  <div class="video-wrapper">

    <video
      class="video-player"
      controls
      autoplay
      @timeupdate="updateWatchTime"
    >
      <source
        :src="videoUrl"
        type="video/mp4"
      />
    </video>

    <h1 class="video-title">
      {{ videoInfo.title }}
    </h1>

    <div class="video-stats">

      <span>
        👁
        {{ videoInfo.views }}
        просмотров
      </span>

      <span>
        📅
        {{
          videoInfo.created_at
            ? new Date(
                videoInfo.created_at
              ).toLocaleDateString()
            : ""
        }}
      </span>

    </div>

    <div class="rating-panel">

      <button
        class="like-btn"
        @click="likeVideo"
      >
        👍 {{ likes }}
      </button>

      <button
        class="dislike-btn"
        @click="dislikeVideo"
      >
        👎 {{ dislikes }}
      </button>

    </div>

    <div class="video-meta">

      <div class="author-info">

        <div class="avatar">
          {{
            videoInfo.author?.[0]
              ?.toUpperCase()
          }}
        </div>

        <div>

          <div class="author-name">
            {{ videoInfo.author }}
          </div>

          <div class="subscribers">
            channel
          </div>

        </div>

      </div>

      <button
        v-if="!isOwnChannel"
        class="subscribe-btn"
        :class="{
          subscribed: isSubscribed
        }"
        @click="toggleSubscribe"
      >
        {{
          isSubscribed
            ? "Subscribed"
            : "Subscribe"
        }}
      </button>

    </div>

    <div class="description-box">

      <h3>
        Описание
      </h3>

      <p>
        {{
          videoInfo.description ||
          "Описание отсутствует"
        }}
      </p>

    </div>

  </div>
</template>

<style scoped>
.video-wrapper {
  width: 100%;
}

.video-player {
  width: 100%;
  max-height: 700px;

  border-radius: 16px;
  background: black;
}

.video-title {
  margin-top: 16px;

  font-size: 24px;
  font-weight: bold;
}

.video-stats {
  margin-top: 8px;

  display: flex;
  gap: 18px;

  color: #777;
}

.rating-panel {
  display: flex;
  gap: 12px;

  margin-top: 16px;
}

.like-btn,
.dislike-btn {
  border: none;
  border-radius: 999px;

  padding: 10px 18px;

  cursor: pointer;
  font-weight: bold;
}

.like-btn {
  background: #e8ffe8;
}

.dislike-btn {
  background: #ffe8e8;
}

.video-meta {
  margin-top: 24px;

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 48px;
  height: 48px;

  border-radius: 50%;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 20px;
  font-weight: bold;
}

.author-name {
  font-size: 16px;
  font-weight: bold;
}

.subscribers {
  color: #777;
  font-size: 13px;
}

.subscribe-btn {
  padding: 10px 18px;

  border: none;
  border-radius: 999px;

  background: red;
  color: white;

  cursor: pointer;
  font-weight: bold;
}

.subscribe-btn.subscribed {
  background: #ddd;
  color: #333;
}

.description-box {
  margin-top: 24px;

  background: #f5f5f5;

  padding: 16px;

  border-radius: 12px;
}

.description-box h3 {
  margin-bottom: 10px;
}
</style>