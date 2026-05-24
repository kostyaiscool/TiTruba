<!-- src/views/SubscriptionsView.vue -->

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

import connection from "@/api";

const router = useRouter();

const subscriptions = ref([]);

const loading = ref(true);
const error = ref(null);

/*
  📥 загрузка подписок
*/
const loadSubscriptions = async () => {
  try {
    const response = await connection.get(
      "/subscribers/get_subscribers"
    );

    subscriptions.value = response.data;

    console.log(subscriptions.value);

  } catch (err) {
    console.error(err);

    error.value =
      "Ошибка загрузки подписок";

  } finally {
    loading.value = false;
  }
};

/*
  👇 переход на страницу канала
*/
const openChannel = (userId) => {
  router.push(`/channel/${userId}`);
};

onMounted(loadSubscriptions);
</script>

<template>
  <div class="subscriptions-page">

    <h1 class="page-title">
      Subscriptions
    </h1>

    <!-- ⏳ loading -->
    <div
      v-if="loading"
      class="status"
    >
      Loading...
    </div>

    <!-- ❌ error -->
    <div
      v-else-if="error"
      class="status error"
    >
      {{ error }}
    </div>

    <!-- 📭 empty -->
    <div
      v-else-if="subscriptions.length === 0"
      class="status"
    >
      No subscriptions yet
    </div>

    <!-- 📃 list -->
    <div
      v-else
      class="subscriptions-list"
    >

      <div
        v-for="sub in subscriptions"
        :key="sub.id"
        class="subscription-card"
        @click="
          openChannel(
            sub.subscribed_to_id
          )
        "
      >

        <!-- 👤 avatar -->
        <div class="avatar">
          {{
            sub.subscribed_to_id
          }}
        </div>

        <!-- ℹ️ info -->
        <div class="subscription-info">

          <div class="UserId">
            Channel #{{ sub.subscribed_to_id }}
          </div>

          <div class="subtitle">
            channel
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<style scoped>
.subscriptions-page {
  padding: 24px;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 24px;
}

.subscriptions-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* card */
.subscription-card {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 14px;

  border-radius: 14px;

  background: #f7f7f7;

  transition: 0.2s;

  cursor: pointer;
}

.subscription-card:hover {
  background: #ececec;
}

/* avatar */
.avatar {
  width: 52px;
  height: 52px;

  border-radius: 50%;

  background: red;
  color: white;

  display: flex;
  align-items: center;
  justify-content: center;

  font-size: 18px;
  font-weight: bold;
}

/* info */
.UserId {
  font-size: 17px;
  font-weight: bold;
}

.subtitle {
  font-size: 13px;
  color: #777;
}

/* states */
.status {
  padding: 40px;
  text-align: center;
}

.error {
  color: red;
}
</style>