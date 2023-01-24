<template>
    <HeaderApp />
    <router-view
        v-slot="{ Component }">
        <component :is="Component" />
    </router-view>
</template>
<script lang="ts">
import { ref } from "vue";
import HeaderApp from "@/components/HeaderApp.vue";
export default {
    components: {
        HeaderApp
    },
    setup() {

    }
};
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
</style>
