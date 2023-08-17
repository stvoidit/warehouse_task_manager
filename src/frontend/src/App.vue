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
<style>
.mt {
    margin-top: 1rem;
}
.mb {
    margin-bottom: 1rem;
}
body {
    background-color: var(--el-fill-color-blank);
}
.el-table .cell {
    word-break: break-word !important;
    text-overflow: initial !important;
}
.text-center {
    text-align: center;
}
.el-table__row {
    cursor: pointer;
}
.el-table thead {
    color: black !important;
}
</style>
