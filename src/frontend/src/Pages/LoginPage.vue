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
                    ref="ruleFormRef"
                    label-position="right"
                    label-width="100px"
                    :model="loginForm"
                    :rules="rules"
                    status-icon
                    style="max-width: 460px">
                    <el-form-item
                        label="Логин"
                        prop="login">
                        <el-input
                            v-model="loginForm.login"
                            type="text" />
                    </el-form-item>
                    <el-form-item
                        label="Пароль"
                        prop="password">
                        <el-input
                            v-model="loginForm.password"
                            type="password" />
                    </el-form-item>
                    <el-form-item>
                        <el-button
                            type="success"
                            @click="handleLogin">
                            Войти
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { useApplicationStore } from "@/store";
import { ElMessageBox } from "element-plus";
export default defineComponent({
    setup() {
        const ruleFormRef = ref();
        const loginForm = reactive({
            login: "",
            password: ""
        });
        const rules = {
            login: {
                required: true, message: 'Поле "логин" обязательно к заполнению', trigger: "blur"
            },
            password: {
                required: true, message: 'Поле "пароль" обязательно к заполнению', trigger: "blur"
            }
        };
        const store = useApplicationStore();
        const handleLogin = async () => {
            if (!ruleFormRef.value) return;
            if (await ruleFormRef.value.validate(valid => valid) === false) return;
            store.doLogin(loginForm).catch(error => {
                if (!ruleFormRef.value) return;
                ruleFormRef.value.resetFields();
                ElMessageBox.alert(error, "Ошибка", {
                    confirmButtonText: "OK"
                });
            });
        };
        return {
            loginForm,
            handleLogin,
            ruleFormRef,
            rules

        };
    }
});
</script>
