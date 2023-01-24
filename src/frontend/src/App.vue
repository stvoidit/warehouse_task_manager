<template>
    <HeaderApp v-if="store.isAuth" />
    <router-view
        v-slot="{ Component }">
        <component :is="Component" />
    </router-view>
</template>
<script lang="ts">
import HeaderApp from "@/components/HeaderApp.vue";
import { useApplicationStore } from "@/store";
export default {
    components: {
        HeaderApp
    },
    setup() {
        const store = useApplicationStore();
        return {
            store
        };
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
