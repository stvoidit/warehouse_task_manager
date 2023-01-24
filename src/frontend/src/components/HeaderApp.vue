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
                <el-popover
                    trigger="click"
                    :width="300"
                    popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;">
                    <template #reference>
                        <el-button
                            plain
                            round>
                            {{ store.currentUser?.employee_name }}
                        </el-button>
                    </template>
                    <template #default>
                        <el-row>
                            <el-col>
                                <div><b>ID:</b> {{ store.currentUser?.id }}</div>
                                <div><b>Логин:</b> {{ store.currentUser?.login }}</div>
                                <div class="mt">
                                    <el-button
                                        size="small"
                                        type="danger"
                                        round
                                        @click="handleLogOut">
                                        выход
                                    </el-button>
                                </div>
                            </el-col>
                        </el-row>
                    </template>
                </el-popover>
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
.el-page-header__back {
    display: none;
}
.el-divider.el-divider--vertical {
    display: none;
}
</style>
