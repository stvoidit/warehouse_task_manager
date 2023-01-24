<template>
    <el-header>
        <el-page-header
            title="назад"
            @back="onBack">
            <template #content>
                <el-menu
                    :ellipsis="false"
                    router
                    mode="horizontal">
                    <el-menu-item
                        route="/">
                        Список задач
                    </el-menu-item>
                </el-menu>
            </template>
            <template #extra>
                <div class="flex items-center">
                    {{ store.currentUser?.employee_name }}
                    <el-button
                        size="small"
                        type="danger"
                        round
                        @click="handleLogOut">
                        выход
                    </el-button>
                </div>
            </template>
        </el-page-header>
    </el-header>
</template>

<script lang="ts">
import { useApplicationStore } from "@/store";
export default {
    setup() {
        const store = useApplicationStore();
        const onBack = () => location.href = "/";
        const handleLogOut = () => {
            window.localStorage.removeItem("token");
            location.href = "/login";
        };
        return {
            store,
            onBack,
            handleLogOut
        };
    }
};
</script>

<style>
.flex-grow {
    flex-grow: 1;
}
</style>
