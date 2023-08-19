<template>
    <el-header v-if="store.isAuth">
        <HeaderApp />
    </el-header>
    <router-view
        v-slot="{ Component }">
        <el-main>
            <component :is="Component" />
        </el-main>
    </router-view>
</template>
<script setup lang="ts">
import HeaderApp from "@/components/HeaderApp.vue";
import { useApplicationStore } from "@/store";
const store = useApplicationStore();
</script>
<style lang="scss">
@import "element-plus/dist/index.css";
@import "@/styles.css";
</style>
