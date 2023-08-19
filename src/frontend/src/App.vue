<template>
    <el-header v-if="isAuth">
        <HeaderApp />
    </el-header>
    <el-main>
        <router-view
            v-slot="{ Component }">
            <component :is="Component" />
        </router-view>
    </el-main>
</template>
<script setup lang="ts">
import HeaderApp from "@/components/HeaderApp.vue";
import useApplicationStore from "@/store";
import { storeToRefs} from "pinia";
const { isAuth } = storeToRefs(useApplicationStore());
</script>
<style lang="scss">
@import "element-plus/dist/index.css";
@import "@/styles.css";
</style>
