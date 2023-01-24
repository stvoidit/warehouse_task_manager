<template>
    <el-row
        style="margin-top: 30vh;"
        justify="center"
        align="middle">
        <el-col
            class="grid-content"
            :span="8">
            <el-card>
                <el-form
                    label-position="right"
                    label-width="100px"
                    :model="loginForm"
                    style="max-width: 460px">
                    <el-form-item label="Логин">
                        <el-input
                            v-model="loginForm.login"
                            type="text" />
                    </el-form-item>
                    <el-form-item label="Пароль">
                        <el-input
                            v-model="loginForm.password"
                            type="password" />
                    </el-form-item>
                    <el-button
                        type="success"
                        @click="handleLogin">
                        Войти
                    </el-button>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, reactive } from "vue";
import { useApplicationStore } from "@/store";
import { ElMessageBox } from "element-plus";
export default defineComponent({
    setup () {
        const loginForm = reactive({
            login: "",
            password: ""
        });
        const store = useApplicationStore();
        const handleLogin = () => store.doLogin(loginForm).catch(error => {
            loginForm.login = "";
            loginForm.password = "";
            ElMessageBox.alert(error, "Ошибка", {
                confirmButtonText: "OK"
            });
        });
        return {
            loginForm,
            handleLogin
        };
    }
});
</script>
