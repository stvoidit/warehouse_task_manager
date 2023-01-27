<template>
    <el-menu
        :ellipsis="false"
        :router="true"
        mode="horizontal">
        <el-menu-item
            v-for="menu in routes"
            :key="menu.path"
            :route="menu.path">
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
                    <span>{{ store.currentUser?.employee_name }}</span>
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

<script lang="ts">
import { useApplicationStore } from "@/store";
import ChangePasswordDialog from "./ChangePasswordDialog.vue";
import { useRoute } from "vue-router";
import { computed } from "vue";
export default {
    components: {
        ChangePasswordDialog
    },
    setup() {
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
        return {
            store,
            handleLogOut,
            routes
        };
    }
};
</script>

<style>
.flex-grow {
    flex-grow: 1;
}
</style>
