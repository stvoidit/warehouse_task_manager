<template>
    <el-row
        style="margin-top: 20vh;"
        justify="center">
        <el-col
            class="grid-content"
            :sm="8"
            :md="8"
            :lg="8"
            :span="18">
            <el-card>
                <el-form
                    ref="ruleFormRef"
                    label-position="right"
                    :model="loginForm"
                    :rules="rules"
                    status-icon>
                    <el-form-item
                        :label-width="60"
                        label="Логин"
                        prop="login">
                        <el-input
                            v-model="loginForm.login"
                            type="text" />
                    </el-form-item>
                    <el-form-item
                        :label-width="60"
                        label="Пароль"
                        prop="password">
                        <el-input
                            v-model="loginForm.password"
                            type="password" />
                    </el-form-item>
                    <el-form-item>
                        <el-button
                            class="mt"
                            type="success"
                            @click="handleLogin"
                            @keydown.enter="handleLogin">
                            Войти
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import { defineComponent, reactive, ref, onMounted, onBeforeUnmount } from "vue";
import { useApplicationStore } from "@/store";
import { ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
export default defineComponent({
    setup() {
        /** ссылка на HTML элемент формы */
        const ruleFormRef = ref();
        /** данные формы */
        const loginForm = reactive({
            login: "",
            password: ""
        });
        /** правила проверки формы */
        const rules = {
            login: {
                required: true, message: 'Поле "логин" обязательно к заполнению', trigger: "blur"
            },
            password: {
                required: true, message: 'Поле "пароль" обязательно к заполнению', trigger: "blur"
            }
        };
        const router = useRouter();
        const store = useApplicationStore();
        /** запрос к API на авторизацию (получение токена) */
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

        /** наблюдение за нажатием кнопки Enter для убоства входа на форме */
        const keypressEnter = (event) => { if (event.key === "Enter") handleLogin(); };
        /**
         * 1) Проверка токена
         * 2) Включение отслеживания нажатия Enter
         */
        onMounted(() => {
            store.checkToken();
            if (store.isAuth) router.push("/");
            document.addEventListener("keypress", keypressEnter);
        });
        /** Отписка от наблюдения за нажатием Enter */
        onBeforeUnmount(() => document.removeEventListener("keypress", keypressEnter));
        return {
            loginForm,
            handleLogin,
            ruleFormRef,
            rules
        };
    }
});
</script>
