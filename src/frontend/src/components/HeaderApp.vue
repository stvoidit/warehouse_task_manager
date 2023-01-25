<template>
    <el-header>
        <el-page-header>
            <template #content>
                <el-menu
                    :ellipsis="false"
                    :router="true"
                    mode="horizontal">
                    <el-menu-item
                        route="/">
                        <el-icon><MessageBox /></el-icon>
                        <span>Список задач</span>
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
            </template>
        </el-page-header>
    </el-header>
</template>

<script lang="ts">
import { useApplicationStore } from "@/store";
import ChangePasswordDialog from "./ChangePasswordDialog.vue";
export default {
    components: {
        ChangePasswordDialog
    },
    setup() {
        const store = useApplicationStore();
        const handleLogOut = () => store.logOut();
        return {
            store,
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
