<template>
    <el-menu
        :ellipsis="false"
        :router="true"
        mode="horizontal">
        <el-menu-item
            v-for="menu in routes"
            :key="menu.label"
            :index="menu.label"
            :route="menu">
            <el-icon>
                <MessageBox v-if="menu.icon === 'MessageBox'" />
                <Guide v-if="menu.icon === 'Guide'" />
            </el-icon>
            <span>{{ menu.label }}</span>
        </el-menu-item>
        <div class="flex-grow" />
        <el-popover
            trigger="click"
            :width="300"
            popper-style="box-shadow: rgb(14 18 22 / 35%) 0px 10px 38px -10px, rgb(14 18 22 / 20%) 0px 10px 20px -15px; padding: 20px;">
            <template #reference>
                <el-button
                    style="margin-top: 0.5rem;"
                    plain
                    round>
                    <el-icon style="vertical-align: middle">
                        <User />
                    </el-icon>
                    <span v-if="isLandscape">{{ store.currentUser?.employee_name }} </span>
                </el-button>
            </template>
            <template #default>
                <el-row :gutter="0">
                    <el-col :span="12">
                        <div><b>ID:</b> {{ store.currentUser?.id }}</div>
                    </el-col>
                    <el-col :span="12">
                        <div><b>Логин:</b> {{ store.currentUser?.login }}</div>
                    </el-col>
                </el-row>
                <el-row class="mt">
                    <el-col :span="12">
                        <el-button
                            size="small"
                            type="danger"
                            round
                            @click="handleLogOut">
                            выход
                        </el-button>
                    </el-col>
                    <el-col :span="12">
                        <ChangePasswordDialog />
                    </el-col>
                </el-row>
            </template>
        </el-popover>
    </el-menu>
</template>

<script setup lang="ts">
import { useApplicationStore } from "@/store";
import ChangePasswordDialog from "./ChangePasswordDialog.vue";
import { useRoute } from "vue-router";
import { computed, ref, onMounted } from "vue";

const store = useApplicationStore();
const handleLogOut = () => store.logOut();
const route = useRoute();
const routes = computed(() => {
    const menuRoutes = [
        {
            label: "Список складов",
            path: "/",
            icon: "Guide"
        }
    ];
    if (route.params.stockID) {
        menuRoutes.push({
            label: "Список задач",
            path: `/stock/${route.params.stockID}`,
            icon: "MessageBox"
        });
    }
    return menuRoutes;
});

const orientation = ref("landscape-primary");
const isLandscape = computed(() => orientation.value === "landscape-primary");
onMounted(() => {
    try {
        orientation.value = screen.orientation.type;
        window.addEventListener("orientationchange", () => {
            orientation.value = screen.orientation.type;
        }, false);
    } catch (error) {
        console.warn(error);
    }
});
</script>

<style>
.flex-grow {
    flex-grow: 1;
}
</style>
