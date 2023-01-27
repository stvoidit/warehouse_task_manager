<template>
    <el-button
        size="small"
        type="primary"
        round
        @click="dialogVisible = true">
        сменить пароль
    </el-button>
    <el-dialog
        v-model="dialogVisible"
        title="Смена пароля"
        append-to-body
        destroy-on-close
        :show-close="false"
        width="30%"
        :before-close="handleClose">
        <el-form
            ref="ruleFormRef"
            label-position="top"
            label-width="100px"
            :model="changePasswordForm"
            :rules="rules"
            status-icon
            style="max-width: 460px">
            <el-form-item
                label="Пароль (минимум 8 символов)"
                prop="newPassword">
                <el-input
                    v-model="changePasswordForm.newPassword"
                    type="password" />
            </el-form-item>
            <el-form-item
                label="Повторение пароля"
                prop="repetitionPassword">
                <el-input
                    v-model="changePasswordForm.repetitionPassword"
                    type="password" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button
                    @click="dialogVisible = false">
                    Закрыть
                </el-button>
                <el-button
                    type="primary"
                    @click="submitForm">
                    Сменить пароль
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from "vue";
import { useApplicationStore } from "@/store";
import { ElMessageBox } from "element-plus";
export default defineComponent({
    setup() {
        const store = useApplicationStore();
        /** ссылка на HTML элемент формы */
        const ruleFormRef = ref();
        /** флаг для отображения модального кона */
        const dialogVisible = ref(false);
        /** обработчик закрытия модального окна */
        const handleClose = () => {
            ruleFormRef.value.resetFields();
            dialogVisible.value = false;
        };
        const changePasswordForm = reactive({
            newPassword: "",
            repetitionPassword: ""
        });
        /** функция-валидатор для пароля */
        const validatePass = (_: any, value: any, callback: any) => {
            if (value === "") {
                callback(new Error("Пожалуйста, введите пароль"));
            } else {
                if (changePasswordForm.repetitionPassword !== "") {
                    if (!ruleFormRef.value) return;
                    ruleFormRef.value.validateField("repetitionPassword", () => null);
                }
                callback();
            }
        };
        /** функция-валидатор для повтора пароля */
        const validatePass2 = (_: any, value: any, callback: any) => {
            if (value === "") {
                callback(new Error("Пожалуйста, введи пароль заново"));
            } else if (value !== changePasswordForm.newPassword) {
                callback(new Error("Пароли не совпадают"));
            } else {
                callback();
            }
        };
        /** правила валидации формы */
        const rules = {
            newPassword: [
                { validator: validatePass, trigger: "blur" },
                { min: 8, message: "Минимальная длина пароля 8 символов", trigger: "blur" }
            ],
            repetitionPassword: [{validator: validatePass2, trigger: "blur"}]
        };
        /** запрос к API на смену пароля */
        const submitForm = async () => {
            if (!ruleFormRef.value) return;
            if (await ruleFormRef.value.validate(valid => valid) === false) return;
            store.changePassword(changePasswordForm)
                .then(() => {
                    alert("Пароль успешно изменен, пожалуйста, перезайдите в систему");
                    store.logOut();
                })
                .catch(error => ElMessageBox.alert(error, "Ошибка", { confirmButtonText: "OK" }));
        };
        return {
            ruleFormRef,
            dialogVisible,
            handleClose,
            changePasswordForm,
            rules,
            submitForm
        };
    }
});
</script>

<style scoped>

</style>
